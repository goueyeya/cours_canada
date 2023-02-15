import sqlite3

with open("database/db.sql","r") as file:
    script = file.read()
co = sqlite3.connect("database/database.db")
cursor = co.cursor()
cursor.execute(script)
co.commit()
co.close()