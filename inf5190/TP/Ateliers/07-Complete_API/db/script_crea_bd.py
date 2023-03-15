import sqlite3

with open("db.sql","r") as file:
    script = file.read()
co = sqlite3.connect("db.db")
cursor = co.cursor()
cursor.executescript(script)
co.commit()
co.close()
