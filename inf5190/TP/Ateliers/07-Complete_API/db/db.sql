create table person (
  id integer primary key,
  nom varchar(50),
  prenom varchar(50),
  age integer,
  date_naissance text
 );

create table gradePerson (
  idPerson integer,
  idGrade integer,
  foreign key(idPerson) references person(id),
  foreign key(idGrade) references grade(id)
 );

 create table grade (
  id integer primary key,
  description varchar(50)
 );