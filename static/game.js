function log(text) {
  console.log(text);
}

$(function() {
  var ws = new WebSocket("ws://localhost:8888/ws");
  ws.onmessage = function(msg) {
    if (msg.indexOf("result") == 0) {
      var won = msg.indexOf("won") != -1;
      $( '#intro-message' ).addClass("hidden");
      $( '#won_message' ).toggleClass("hidden", !won);
      $( '#lost_message' ).toggleClass("hidden", won);
    }
    if (msg.data.indexOf("uid:") === 0) {
        var uid = msg.data.slice(4);
        document.cookie = "uid=" + uid;
    }
    console.log("client: " + msg);
  };

  ws.onopen = function() {
    ws.send("hello server");
  };

  $.each( $( ".choice" ), function(_, raw_elem) {
    var elem = $(raw_elem);
    elem.click( function() {
      $.post('http://localhost:8888/rpc/turn/' +
              elem.data('item'));
    });
  });
});
