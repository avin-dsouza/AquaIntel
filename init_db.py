import sqlite3

conn = sqlite3.connect('database/aqua.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS water_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    ph REAL,
    tds REAL,
    hardness REAL,
    do REAL,
    date TEXT,
    score INTEGER,
    status TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully!")