import os
import psycopg2
import psycopg2.extras

def postgres_connect():
    try:
        # Use the same connection method for both local and cloud environments
        connection = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME')
        )

        print("Database connection established successfully.")
        return connection

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None
