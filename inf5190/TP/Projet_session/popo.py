from db.database import Database
from index import send_email
db = Database()

liste = db.get_new_contrevenants()
print(len(list(liste)))

