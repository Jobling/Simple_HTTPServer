class server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return '%s:%s' % (self.ip, self.port)
