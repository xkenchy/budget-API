import psycopg2
import os

def postgres_connect():
    try:
        connection = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
        return connection

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None
