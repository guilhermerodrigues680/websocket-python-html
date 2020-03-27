var PLAY_WITH_DOCKER = true;
var websocketUrl;

if (PLAY_WITH_DOCKER) { // Ex url: http://ip172-18-0-6-bpv591jcktm0008lvju0-8080.direct.labs.play-with-docker.com/
    const url = window.location.host;
    const hostWithPortWebsocket = url.replace(8080, 6789);
    websocketUrl = "ws://" + hostWithPortWebsocket; // PLAY WITH DOCKER
} else {
    websocketUrl = 'ws://127.0.0.1:6789/'; // DEFAULT 
}

console.info("Websocket Url: ",websocketUrl);
var websocket = new WebSocket(websocketUrl);

$( document ).ready(function() {
    $('#btn-reconectar').hide();
});

$('.minus').click(function () {
    websocket.send(JSON.stringify({ action: 'minus' }));
});

$('.plus').click(function () {
    websocket.send(JSON.stringify({ action: 'plus' }));
});

$('#btn-reconectar').click(function (params) {
    location.reload(true);
});

websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case 'state':
            $('.value').text(data.value);
            break;
        case 'users':
            $('.users').text(`${data.count.toString()} user${data.count == 1 ? "" : "s"} online`);
            break;
        default:
            console.error("unsupported event", data);
    }
};

websocket.onopen = function (event) {
    console.log("Websocker conectado!")
};

websocket.onclose = function (event) {
    $('.users').text("Sem conexão...")
    $('#btn-reconectar').show();
};
