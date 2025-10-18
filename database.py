import sqlite3

def init_db():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT,
            upcoming INTEGER DEFAULT 0,
            payment_type TEXT DEFAULT 'Cash'
        )
    ''')
    conn.commit()
    conn.close()