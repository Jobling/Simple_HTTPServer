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
        self.response.write(json.dumps(db.listDevices))

class deviceGetHandler(webapp2.RequestHandler, mac_address):
    def get(self):
        self.response.write(json.dumps(db.getDevice(mac_address)))        

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainPage),
    webapp2.Route(r'/devices', devicesListHandler),
    webapp2.Route(r'/devices/<mac_address:\d+>', deviceGetHandler)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()