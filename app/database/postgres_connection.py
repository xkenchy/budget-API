import os
import boto3
import psycopg2
import psycopg2.extras

def postgres_connect():
    try:
        # Check if running in AWS Lambda
        if os.getenv('AWS_EXECUTION_ENV') is not None:
            # Cloud (AWS Lambda) - Use IAM authentication
            rds_client = boto3.client('rds')
            token = rds_client.generate_db_auth_token(
                DBHostname=os.getenv('DB_HOST'),
                Port=int(os.getenv('DB_PORT', 5432)),
                DBUsername=os.getenv('DB_USER'),
                Region=os.getenv('AWS_REGION')
            )

            connection = psycopg2.connect(
                user=os.getenv('DB_USER'),
                password=token,
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                sslmode='require',
                sslrootcert='rds-combined-ca-bundle.pem'
            )

        else:
            # Local - Use environment variables for credentials
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
