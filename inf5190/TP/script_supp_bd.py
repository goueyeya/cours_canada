import sqlite3

co = sqlite3.connect("chemin bd")
cursor = co.cursor()
cursor.execute("delete from *")
co.commit()
co.close()