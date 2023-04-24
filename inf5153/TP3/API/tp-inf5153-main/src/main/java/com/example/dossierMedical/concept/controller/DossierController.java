package com.example.dossierMedical.concept.controller;


import com.example.dossierMedical.concept.entity.DossierMedical;
import com.example.dossierMedical.concept.service.DossierMedicalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.List;

@RestController
public class DossierController {

    @Autowired
    private DossierMedicalService service;

    @PostMapping("/addDossierMedical")
    public DossierMedical addDossierMedical(@RequestBody DossierMedical dossierMedical) {
        return service.saveDossierMedical(dossierMedical);
    }

    @PostMapping("/addDossierMedicalList")
    public List<DossierMedical> addDossierMedicalList(@RequestBody List<DossierMedical> dossierMedicalList) {
        return service.saveDossierMedicalList(dossierMedicalList);
    }

    @GetMapping("/dossierMedicalList")
    public List<DossierMedical> findAllDossierMedical() {
        return service.getDossierMedicalList();
    }

    @GetMapping("/dossierMedicalById/{id}")
    public DossierMedical findDossierMedicalById(@PathVariable int id) {
        return service.getDossierMedicaById(id);
    }

    @GetMapping("/dossierMedicalByPrenom/{prenom}")
    public List<DossierMedical> findDossierMedicalByPrenom(@PathVariable String prenom) {
        return service.getDossierMedicalByPrenom(prenom);
    }

    @GetMapping("/dossierMedicalByNom/{nom}")
    public List<DossierMedical> findDossierMedicalByNom(@PathVariable String nom) {
        return service.getDossierMedicalByNom(nom);
    }

    @GetMapping("/dossierMedicalByDateNaissance/{dateNaissance}")
    public List<DossierMedical> findDossierMedicalByNom(@PathVariable Date dateNaissance) {
        return service.getDossierMedicalByDateNaissance(dateNaissance);
    }

    @PutMapping("/update")
    public DossierMedical updateDossierMedical(@RequestBody DossierMedical dossierMedical) {
        return service.updateDossierMedical(dossierMedical);
    }

    @DeleteMapping("/delete/{id}")
    public String deleteProduct (@PathVariable int id) {
        return service.deleteDossierMedical(id);
    }
}
