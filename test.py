import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

application = tornado.web.Application(
	[
    (r"/", MainHandler),
  ],
  template_path=os.path.join(os.path.dirname(__file__), "frontend"),
  static_path=os.path.join(os.path.dirname(__file__), "static"),
  debug=True
)

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()