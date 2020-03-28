var websocketUrl;

// PLAY_WITH_DOCKER é definida no arquivo 'config.js'
if (PLAY_WITH_DOCKER) { // Ex url: http://ip172-18-0-6-bpv591jcktm0008lvju0-8080.direct.labs.play-with-docker.com/
    const url = window.location.host;
    let hostWithPortWebsocket = url.replace(8080, 6789);
    hostWithPortWebsocket += window.location.pathname.replace('.html', '') + '/'
    websocketUrl = "ws://" + hostWithPortWebsocket; // PLAY WITH DOCKER
} else {
    websocketUrl = 'ws://127.0.0.1:6789/text-transmission-submit/'; // DEFAULT 
}

console.info("Websocket Url: ",websocketUrl);
var websocket = new WebSocket(websocketUrl);

$(document).ready(function(){
    $("textarea").keyup(function(){
        const texto = $("textarea").val();
        websocket.send(JSON.stringify({ msg: texto }));
    });
});

websocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    switch (data.type) {
        case 'users':
            $('#users-count').text(`Usuários: ${data.count}`);
            break;
    }
};

websocket.onopen = function (event) {
    console.log("Websocker conectado!");
};