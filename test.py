from __future__ import print_function

import tornado.ioloop
import tornado.web
from tornado import websocket
import os

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

class EchoWebSocketHandler(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        self.write_message("server: " + message);

    def on_close(self):
        print("WebSocket closed")


application = tornado.web.Application(
	[
    (r"/", MainHandler),
    (r"/ws", EchoWebSocketHandler),
  ],
  template_path=os.path.join(os.path.dirname(__file__), "frontend"),
  static_path=os.path.join(os.path.dirname(__file__), "static"),
  debug=True
)

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
