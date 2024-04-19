import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('diary2.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Update table to include time and ensure the entry column is suitable for binary data
sql = '''
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    date TEXT,
    time TEXT,
    entry BLOB 
)
'''
cursor.execute(sql)

# Commit your changes and close the connection
conn.commit()
conn.close()
