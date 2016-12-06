#!/usr/bin/python

import device
import server
import pickle

MAC_ADDRESS_LENGTH = 12

class database(object):
    def __init__(self, name):
        self.name = name
        try:
            f = open('db_' + name, 'rb')
            self.db = pickle.load(f)
            f.close()
        except IOError:
            self.db = {}

    def addDevice(self, mac_address, server_ip, server_port):
        mac = mac_address.translate(None, "-: ").lower()
        if mac not in self.db:
            if len(mac) == MAC_ADDRESS_LENGTH:
                self.db[mac] = device.device(mac, server.server(server_ip, server_port))
            else:
                print 'Wrong mac address size.'
        else:
            print 'Device with same MAC address already exists.'

        f = open('db_' + self.name, 'wb')
        pickle.dump(self.db, f)
        f.close()

    def getDevice(self, mac_address):
        mac = mac_address.translate(None, "-: ").lower()
        device = self.db.get(mac, None)
        if device is not None:
            return {'mac': device.mac,
                    'server_ip': device.server.ip,
                    'server_port': device.server.port}
        else:
            return {}
        pass

    def listDevices(self):
        ret = {}
        for mac, device in self.db.iteritems():
            ret[mac] = str(device)
        return ret

