import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.sql.Date;
import java.util.Scanner;

public class DossierService {

    public DossierMedical getDossierMedical(int id) throws IOException, ParseException {

        URL url = new URL("http://localhost:8080/dossierMedicalById/"+ id);

        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.connect();

        Scanner scanner = new Scanner(url.openStream());
        String inline = "";
        while (scanner.hasNext()) {
            inline += scanner.nextLine();
        }
        scanner.close();

        JSONParser parse = new JSONParser();
        JSONObject data_obj = (JSONObject) parse.parse(inline);
        DossierMedical dossierMedical = new DossierMedical();

        dossierMedical.setId(Integer.parseInt(data_obj.get("id").toString()));
        dossierMedical.setPrenom(data_obj.get("prenom").toString());
        dossierMedical.setNom(data_obj.get("nom").toString());
        dossierMedical.setDate(Date.valueOf(data_obj.get("dateNaissance").toString()));

        return dossierMedical;
    }

    public boolean setDossierMedical(DossierMedical dossier, boolean estNouveauDossier) throws IOException {
        URL url;
        if (!estNouveauDossier) {
            url = new URL("http://localhost:8080/update");
        } else {
            url = new URL("http://localhost:8080/addDossierMedical");
        }
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        if (!estNouveauDossier) {
            connection.setRequestMethod("PUT");
        } else {
            connection.setRequestMethod("POST");
        }
        connection.setRequestProperty("accept", "*/*");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setDoOutput(true);

        String jsonInputString = "";
        if (!estNouveauDossier) {
            jsonInputString = "{\"id\": \" " + dossier.getId() + "\", \"prenom\": \"" + dossier.getPrenom() + "\"," +
                    " \"nom\": \"" + dossier.getNom() + "\", \"dateNaissance\": \"" + dossier.getDate().toString() + "\"}";
        } else {
            jsonInputString = "{\"prenom\": \"" + dossier.getPrenom() + "\"," +
                    " \"nom\": \"" + dossier.getNom() + "\", \"dateNaissance\": \"" + dossier.getDate().toString() + "\"}";
        }
        System.out.println(jsonInputString);

        try(OutputStream os = connection.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"))) {
            String response = "";
            String line;
            while ((line = br.readLine()) != null) {
                response += line;
            }
            return true;
        } catch (Exception e) {
            return false;
        }

    }

    public String modifierNom (DossierMedical dossier, String prenom, String nom) {
        dossier.setPrenom(prenom);
        dossier.setNom(nom);
        return prenom + " " + nom;
    }

    public String modifierDateNaissance(DossierMedical dossier, String dateNaissance) {
        dossier.setDate(Date.valueOf(dateNaissance));
        return dateNaissance;
    }
}
