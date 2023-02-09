create table utilisateur(
    id integer primary key,
    nom varchar(35),
    prenom varchar(35),
    courriel varchar(50),
    date_inscription date,
    salt varchar(24),
    mdp varchar(500)
);

