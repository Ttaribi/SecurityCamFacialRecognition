import os
import glob
import sqlite3

# Reset DB
conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS STUDENTS")
cursor.execute('''
    CREATE TABLE STUDENTS (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        age INTEGER
    );
''')
conn.commit()
conn.close()
print("Database reset.")

# Clear dataset images
files = glob.glob("dataset/*.jpg")
for f in files:
    os.remove(f)
print("Dataset images cleared.")
