import tornado.web
import tornado.websocket
import tornado.ioloop

# could be redis
connections = []

# could be database 
msgs = []

class ChatServer(tornado.websocket.WebSocketHandler):

	def open(self):
		print "client connected"
		connections.append(self)

	def on_message(self,msg):
		msgs.append(msg)
		for connection in connections:
			connection.write_message(msg)

	def on_close(self):
		connections.remove(self)


class HomePage(tornado.web.RequestHandler):

	def get(self):
		self.getChatTemplate()

	def post(self):
		self.getChatTemplate()

	def getChatTemplate(self):
		self.render("chat.html",msgs=msgs)


urls = [('/',HomePage),('/chat',ChatServer)]

application = tornado.web.Application(
                                handlers=urls,
                                debug=True
                           )

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
	
