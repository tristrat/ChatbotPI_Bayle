var BTN = document.getElementById("button");
var TEXTAREA = document.getElementById("user-message");
var DIV = document.getElementById("chatbot-response");
var BTN_MIC = document.getElementById("bMic");
var BTN_SP = document.getElementById("bSpeak")
BTN.addEventListener("click", function () {
    var userQuery = TEXTAREA.value;
    sendQueryToServer(userQuery);
    TEXTAREA.value = '';
});

BTN_MIC.addEventListener("click", function () {
    speechToText();
});

BTN_SP.addEventListener("click", function () {
    textToSpeech(DIV.texte);
});

function sendQueryToServer(query) {
    var url_backend = "http://127.0.0.1:8000/analyse";
    fetch(url_backend, {
        method: "POST",
        body: JSON.stringify({ "texte": query }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            response.json()
                .then(data => {
                    console.log(data);
                    DIV.innerText = data.chatbot_response;
                })
        })
        .catch(e => {
            console.warn(e);
        });
}

function textToSpeech(texte){
    //lire sous format Audio  
    let utterance = new SpeechSynthesisUtterance(texte);
    speechSynthesis.speak(utterance); 
}

function speechToText() {
    recognition.start();
}

var recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US'; // Choisir la langue appropriée
recognition.maxAlternatives = 1;

recognition.onresult = function (event) {
    var message = event.results[0][0].transcript;
    console.log('Result received: ' + message + '.');
    console.log('Confidence: ' + event.results[0][0].confidence);

    TEXTAREA.value = message;
};
