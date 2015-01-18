$(function() {
  var ws = new WebSocket("ws://localhost:8888/ws");
  var parse_msg = function(s) { return s.split(":"); }

  ws.onmessage = function(msg) {
    if (msg.data.indexOf("result") == 0) {
      var result = msg.data.split(":")[1];
      $( '#intro-message' ).addClass("hidden");
      $( '#won_message' ).toggleClass("hidden", result != "won");
      $( '#lost_message' ).toggleClass("hidden", result != "lost");
      $( '#tie_message' ).toggleClass("hidden", result != "tie");
      $( '#waiting_message' ).addClass("hidden");
      $( '#choices ' ).removeClass("hidden");
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

      $( '#waiting_message' ).removeClass("hidden");
      $( '#choices ' ).addClass("hidden");
    });
  });
});
