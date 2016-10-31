#!/usr/bin/python
import cherrypy

import random
import string

class StringGenerator(object):
	@cherrypy.expose
	def index(self):
		return "Hello World!"

	@cherrypy.expose
	def generate(self, length=8):
		return ''.join(random.sample(string.hexdigits, int(length)))

if __name__ == '__main__':
	cherrypy.quickstart(StringGenerator())
