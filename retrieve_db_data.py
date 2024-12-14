import mysql.connector

# Database connection setup
db_config = {
    'host': 'localhost',        # Your server's IP or 'localhost'
    'user': 'root',             # MariaDB username
    'password': 'Cleopatra02@',# MariaDB password
    'database': 'bible_verses'  # Name of your database
}

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Example query: Get all verses associated with "hope"
    emotion_name = "hope"
    query = """
    SELECT v.reference, v.text 
    FROM verses v
    JOIN verse_emotions ve ON v.id = ve.verse_id
    JOIN emotions e ON ve.emotion_id = e.id
    WHERE e.name = %s
    """
    cursor.execute(query, (emotion_name,))

    # Fetch and print results
    verses = cursor.fetchall()
    for reference, text in verses:
        print(f"{reference}: {text}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
