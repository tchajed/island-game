function log(text) {
  console.log(text);
}

$(function() {
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onmessage = function(msg) {
        console.log("client: " + msg);
    };
    ws.onopen = function() {
        ws.send("hello server");
    };
});
