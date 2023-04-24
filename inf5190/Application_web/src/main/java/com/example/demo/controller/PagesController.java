package com.example.demo.controller;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Controller
public class PagesController {
    @GetMapping("/")
    public String display_home_page(){
        return "pages/home";
    }

    @PostMapping("/identification")
    public String display_dossier(@RequestParam String id, ModelMap model) throws JsonProcessingException {
        int id_p;
        try{
            id_p = Integer.parseInt(String.valueOf(id));
        }catch (Exception e){
            return "pages/home";
        }
        String url = "http://localhost:8080/dossierMedicalById/" + id_p;
        RestTemplate restTemplate = new RestTemplate();
        String json = restTemplate.getForObject(url, String.class);
        List<Map<String, Object>> dataList = null;
        // Analyser le JSON et extraire les données nécessaires
        // Dans cet exemple, nous supposons que le JSON est un objet avec des champs "id", "nom" et "prenom"
        if (json != null) {
            Map<String, Object> data = new ObjectMapper().readValue(json, new TypeReference<Map<String, Object>>() {});
            dataList = new ArrayList<>();
            dataList.add(data);
        }
        List<Map<String, String>> myDataList = new ArrayList<>();
        if (dataList != null && !dataList.isEmpty()) {
            myDataList = dataList.stream()
                    .map(map -> {
                        Map<String, String> myMap = new HashMap<>();
                        myMap.put("id", map.get("id").toString());
                        myMap.put("nom", (String) map.get("nom"));
                        myMap.put("prenom", (String) map.get("prenom"));
                        myMap.put("date_naissance", (String) map.get("dateNaissance"));
                        return myMap;
                    })
                    .collect(Collectors.toList());
        } else {
            Map<String, String> myMap = new HashMap<>();
            myMap.put("id", "???");
            myMap.put("nom", "???");
            myMap.put("prenom", "???");
            myMap.put("date_naissance", "???");
            myDataList.add(myMap);
        }
        // Stocker les données dans le ModelMap et retourner le nom de la vue
        model.addAttribute("attributs", myDataList);
        return "pages/dossier";
    }
}
