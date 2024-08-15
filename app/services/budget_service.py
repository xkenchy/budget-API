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


def get_budget_left():
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Step 1: Get the user's monthly budget
            user_id = 'ben123'
            get_budget_query = """
            SELECT monthly_budget FROM budget.users
            WHERE id = %s;
            """
            cursor.execute(get_budget_query, (user_id,))
            result = cursor.fetchone()
            if result is None:
                print(f"No budget found for user {user_id}")
                return None

            monthly_budget = result[0]

            # Step 2: Calculate the sum of the purchases for the month to date
            start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime(
                '%Y-%m-%d %H:%M:%S')
            end_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            get_purchases_sum_query = """
            SELECT SUM(price) FROM budget.purchases
            WHERE user_id = %s AND created_at BETWEEN %s AND %s;
            """
            cursor.execute(get_purchases_sum_query, (user_id, start_date, end_date))
            total_spent = cursor.fetchone()[0] or 0  # Default to 0 if no purchases

            # Step 3: Calculate the remaining budget
            remaining_budget = monthly_budget - total_spent

            return remaining_budget

        except Exception as error:
            print(f"Error while calculating remaining budget: {error}")
            return None

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")
        return None
def upsert_user_monthly_data(monthly_inc, monthly_save, total_mandatory, reoccurrings):
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()
            user_id = 'ben123'  # Hardcoded user ID for Ben

            # Upsert the user's monthly data (monthly_inc, monthly_save, monthly_mandatory)
            upsert_user_query = """
            INSERT INTO budget.users (id, monthly_inc, monthly_save, monthly_mandatory)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET monthly_inc = EXCLUDED.monthly_inc,
                monthly_save = EXCLUDED.monthly_save,
                monthly_mandatory = EXCLUDED.monthly_mandatory;
            """
            cursor.execute(upsert_user_query, (user_id, monthly_inc, monthly_save, total_mandatory))

            # Insert the recurring expenses into the monthly_reoccurrings table
            insert_reoccurring_query = """
            INSERT INTO budget.monthly_reoccurrings (user_id, description, amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, description) DO UPDATE
            SET amount = EXCLUDED.amount;
            """

            for item in reoccurrings:
                cursor.execute(insert_reoccurring_query, (user_id, item['description'], item['amount']))

            connection.commit()
            print("User's monthly data and recurring expenses upserted successfully")

        except Exception as error:
            print(f"Error while upserting user's monthly data and recurring expenses: {error}")

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")
def get_user_monthly_data():
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()
            user_id = 'ben123'  # Hardcoded user ID for Ben

            # Get monthly data from users table
            get_user_data_query = """
            SELECT monthly_inc, monthly_save, monthly_budget, monthly_mandatory
            FROM budget.users
            WHERE id = %s;
            """
            cursor.execute(get_user_data_query, (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                return {"error": "User not found"}, 404

            monthly_inc, monthly_save, monthly_budget, monthly_mandatory = user_data

            # Get all recurring expenses for the user
            get_reoccurrings_query = """
            SELECT description, amount
            FROM budget.monthly_reoccurrings
            WHERE user_id = %s;
            """
            cursor.execute(get_reoccurrings_query, (user_id,))
            reoccurrings = cursor.fetchall()

            # Format the reoccurrings into a list of dictionaries
            reoccurrings_list = [{"description": row[0], "amount": row[1]} for row in reoccurrings]

            return {
                "monthly_inc": monthly_inc,
                "monthly_save": monthly_save,
                "monthly_budget": monthly_budget,
                "monthly_mandatory": monthly_mandatory,
                "reoccurrings": reoccurrings_list
            }

        except Exception as error:
            print(f"Error while fetching user's monthly data: {error}")
            return {"error": "Internal server error"}, 500

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    else:
        print("Failed to connect to the database")
        return {"error": "Database connection failed"}, 500
