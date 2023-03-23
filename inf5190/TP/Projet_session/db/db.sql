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