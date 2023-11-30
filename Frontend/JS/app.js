var BTN=document.querySelector("button")
var TFXTARFA=document.querySelector("textarea")
var DIV=document.querySelector("#reponsr_msg")

//EVENEMENT
BTN.addEventListener("click", chatBot)

//Fonction principale
function chatBot(){
    let text=TEXTAREA.value

    //je dois communiquer avec le backend
    var url_backend="http://127.0.0.1:8000/analyse"
    fetch(url_backend,
        {
            method: "post",
            body: JSON.stringify({"texte":text}),
            accept: 'application/json'
        })
        .then(response =>{
            response.json()
            .then(data=>{
                console.log(data)
            })
        })

}
