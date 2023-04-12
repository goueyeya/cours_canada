create table contrevenant (
  id integer primary key,
  id_poursuite integer unique,
  business_id integer,
  date text,
  description varchar(500),
  adresse varchar(50),
  date_jugement text,
  etablissement varchar(100),
  montant integer,
  proprietaire varchar(50),
  ville varchar(50),
  statut varchar(50),
  date_statut text,
  categorie varchar(100)
  );

CREATE TABLE user(
  id INTEGER PRIMARY KEY,
  nom_complet varchar(100),
  email TEXT ,
  etablissements TEXT,
  password TEXT,
  salt TEXT
  );

create table session (
  id integer primary key,
  id_session varchar(32),
  utilisateur_email text
);

create table image(
  id varchar(32) primary key,
  email_user text unique,
  image blob
)