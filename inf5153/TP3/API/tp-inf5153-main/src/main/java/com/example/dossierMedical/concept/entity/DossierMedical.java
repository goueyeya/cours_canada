package com.example.dossierMedical.concept.entity;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.sql.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "DossierMedical_TBL")
public class DossierMedical {

    @Id
    @GeneratedValue
    private int id;

    @Column
    private String prenom;

    @Column
    private String nom;

    @Column
    @Temporal(TemporalType.DATE)
    private Date dateNaissance;



}
