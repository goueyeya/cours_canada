import org.json.simple.parser.ParseException;
import java.io.*;


public class DossierController {

    DossierService dossierService= new DossierService();

    public DossierMedical telechargDossier(int id) {
        try {
            return dossierService.getDossierMedical(id);
        } catch (IOException | ParseException e) {
            return new DossierMedical();
        }
    }

    public void sauvegarderDossier (DossierMedical dossier, boolean estNouveauDossier) {
        try {
            System.out.println("here");
            dossierService.setDossierMedical(dossier, estNouveauDossier);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public DossierMedical modifierDossier(DossierMedical dossier, String prenom, String nom, String date) {
        dossierService.modifierNom(dossier, prenom, nom);
        dossierService.modifierDateNaissance(dossier, date);

        sauvegarderDossier(dossier, false);

        return dossier;
    }
}
