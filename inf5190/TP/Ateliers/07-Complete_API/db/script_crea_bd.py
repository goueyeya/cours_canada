import sqlite3

with open("database/db.sql","r") as file:
    script = file.read()
co = sqlite3.connect("db/db.db")
cursor = co.cursor()
cursor.executescript(script)
co.commit()
co.close()