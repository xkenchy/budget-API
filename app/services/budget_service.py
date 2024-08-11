from database.postgres_connection import postgres_connect
from datetime import datetime

def insert_purchase(price, category, item):
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()
            user_id = 'ben123'  # Hardcoded user ID for Ben
            insert_purchase_query = """
            INSERT INTO budget.purchases (user_id, price, category, item)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_purchase_query, (user_id, price, category, item))
            connection.commit()
            print("Purchase record inserted successfully")

        except Exception as error:
            print(f"Error while inserting data into purchases table: {error}")

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")

def get_month_to_date_purchases():
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()
            user_id = 'ben123'  # Hardcoded user ID for Ben
            # Assuming the server is set to GMT or timestamps are stored in UTC
            start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            end_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            get_purchases_query = """
            SELECT * FROM budget.purchases
            WHERE user_id = %s AND created_at BETWEEN %s AND %s;
            """
            cursor.execute(get_purchases_query, (user_id, start_date, end_date))
            purchases = cursor.fetchall()
            return purchases

        except Exception as error:
            print(f"Error while querying purchases: {error}")
            return []

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")
        return []
def get_purchase_categories():
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()
            get_categories_query = """
            SELECT name, description FROM budget.category_enum;
            """
            cursor.execute(get_categories_query)
            categories = cursor.fetchall()
            # Map the results to a list of dictionaries
            categories_list = [{"name": row[0], "description": row[1]} for row in categories]
            return categories_list

        except Exception as error:
            print(f"Error while querying categories: {error}")
            return []

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")
        return []
