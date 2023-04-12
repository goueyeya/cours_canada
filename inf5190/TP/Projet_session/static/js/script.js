// récpère les données et affiche le tableau
function displayTableau(){
 var error = document.getElementById("error_table"); //contenant pour écrire les messages en cas d'erreur
 const date_debut = document.getElementById("date_debut").value;
 const date_fin = document.getElementById("date_fin").value;
 const tableau = document.getElementById("table_contrevenant");
 tableau.innerHTML = "";
 error.innerHTML = "";
 if(!(validateDate(date_debut, date_fin))){
   error.innerHTML = "Pas de contrevenants trouvés pour ces dates.";
 }
 else{
   fetch("/api/contrevenants?du="+date_debut+"&au="+date_fin)
   .then(response => response.json())
   .then(response => {
     createTableau(response);
   })
   .catch(err => {
     error.innerHTML =  "Pas de contrevenants trouvés pour ces dates.";
   });
 }
}

//fonction qui créee le tableau
function createTableau(data){
 var error = document.getElementById("error_table"); //contenant pour écrire les messages en cas d'erreur
 if (data.length === 0){
   error.innerHTML = "Pas de contrevenants trouvés pour ces dates.";
 }
 else{
   const tableau = document.getElementById("table_contrevenant");
   var {listeEtablissement, nbContravenants} = createLists(data);
   tableau.innerHTML = `<tr>
                          <th>Nom d'établissement</th>
                          <th>Nombre de contrevenants</th>
                        </tr>`;
   //boucle qui crée le tableau
   for(var i = 0; i < listeEtablissement.length ;i++){
     var row = `<tr>
                  <td>${listeEtablissement[i]}</td>
                  <td>${nbContravenants[i]}</td>
                </tr>`;
     tableau.innerHTML += row ;
   }
 }
}

// créé les listes d'établissement
function createLists(data){
   var listeEtablissement = new Array();
   var nbContravenants = new Array();
   //boucle qui crée 2 listes contenants les etablissement et leurs nombre de contrevenant
   for(var i = 0; i< data.length; i++){
     let j = 0 ;
     var estPresent = Boolean(false);
     while(!estPresent && j<listeEtablissement.length){
       var estPresent = (data[i]["etablissement"] === listeEtablissement[j])
       if(estPresent){
         nbContravenants[j]++;
       }
        j++;
     }
     if(!estPresent){
       listeEtablissement.push(data[i]["etablissement"])
       nbContravenants.push(1);
       }
   }
   return {listeEtablissement, nbContravenants};
}

//fonction qui valide les données en entrées
function validateDate(date_debut, date_fin){
   try{
     if (date_fin === "" || date_debut === ""){
       return false;
     }
     var deb = new Date(date_debut);
     var fin = new Date(date_fin);
     if(fin < deb){
       return False;
     }
     return true;
   }
   catch(error){
     return false;
   }
}

// déclenche un évenement quand la recherche est lancée
document.getElementById("submit_quick_search").addEventListener("click", displayTableau);

function displayInfosEtablissement(){
  const name = document.getElementById("liste_etablissement").value;
  const container = document.getElementById("container_list");
  container.innerHTML = "";
  if(!(name === "")){
       fetch("/api/contrevenant?name="+encodeURIComponent(name))
   .then(response => response.json())
   .then(response => {
     createInfos(response);
   })
   .catch(err => {
     console.log(err);
     error.innerHTML =  "Pas de contrevenants trouvés pour ces dates.";
   });
  }
}
 // affiche les infos sur un contrevenants
function createInfos(data){
  const container = document.getElementById("container_list");
  container.innerHTML = `<br><div class='container bg-light contrevenant'>
                         <h5>${data[0]["etablissement"]}<i>(${data[0]["statut"]}</i> depuis le ${data[0]["date_statut"]} )</h5>
                         <small class="text-muted">Adresse: ${data[0]["adresse"]}, ${data[0]["ville"]}</small><br>
                         <small class="text-muted">Propriétaire: ${data[0]["proprietaire"]}</small><br>
                         <small class="text-muted">Identifiant restaurant: ${data[0]["business_id"]}</small>
                         </div><br>`;

  for(var i = 0; i<data.length; i++){
    container.innerHTML += `<hr><div>
                            <h6>Contrevenant n°${i+1} :</h6>
                            <small class="text-muted">Identifiant de la poursuite: ${data[i]["id_poursuite"]} </small><br>
                            <small class="text-muted">Date de jugement: ${data[i]["date_jugement"]}</small><br>
                            <small class="text-muted">Montant de l'amende : ${data[i]["montant"]} CAD</small>
                            <p class="text-muted">Description: ${data[i]["description"]} <i>(Enquête du ${data[i]["date"]})</i></p>
                            <div>`;
  }
}
// déclenche un évenement quand la recherche est lancée
document.getElementById("submit_search_by_name").addEventListener("click", displayInfosEtablissement)