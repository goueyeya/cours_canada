import sqlite3

with open("database/script.sql","r") as file:
    script = file.read()
co = sqlite3.connect("database/database.db")
cursor = co.cursor()
cursor.executescript(script)
co.commit()
co.close()