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