import device
import server
import pickle

class database(object):
    def __init__(self, name):
        self.name = name
        try:
            f = open('db_' + name, 'rb')
            self.db = pickle.load(f)
            f.close()
        except IOError:
            self.db = {}

    def addDevice(self, mac, server_ip, server_port):
        if mac not in self.db:
            self.db[mac] = device.device(mac, server.server(server_ip, server_port))
        else:
            print 'Device with same MAC address already exists.'

        f = open('db_' + self.name, 'wb')
        pickle.dump(self.db, f)
        f.close()

    def getDevice(self, mac):
        device = self.db.get(mac, None)
        if device is not None:
            return {'mac': device.mac,
                    'server_ip': device.server.ip,
                    'server_port': device.server.port}
        else:
            return {}
        pass

    def getNetwork(self, server):
        ret = set()
        for mac, device in self.db.iteritems():
            if device.server == server:
                ret.add(mac)
            else:
                pass
        return ret

    def listDevices(self):
    	ret = {}
    	for mac, device in self.db.iteritems():
    		ret[mac] = str(device)
            return ret
