#!/usr/bin/python
# Imports
import webapp2
from webapp2_extras import routes
from paste import httpserver

import socket
import database
import json
import requests
import sys

# Global variables
db = database.database('devices')
HOST = '127.0.0.1'
PORT = '8080'

CONTROLLER_IP = '127.0.0.1'
CONTROLLER_PORT = '5000'

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Server is up!')

class devicesListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(200)
        self.response.write(json.dumps(db.listDevices()))

class deviceGetHandler(webapp2.RequestHandler):
    def get(self, mac_address):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(200)
        self.response.write(json.dumps(db.getDevice(mac_address)))

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainPage),
    webapp2.Route(r'/devices', devicesListHandler),
    webapp2.Route(r'/devices/<mac_address>', deviceGetHandler),
    ], debug=True)

def get_port():
    global PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    while port < 9000:
        try:
            s.bind((HOST, port))
            s.close()
            PORT = str(port)
            return True
        except:
            port += 1
            pass
    return False

def notify_Controller():
    URL = "http://%s:%s/wm/mactracker/servers" % (CONTROLLER_IP, CONTROLLER_PORT)
    payload = {'hostname': HOST, 'port': PORT}

    response = requests.put(URL, json=payload)
    print response.content
    
def main():
    if not get_port():
        print 'Could not find suitable port between 8080 and 9000. Exiting.'
        sys.exit()
    
    notify_Controller()
    httpserver.serve(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()
