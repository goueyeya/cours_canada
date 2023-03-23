function onNomChange() {
  let infosPerson = document.getElementById("infos");

  const id = document.getElementById("champ-persons").value;
  if (id === ""){
    infosPerson.value = "";
  }
  else{
    fetch("/person/"+id)
    .then(response => response.text())
    .then(response => {
       infosPerson.innerHTML = response;
       infosPerson.value = "";
    })
    .catch(err => {
      console.log("Erreur avec le serveur :", err);
    });
  }
}

document.getElementById("champ-persons").addEventListener("change", onNomChange);