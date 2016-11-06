import device
import pickle

class database(object):
    def __init__(self, name):
        self.name = name
        try:
            f = open('bd_' + name, 'rb')
            self.db = pickle.load(f)
            f.close()
        except IOError:
            self.db = {}

    def addDevice(self, mac, server, application=None, company=None):
        if mac not in self.db:
            self.db[mac] = device.device(mac, server, application, company)
        else:
            print 'Device with same MAC address already exists.'

        f = open('bd_' + name, 'wb')
        pickle.dump(self.db, f)
        f.close()

    def getDevice(self, mac):
        device = self.db.get(mac, None)
        if device is not None:
            return {'mac': device.mac,
                    'server': device.server,
                    'application': device.application,
                    'company': device.company}
        else:
            return {}
        pass

    def listDevices(self):
        return self.db
