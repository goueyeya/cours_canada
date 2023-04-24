package com.example.dossierMedical.concept.service;

import com.example.dossierMedical.concept.entity.DossierMedical;
import com.example.dossierMedical.concept.repository.DossierMedicalRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;

@Service
public class DossierMedicalService {

    @Autowired
    private DossierMedicalRepository repository;

    public DossierMedical saveDossierMedical(DossierMedical dossierMedical) {
        return repository.save(dossierMedical);
    }

    public List<DossierMedical> saveDossierMedicalList(List<DossierMedical> dossierMedical) {
        return repository.saveAll(dossierMedical);
    }

    public List<DossierMedical> getDossierMedicalList() {
        return repository.findAll();
    }

    public DossierMedical getDossierMedicaById(int id) {
        return repository.findById(id).orElse(null);
    }

    public List<DossierMedical> getDossierMedicalByPrenom(String prenom) {
        return repository.findByPrenom(prenom);
    }

    public List<DossierMedical> getDossierMedicalByNom(String nom) {
        return repository.findByNom(nom);
    }

    public List<DossierMedical> getDossierMedicalByDateNaissance(Date dateNaissance) {
        return repository.findByDateNaissance(dateNaissance);
    }

    public String deleteDossierMedical(int id) {
        repository.deleteById(id);
        return "Dossier médical supprimé!";
    }

    public DossierMedical updateDossierMedical (DossierMedical dossierMedical) {
        DossierMedical dossierExistant = repository.findById(dossierMedical.getId()).orElse(null);
        dossierExistant.setNom(dossierMedical.getNom());
        dossierExistant.setPrenom(dossierMedical.getPrenom());
        dossierExistant.setDateNaissance(dossierMedical.getDateNaissance());
        return repository.save(dossierExistant);
    }


}
