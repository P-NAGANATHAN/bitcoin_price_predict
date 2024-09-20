from flask import Flask, render_template, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL connection details
POSTGRES_HOST = "postgres"  
POSTGRES_DB = "bitcoin"
POSTGRES_USER = "bitcoin_usr"
POSTGRES_PASSWORD = "bitcoin_pwd"

# Function to fetch
def get_latest_bitcoin_data():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM (
            SELECT *
            FROM bitcoin_data
            ORDER BY timestamp DESC
            LIMIT 20
        ) AS latest_data
        ORDER BY timestamp ASC;
        """
        cursor.execute(query)
        
        rows = cursor.fetchall()
        print(f"Rows fetched: {len(rows)}")  

        # Format data 
        data = {
            "timestamps": [row[0] for row in rows],
            "buy_prices": [row[1] for row in rows],
            "sell_prices": [row[2] for row in rows],
            "volumes": [row[3] for row in rows]
        }
        return data

    except Exception as e:
        print(f"Error fetching data: {e}") 
        return {}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/bitcoin-data', methods=['GET'])
def bitcoin_data():
    data = get_latest_bitcoin_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
