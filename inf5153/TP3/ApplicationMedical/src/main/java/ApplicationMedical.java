import org.json.simple.parser.ParseException;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.sql.Date;

public class ApplicationMedical {

    private static final DossierController dossierController = new DossierController();

    public static void main (String [] args) {
        createMainWindow();
    }

    public static void createMainWindow() {
        JFrame mainWindow = new JFrame("Dossier Médical");
        mainWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainWindow.setLayout(null);
        mainWindow.setSize(1000, 700);
        mainWindow.setResizable(false);
        createDefaultUI(mainWindow);
        mainWindow.setVisible(true);
    }

    public static void createDefaultUI(JFrame mainWindow){

        JLabel aucunDossier = new JLabel("Aucun dossier médical d'ouvert");
        aucunDossier.setBounds(400,200,200,100);

        JButton telechargerButton = new JButton("Ouvrir un dossier");
        telechargerButton.setBounds(400, 500, 200,100);
        telechargerButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                mainWindow.remove(aucunDossier);
                mainWindow.remove(telechargerButton);
                mainWindow.revalidate();
                mainWindow.repaint();
                dossierIDInput(mainWindow);
            }
        });

        mainWindow.add(aucunDossier);
        mainWindow.add(telechargerButton);
    }

    public static void dossierIDInput(JFrame mainWindow) {
        JTextField IDInput = new JTextField();
        IDInput.setBounds(300,200,500,50);

        JLabel IDText = new JLabel("ID:");
        IDText.setBounds(275, 200, 25, 50);

        JButton nouveauDossier = new JButton("Nouveau dossier");

        JButton telechargerDossierButton = new JButton("Charger le dossier");
        telechargerDossierButton.setBounds(200, 500, 200,100);
        telechargerDossierButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                DossierMedical dossier = dossierController.telechargDossier(Integer.parseInt(IDInput.getText()));
                mainWindow.remove(IDInput);
                mainWindow.remove(IDText);
                mainWindow.remove(telechargerDossierButton);
                mainWindow.remove(nouveauDossier);
                mainWindow.revalidate();
                mainWindow.repaint();
                afficherDossierUI(mainWindow, dossier, false);
            }
        });

        nouveauDossier.setBounds(600, 500, 200,100);
        nouveauDossier.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                DossierMedical dossier = new DossierMedical();
                dossier.setPrenom("");
                dossier.setNom("");
                dossier.setDate(Date.valueOf("0000-01-01"));
                mainWindow.remove(IDInput);
                mainWindow.remove(IDText);
                mainWindow.remove(telechargerDossierButton);
                mainWindow.remove(nouveauDossier);
                mainWindow.revalidate();
                mainWindow.repaint();
                afficherDossierUI(mainWindow, dossier, true);
            }
        });


        mainWindow.add(IDInput);
        mainWindow.add(IDText);
        mainWindow.add(telechargerDossierButton);
        mainWindow.add(nouveauDossier);
    }

    public static void afficherDossierUI (JFrame mainWindow, DossierMedical dossier, boolean estNouveauDossier) {
        JLabel prenomLabel = new JLabel("Prenom:");
        JTextField prenomField = new JTextField(dossier.getPrenom());
        prenomLabel.setBounds(250, 100, 100, 50);
        prenomField.setBounds(300,100,500,50);

        JLabel nomLabel = new JLabel("Nom:");
        JTextField nomField = new JTextField(dossier.getNom());
        nomLabel.setBounds(270, 200, 40, 50);
        nomField.setBounds(300,200,500,50);

        JLabel dateLabel = new JLabel("Date de Naissance:");
        JTextField dateField = new JTextField(dossier.getDate().toString());
        dateLabel.setBounds(182, 300, 500, 50);
        dateField.setBounds(300,300,500,50);



        JButton saveAndOpenButton = new JButton("Sauvegarder et ouvrir un autre dossier");
        saveAndOpenButton.setBounds(300, 500, 400,100);
        saveAndOpenButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (!estNouveauDossier) {
                    DossierMedical dossierModifier = dossierController.modifierDossier(
                            dossier,
                            prenomField.getText(),
                            nomField.getText(),
                            dateField.getText());
                } else {
                    dossier.setPrenom(prenomField.getText());
                    dossier.setNom(nomField.getText());
                    dossier.setDate(Date.valueOf(dateField.getText()));
                    dossierController.sauvegarderDossier(dossier, true);
                }
                mainWindow.remove(prenomLabel);
                mainWindow.remove(prenomField);
                mainWindow.remove(nomLabel);
                mainWindow.remove(nomField);
                mainWindow.remove(dateLabel);
                mainWindow.remove(dateField);
                mainWindow.remove(saveAndOpenButton);
                mainWindow.revalidate();
                mainWindow.repaint();
                dossierIDInput(mainWindow);
            }
        });

        mainWindow.add(prenomLabel);
        mainWindow.add(prenomField);
        mainWindow.add(nomLabel);
        mainWindow.add(nomField);
        mainWindow.add(dateLabel);
        mainWindow.add(dateField);
        mainWindow.add(saveAndOpenButton);
    }





}
