import sqlite3

conn = sqlite3.connect("expense.db")
cursor = conn.cursor()

# Budget Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_income REAL,
    rent_limit REAL,
    food_limit REAL,
    travel_limit REAL,
    study_limit REAL,
    entertainment_limit REAL,
    misc_limit REAL
)
""")

# Expense Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    category TEXT,
    description TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")