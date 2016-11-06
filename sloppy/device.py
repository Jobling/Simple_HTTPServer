class device(object):
    def __init__(self, mac, server, application=None, company=None):
        self.mac = mac
        self.server = server
        self.application = application
        self.company = company

    def __str__(self):
        return 'Device %s connects to server %s.' % (self.mac, self.server)
