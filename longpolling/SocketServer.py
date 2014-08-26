import tornado
import tornado.web
import tornado.websocket
import psycopg2
from psycopg2.extras import *
import time
import json
import tornado.concurrent

conn = psycopg2.connect("dbname=<database> user=<user> password=<password> host=<host>")

@tornado.gen.coroutine
def async_sleep(timeout):
    """ Sleep without blocking the IOLoop. """
    yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + timeout)

class PushServer(tornado.web.RequestHandler):

	@tornado.gen.coroutine
	def get(self,input=None):
		print "into callback"
		yield async_sleep(10)		
		data = self.getData();
		js = json.dumps(data)
		self.write(js)
		self.finish()
		
	def getData(self):
		sql = "select source , count(*) from table group by source"
		curr = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		curr.execute(sql)
		data = curr.fetchall()		
		return data

class Main(tornado.web.RequestHandler):
	def get(self):
		sql = "select source , count(*) from cs_options_property group by source"
		self.render('index.html')
		
		
# this calls on message once in a while

application = tornado.web.Application([
	(r'/',Main),
	(r'/pull',PushServer)
])

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()