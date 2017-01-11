#!/usr/bin/python
import requests
import argparse
import socket
import sys
import os

def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        hostname = s.getsockname()[0]
    except:
        hostname = '127.0.0.1'
    finally:
        s.close()
        return hostname

class VNFClient():
    def __init__(self, controller_ip, controller_port, gateway):
        if controller_port is None: controller_port = 5000
        if gateway is None: gateway = get_host()
        self.url = 'http://%s:%d/networkService/v1.1/tenants/default/networks' % (controller_ip, controller_port)
        self.networks = {}
        self.gateway = gateway

    def createNetwork(self, name):
        # Generate Network PUT payload
        url = '%s/%s' % (self.url, name)
        if name in self.networks:
            print 'Network already exists with gateway %s.' % self.networks[name]['gateway']
            return

        network = {
            'network': {
                'gateway': self.gateway,
                'name': name
            }
        }
        
        response = requests.put(url, json=network)
        if response.status_code is not 200:
            print 'Could not create network.'
            print response
        else:
            self.networks[name] = {'gateway': self.gateway, 'attachments': []}
        
    def attachDevice(self, network, port, macAddress):
        url = '%s/%s/ports/%s/attachment' % (self.url, network, port)
        attachment = {
            'attachment': {
                'id': network,
                'mac': macAddress
            }
        }
        
        response = requests.put(url, json=attachment)
        if response.status_code is not 200:
            print 'Failed to create attachment on %s' % (port)
            print response
        else:
            self.networks[network]['attachments'].append({'port': port, 'mac': macAddress})

    def listNetworks(self):
        os.system('clear')
        for name, network in self.networks.iteritems():
            print 'Network: %s (with gateway %s)' % (name, network['gateway'])
            for attachment in network['attachments']:
                print '\t%s -- %s' % (attachment['port'], attachment['mac'])
        print ''

    def getNetworks(self):
        print requests.get(self.url).content

class SimpleMenu():
    def __init__(self, client):
        self.client = client
        self.running = 0
        self.menu_actions = {
            'main_menu': self.main_menu,
            '1': self.new_network,
            '2': self.new_device,
            '3': self.list_all,
            '4': self.get_from_server,
            '9': self.main_menu,
            '0': self.exit,
        }
        
    def start(self):
        self.running = 1
        self.main_menu()

    def main_menu(self):
        while self.running:
            os.system('clear')
            
            print "Welcome,\n"
            print "Please choose what you want to do:"
            print "1. Create Network"
            print "2. Add device to existing Network"
            print "3. List existing Networks"
            print "4. GET network information"
            print "\n0. Quit"
            choice = raw_input(">>  ")

            os.system('clear')
            ch = choice.lower()
            if ch == '':
                pass
            else:
                try:
                    self.menu_actions[ch]()
                except KeyError:
                    print "Invalid selection, please try again.\n"
        return
     
    # 1
    def new_network(self):
        os.system('clear')
        print "Please provide the following information."
        try:
            network = raw_input("Network Name >> ")
            raw_input("Press ENTER to confirm.")
            self.client.createNetwork(network)        
        except KeyboardInterrupt:
            print "Aborted."
        
        raw_input("Press ENTER to continue...")
        return
    
    # 2
    def new_device(self):
        os.system('clear')
        print "Please provide the following information."
        try:
            network = raw_input("Network Name >> ")
            port = raw_input("Port >> ")
            mac = raw_input("Mac Address >> ")
            raw_input("Press ENTER to confirm.")
            self.client.attachDevice(network, port, mac)
        except KeyboardInterrupt:
            print "Aborted."
        
        raw_input("Press ENTER to continue...")
        return
        
    # 3
    def list_all(self):
        os.system('clear')
        self.client.listNetworks()
        raw_input("Press ENTER to continue...")
        return

    # 4
    def get_from_server(self):
        os.system('clear')
        self.client.getNetworks()        
        raw_input("Press ENTER to continue...")
        return
     
    # Exit program
    def exit(self):
        self.running = 0
        return

if __name__ == '__main__':
    # Create parser
    parser = argparse.ArgumentParser(description = ' Test Virtual Network Filter REST API')
    parser.add_argument('-i', required=True, help='IP of the SDN controller. It is not verified on runtime.')
    parser.add_argument('-p', required=False, help='Port of REST API on SDN Controller. Default: 5000.', default=None, type=int)
    parser.add_argument('-n', required=False, help='Mininet NAT private ip address.', default=None)

    # Generate Virtual Network Filter URL for TestNetwork
    args = parser.parse_args()
    client = VNFClient(args.i, args.p, args.n)
    menu = SimpleMenu(client)
    menu.start()
    
    



