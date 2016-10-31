#!/usr/bin/python
import cherrypy

import random
import string

class StringGenerator(object):
	@cherrypy.expose
	def index(self):
		return """
		<html>
			<head></head>
			<body>
				<form method="get" action="generate">
					<input type="text" value="8" name="length" />
					<button type="submit">Give it now!</button>
				</form>
			</body>
		</html>
		"""

	@cherrypy.expose
	def generate(self, length=8):
		some_string = ''.join(random.sample(string.hexdigits, int(length)))
		cherrypy.session['my_string'] = some_string
		return some_string
		
	@cherrypy.expose
	def display(self):
		return cherrypy.session['my_string']

if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True
		}
	}
	cherrypy.quickstart(StringGenerator(), '/', conf)
