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

class TurnResult(object):
  Win, Tie, Lose = "win", "tie", "lose"

class TurnHandler(tornado.web.RequestHandler):
  last_player = None
  last_move = None

  def get_current_uid(self):
    return self.get_cookie("uid")

  @classmethod
  def result(cls, last_move, move):
    if move == last_move:
      return TurnResult.Tie

    item_beats = {
      'rock' : ['scissors'],
      'paper' : ['rock'],
      'scissors' : ['paper'],
    }

    if last_move in item_beats[move]:
      return TurnResult.Win
    return TurnResult.Lose

  def post(self, move):
    if move not in {"rock", "paper", "scissors"}:
      raise tornado.web.HTTPError(400)

    me = self.get_current_uid()
    print("user {} made move {}".format(me, move))

    if TurnHandler.last_player == me:
      # change your move
      TurnHandler.last_move = move
      return

    if TurnHandler.last_move is None:
      TurnHandler.last_move, TurnHandler.last_player = move, me
      return
    
    last_move = TurnHandler.last_move
    last_player = TurnHandler.last_player
    TurnHandler.last_player = None
    TurnHandler.last_move = None

    result = TurnHandler.result(last_move, move)
    if result == TurnResult.Tie:
      get_user(last_player).write_message("result:tie")
      get_user(me).write_message("result:tie")
      return

    if result == TurnResult.Win:
      winner, loser = me, last_player
    if result == TurnResult.Lose:
      winner, loser = last_player, me

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
  port = int(os.environ.get("PORT", 8888))
  application.listen(port)
  tornado.ioloop.IOLoop.instance().start()
