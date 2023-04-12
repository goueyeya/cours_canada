// Déclenche un événement quand le formulaire est soumis
document.getElementById("formulaire_sub").addEventListener("submit", function(event) {
  event.preventDefault();
  let nom_complet = document.getElementById("nom_complet").value;
  let email = document.getElementById("email").value;
  let chaine_etablissements = document.getElementById("etablissements").value;
  var etablissements = parserChaine(chaine_etablissements)
  let password = document.getElementById("password").value;
  let error = document.getElementById("error")

  if(validateData(nom_complet, email, etablissements, password, error)){
    fetch('/api/utilisateur', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "nom_complet": nom_complet,
      "email": email,
      "etablissements": etablissements,
      "password": password
    })
  })
    .then(response => {
      if(response.ok){
          window.location.replace("/confirmation_formulaire_compte");
      }
    })
    .catch(error => {
      console.error('Erreur :', error);
      error.innerHTML = 'Une erreur est survenue lors de l\'envoi de la demande.';
    });
  }
});

function parserChaine(chaine) {
  var tableauChaine = chaine.split(",");
  return tableauChaine;
};

function validateData(nom_complet, email, etablissements, password, error) {
  if (nom_complet == "" || email == "" || etablissements == "" || password == "") {
    error.innerHTML = "Veuillez remplir tous les champs obligatoires.";
    return false;
  }
  return true;
};