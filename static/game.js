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

    $.each( $( ".choice" ), function(_, raw_elem) {
      var elem = $(raw_elem);
      elem.click( function() {
        ws.send(elem.data('item'));
      });
    });
});
