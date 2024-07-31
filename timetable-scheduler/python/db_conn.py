import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='chuchu',
            database='timetable_db'
        )
        if connection.is_connected():
            # print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def fetch_data(connection, query):
    """Fetch data from the database using the provided query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None

def get_classrooms(connection):
    """Fetch and return all classroom data from the 'classrooms' table."""
    select_classrooms = "SELECT * FROM classrooms"
    return fetch_data(connection, select_classrooms)

# Example of exporting function to get classrooms
def export_classrooms():
    """Export classroom data."""
    connection = create_connection()
    if connection:
        rooms = get_classrooms(connection)
        connection.close()
        return rooms
    return None

# Example usage
if __name__ == "__main__":
    classrooms = export_classrooms()
