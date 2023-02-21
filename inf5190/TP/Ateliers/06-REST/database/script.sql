drop table if exists livre;

create table livre(
  id integer primary key,
  titre text,
  auteur text,
  annee_publi text,
  nb_pages integer,
  nb_chap integer
);

insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Les Miserables', 'Victor Hugo', '1862', 1232, 48);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('La Divine Comedie', 'Dante Alighieri', '1320', 713, 100);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Comte de Monte-Cristo', 'Alexandre Dumas', '1844', 1312, 117);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Guerre et Paix', 'Leon Tolstoï', '1869', 1392, 361);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', '1954', 1178, 6);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('1984', 'George Orwell', '1949', 328, 2);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Nom de la Rose', 'Umberto Eco', '1980', 592, 7);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Crime de l''Orient-Express', 'Agatha Christie', '1934', 256, 3);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('La Peste', 'Albert Camus', '1947', 320, 5);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Moby Dick', 'Herman Melville', '1851', 720, 135);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Orgueil et Prejuges', 'Jane Austen', '1813', 432, 61);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Portrait de Dorian Gray', 'Oscar Wilde', '1890', 256, 20);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('L''Etranger', 'Albert Camus', '1942', 123, 2);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Hobbit', 'J.R.R. Tolkien', '1937', 304, 19);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Les Fourmis', 'Bernard Werber', '1991', 300, 4);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Guide du voyageur galactique', 'Douglas Adams', '1979', 193, 35);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Vieil Homme et la Mer', 'Ernest Hemingway', '1952', 127, 3);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Dernier des Mohicans', 'James Fenimore Cooper', '1826', 416, 33);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Rouge et le Noir', 'Stendhal', '1830', 608, 2);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Les Trois Mousquetaires', 'Alexandre Dumas', '1844', 704, 67);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Chateau de l''Aventure', 'Geronimo Stilton', '2004', 128, 7);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('La Case de l''oncle Tom', 'Harriet Beecher Stowe', '1852', 464, 45);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Les Rois maudits', 'Maurice Druon', '1955', 384, 7);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Les Hauts de Hurlevent', 'Emily Bronte', '1847', 416, 34);
insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES ('Le Parfum', 'Patrick Suskind', '1985', 272, 51);

--data en json
"{
	"annee_publi": 1078,
	"auteur": "Sun Tzu",
	"nb_chap": 13,
	"nb_pages": 95,
	"titre": "L'art de la guerre"
}
"