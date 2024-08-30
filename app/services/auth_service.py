from database.postgres_connection import postgres_connect


def create_user(username, password_hash, email):
    connection = postgres_connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Define the SQL query for inserting a new user
            insert_user_query = """
            INSERT INTO budget.users (id, password_hash, email)
            VALUES (%s, %s, %s);
            """

            # Execute the query with the provided parameters
            cursor.execute(insert_user_query, (username, password_hash, email))
            connection.commit()
            print("User record inserted successfully")

        except Exception as error:
            print(f"Error while inserting data into users table: {error}")
            return {'status': 'error', 'message': str(error)}

        finally:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return {'status': 'success'}

    else:
        print("Failed to connect to the database")
        return {'status': 'error', 'message': 'Database connection failed'}

def find_user_by_username(username):
    connection = postgres_connect()
    cursor = connection.cursor()

    # Query to find the user by username
    cursor.execute("SELECT id, password_hash FROM budget.users WHERE id = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return {'username': user[0], 'password_hash': user[1]}
    else:
        return None