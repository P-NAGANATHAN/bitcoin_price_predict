# Bitcoin Data Stream Processing and Prediction Project

## Description

This project implements a real-time Bitcoin data processing pipeline using **Kafka**, **Spark**, **Hadoop**, and **Docker**. The pipeline simulates Bitcoin price data, processes the data in real-time, stores it in HDFS, and performs predictive analysis using machine learning models. Additionally, it includes a web-based interface for monitoring data and visualizing predictions.

### Key Features:
- **Real-time Bitcoin price simulation** with a custom Python simulator.
- **Kafka** for data streaming and message brokering.
- **Apache Spark** for real-time processing and machine learning model execution.
- **Hadoop HDFS** for distributed storage of processed data.
- **PostgreSQL** for relational data storage and interaction with **Superset** for data visualization.
- **Flask** as a frontend to display Bitcoin price data and predictions.
- **Superset** for interactive data dashboards.

## Technologies Used

- **Docker**: Containerization of services
- **Apache Hadoop (HDFS)**: Distributed file storage
- **Apache Kafka**: Message streaming platform
- **Apache Spark**: Distributed data processing and machine learning
- **PostgreSQL**: Relational database for storing processed data
- **Flask**: Frontend web server for displaying predictions
- **Superset**: Data visualization and dashboard tool

## Prerequisites

- **Docker** and **Docker Compose** should be installed on your system.

## Installation and Setup

1. Clone the repository
2. docker-compose up
