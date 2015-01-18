from __future__ import print_function

import tornado.ioloop
import tornado.web
from tornado import websocket
import os
import random

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

def get_user(uid):
  return WebSocketHandler.users[uid]

class WebSocketHandler(websocket.WebSocketHandler):
  users = {}

  def open(self):
    uid = self.get_cookie("uid")
    if uid is None:
      uid = str(random.randint(0, 100000))
      self.write_message("uid:" + uid)
    print("WebSocket opened for " + uid)
    WebSocketHandler.users[uid] = self

  def on_message(self, message):
    print(message)
    self.write_message("server: " + message)

  def on_close(self):
    for uid, user in WebSocketHandler.users.iteritems():
      if user == self:
        del WebSocketHandler.users[uid]
      print("WebSocket closed for " + uid)
      return

class TurnHandler(tornado.web.RequestHandler):
  last_player = None
  last_move = None

  def get_current_uid(self):
    return self.get_cookie("uid")

  def wins(self, move):
    item_beats = {
      'rock' : ['scissors'],
      'paper' : ['rock'],
      'scissors' : ['paper'],
    }

    return TurnHandler.last_move in item_beats[move]

  def post(self, move):
    if move not in {"rock", "paper", "scissors"}:
      raise tornado.web.HTTPError(400)

    me = self.get_current_uid()

    print("user {} made move {}".format(me, move))
    if TurnHandler.last_move is None:
      TurnHandler.last_move, TurnHandler.last_player = move, me
      return
    
    if self.wins(move):
      winner, loser = me, TurnHandler.last_player
    else:
      winner, loser = TurnHandler.last_player, me

    TurnHandler.last_player = None
    TurnHandler.last_move = None

    print("winner: {} loser: {}".format(winner, loser))

    get_user(winner).write_message("result:won")
    get_user(loser).write_message("result:lost")

application = tornado.web.Application(
	[
    (r"/", MainHandler),
    (r"/ws", WebSocketHandler),
    (r"/rpc/turn/([^/]+)", TurnHandler), 
  ],
  template_path=os.path.join(os.path.dirname(__file__), "frontend"),
  static_path=os.path.join(os.path.dirname(__file__), "static"),
  debug=True
)

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
