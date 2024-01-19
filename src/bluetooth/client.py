"""
A simple Python script to act as a client over Bluetooth using
Python sockets with Python 3.3 or above.
"""

import socket
import json

serverMACAddress = '5C:E9:1E:90:AA:3C'  # The MAC address of the server's Bluetooth adapter
port = 3  # The server's port number

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))

try:
    while True:
        data = s.recv(1024)
        if data:
            print(f"Received: {data.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
