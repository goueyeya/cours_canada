package com.example.dossierMedical.concept.repository;

import com.example.dossierMedical.concept.entity.DossierMedical;
import org.springframework.data.jpa.repository.JpaRepository;
import java.sql.Date;

import java.util.List;

public interface DossierMedicalRepository extends JpaRepository<DossierMedical, Integer> {

    List<DossierMedical> findByPrenom(String prenom);

    List<DossierMedical> findByNom(String nom);

    List<DossierMedical> findByDateNaissance(Date dateNaissance);


}
