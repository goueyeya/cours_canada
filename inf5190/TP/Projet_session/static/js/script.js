function displayTableau() {
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

document.getElementById("submit_quick_search").addEventListener("click", displayTableau);



