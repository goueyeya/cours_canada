import sqlite3

co = sqlite3.connect("musique.db")
cursor = co.cursor()
suite = 0

def display_artistes():
    cursor.execute("select id,nom from artiste")
    for row in cursor:
        print(str(row[0])+". "+row[1])

def choose_artiste():
    try:
        choice = int(input("\nEntrez un numero d'artiste afin de voir ses albums :  "))
    except:
        choose_artiste()
    return choice

def display_album_by_artiste(choice):
    cursor.execute("select id, titre from album where artiste_id = ?", [choice])
    print()
    for row in cursor:
        print(str(row[0]) + ". " + row[1])


while suite!=-1:
    display_artistes()
    display_album_by_artiste(choose_artiste())
    suite = int(input("\nTapez un chiffre pour continuer et -1 pour arreter\n"))



co.close()

