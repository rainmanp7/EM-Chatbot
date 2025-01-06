# setup_database.py
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create the math_operations table
cursor.execute("""
CREATE TABLE IF NOT EXISTS math_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,
    result TEXT NOT NULL
)
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")

# Test for setup_database.py
if __name__ == "__main__":
    print("Testing setup_database.py...")
    # Re-run the script to ensure it doesn't fail if the table already exists
    print("Attempting to create the database and table again...")
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='math_operations'")
    table_exists = cursor.fetchone()
    if table_exists:
        print("Table 'math_operations' already exists. No issues detected.")
    else:
        print("Table 'math_operations' was not created. Check the script for errors.")
    conn.close()