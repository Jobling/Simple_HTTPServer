class device(object):
    def __init__(self, mac, server):
        self.mac = mac
        self.server = server

    def __str__(self):
        return 'Device %s connects to server %s.' % (self.mac, self.server)
