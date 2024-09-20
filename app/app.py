from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Define the schema for Bitcoin data
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("buy_price", FloatType(), True),
    StructField("sell_price", FloatType(), True),
    StructField("volume", FloatType(), True)
])

# Create Spark session
spark = SparkSession.builder \
    .appName("BitcoinDataToPostgres") \
    .getOrCreate()

# Read data from Kafka
bitcoin_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "bitcoin_data_stream") \
    .load()

# Parse the JSON data
bitcoin_parsed_df = bitcoin_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# PostgreSQL JDBC connection properties
jdbc_url = "jdbc:postgresql://postgres:5432/bitcoin"
connection_properties = {
    "user": "bitcoin_usr",
    "password": "bitcoin_pwd",
    "driver": "org.postgresql.Driver"
}

# Write the data to PostgreSQL
query = bitcoin_parsed_df.writeStream \
    .foreachBatch(lambda df, _: df.write.jdbc(url=jdbc_url, table="bitcoin_data", mode="append", properties=connection_properties)) \
    .start()

query.awaitTermination()
