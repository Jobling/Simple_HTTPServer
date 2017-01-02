#!/usr/bin/python
# Imports
import argparse
import socket
import sys

def main():
    parser = argparse.ArgumentParser(prog='IoT Client')
    parser.add_argument('-i', '--ip', default='127.0.0.1', help='IoT server remote ip address.')
    parser.add_argument('-p', '--port', type=int, default=9000, help='IoT server remote port.')
    args = parser.parse_args()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostbyname(args.ip)
    server_port = args.port
    server_address = (server_ip, server_port)
    
    try:
        s.connect(server_address)
	message = s.recv(256)
	print message
    finally:
        s.close()
        
    sys.exit(0)

if __name__ == '__main__':
    main()

