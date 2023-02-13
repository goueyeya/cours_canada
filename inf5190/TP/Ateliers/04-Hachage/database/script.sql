create table utilisateur(
    id integer primary key,
    nom varchar(32),
    prenom varchar(32),
    courriel varchar(100),
    date_inscription date,
    salt varchar(32),
    mdp varchar(128)
);

