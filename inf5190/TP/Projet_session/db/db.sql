create table contrevenant (
  id_poursuite integer primary key,
  business_id integer,
  date text,
  description var varchar(500),
  adresse,
  date_jugement,
  etablissement,
  montant,
  proprietaire,
  ville varchar(),
  statut varchar(50),
  date_statut text,
  categorie varchar(100)
);