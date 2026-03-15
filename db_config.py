import mysql.connector
from mysql.connector import Error

def create_server_connection(host_name, user_name, user_password, db_name):
    """
    Establishes a connection to the MySQL database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=3307 
        )
        print(f"Successfully connected to the '{db_name}' database.")
    except Error as err:
        print(f"Error: '{err}' - Could not connect to the database.")

    return connection

# --- Testing the Connection ---
if __name__ == '__main__':
    # Replace these variables with your actual database credentials
    DB_HOST = "localhost"  # Usually localhost if running on your HP laptop via XAMPP or MySQL Workbench
    DB_USER = "root"       # Default username for local servers
    DB_PASS = ""           # Enter your MySQL password here (often blank by default on XAMPP)
    DB_NAME = "attendance_system" 

    # Execute the function
    my_db_connection = create_server_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    
    # Always a good habit to close the connection after testing
    if my_db_connection is not None and my_db_connection.is_connected():
        my_db_connection.close()
        print("Connection closed.")