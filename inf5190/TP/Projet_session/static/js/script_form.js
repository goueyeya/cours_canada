// Déclenche un événement quand le formulaire est soumis
document.getElementById("formulaire_image").addEventListener("submit", function(event) {
  event.preventDefault();
  fetch('/save_img', {method: 'POST'})
  .then(response => {
    if(response.ok){
      window.location.replace("/confirmation_formulaire_plainte");
    }
  })// Déclenche un événement quand le formulaire est soumis
document.getElementById("formulaire_plainte").addEventListener("submit", function(event) {
  event.preventDefault();

  let nom_etablissement = document.getElementById("nom_etablissement").value;
  let adresse = document.getElementById("adresse").value;
  let ville = document.getElementById("ville").value;
  let date_visite = document.getElementById("date_visite").value;
  let nom = document.getElementById("nom").value;
  let prenom = document.getElementById("prenom").value;
  let description_probleme = document.getElementById("description_probleme").value;
  let error = document.getElementById("container_reponse").value;
  if(validateData(nom_etablissement, adresse, ville, date_visite, nom, prenom, description_probleme, error)){
    fetch('/api/demande', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "nom_etablissement": nom_etablissement,
      "adresse": adresse,
      "ville": ville,
      "date_visite": date_visite,
      "nom": nom,
      "prenom": prenom,
      "description_probleme": description_probleme
    })
  })
    .then(response => {
      if(response.ok){
        window.location.replace("/confirmation_formulaire_plainte");
      }
    })
    .catch(error => {
      console.error('Erreur :', error);
      error.innerHTML = 'Une erreur est survenue lors de l\'envoi de la demande.';
    });
  }
});

function validateData(nom_etablissement, adresse, ville, date_visite, nom, prenom, description_probleme, error) {
  if (nom_etablissement === "" || adresse === "" || ville === "" || date_visite === "" || nom === "" || prenom === "" || description_probleme === "") {
    error.innerHTML = "Veuillez remplir tous les champs obligatoires.";
    return false;
  }
  // Vérification du format de la date de visite
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(date_visite)) {
    error.innerHTML = 'Veuillez entrer une date de visite valide (format : yyyy-mm-dd).';
    return false;
  }
  return true;
}

  .catch(error => {
    console.error('Erreur :', error);
    error.innerHTML = 'Une erreur est survenue lors de l\'envoi de la demande.';
  });
}});

function validateData(nom_etablissement, adresse, ville, date_visite, nom, prenom, description_probleme, error) {
  if (nom_etablissement === "" || adresse === "" || ville === "" || date_visite === "" || nom === "" || prenom === "" || description_probleme === "") {
    error.innerHTML = "Veuillez remplir tous les champs obligatoires.";
    return false;
  }
  // Vérification du format de la date de visite
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(date_visite)) {
    error.innerHTML = 'Veuillez entrer une date de visite valide (format : yyyy-mm-dd).';
    return false;
  }
  return true;
}