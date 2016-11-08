import webapp2
from webapp2_extras import routes

import database
import json

db = database.database('devices')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Server is up!')

class devicesListHandler(webapp2.RequestHandler):
    def get(self):
	self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(db.listDevices()))

class deviceGetHandler(webapp2.RequestHandler):
    def get(self, mac_address):
	self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(db.getDevice(mac_address)))

'''
class networkListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(db.listDevices()))

class networkGetHandler(webapp2.RequestHandler):
    def get(self, server_ip, server_port):
        self.response.write(json.dumps(db.getDevice(mac_address)))
'''

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainPage),
    webapp2.Route(r'/devices', devicesListHandler),
    webapp2.Route(r'/devices/<mac_address>', deviceGetHandler),
    #webapp2.Route(r'/networks', networkListHandler),
    #webapp2.Route(r'/networks/<server_ip>/<server_port>', networkGetHandler)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
