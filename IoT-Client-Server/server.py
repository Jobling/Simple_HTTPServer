#!/usr/bin/python
# Imports
import socket
import sys

HOST = ''

def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()

def get_port(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 9000
    while port < 10000:
        try:
            s.bind((host, port))
            s.close()
            return port
        except:
            port += 1
            pass    
    print 'Did not find valid port between 9000 and 10000'
    sys.exit(1)

def get_address():
    global HOST
    hostname = ''
    HOST = get_host()
    port = get_port(hostname)
        
    return (hostname, port)
    
def main():
    # Get ip address and port
    server_address = get_address()
    
    # Create socket and bind address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Binding (external) address %s:%d" % (HOST, server_address[1])
    s.bind(server_address)
    
    s.listen(1)
    while(True):
        c, client_address = s.accept()
        message = "You, %s:%d, are connected to me, %s:%d. Welcome." % \
		(client_address[0], client_address[1], HOST, server_address[1])
        c.send(message)
        c.close()
        s.close()
        sys.exit(0)
        
if __name__ == '__main__':
    main()
