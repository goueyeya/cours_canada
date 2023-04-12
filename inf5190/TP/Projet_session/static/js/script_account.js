//Déclenche un événement quand le formulaire de mise à jour de l'image est soumis
document.getElementById("formulaire_image").addEventListener("submit", function(event) {
  event.preventDefault();
  const photo = document.getElementById("photo");
  const photo_file = photo.files[0];
  const formData = new FormData();
  let container = document.getElementById("container_image");
  formData.append("photo", photo_file);
  fetch('/save_img', {
    method: 'POST',
    body: formData
    })
  .then(response => {
    if(response.ok){
      return response.text(); // récupérer le contenu de la réponse en tant que chaîne de texte
    }
    else{
      window.location.reload();
    }
  })
  .then(content => {
    container.innerHTML = content; // afficher le contenu de la réponse dans le conteneur d'image
  })
  .catch(error => {
    console.error('Erreur :', error);
  });
});


// Déclenche un événement quand le formulaire  d'envoi des etablissements est soumis
document.getElementById("formulaire_etablissement").addEventListener("submit", function(event) {
  event.preventDefault();
  let chaine_etablissements = document.getElementById("etablissements").value;
  var etablissements = parserChaine(chaine_etablissements);
  let error = document.getElementById("error");
  fetch('/save_etablissement', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "etablissements": etablissements,
    })
  })
  .then(response => {
    if(response.ok){
        chaine_etablissements.innerHTML = response.text;
    }
  })
  .catch(error => {
    console.error('Erreur :', error);
    error.innerHTML = 'Une erreur est survenue lors de l\'envoi de la demande.';
  });
 });

function parserChaine(chaine) {
  var tableauChaine = chaine.split(";");
  return tableauChaine;
};

