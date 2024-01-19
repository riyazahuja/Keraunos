"""
A simple Python script to act as a server over Bluetooth using
Python sockets with Python 3.3 or above.
"""

import socket
import json

hostMACAddress = '5C:E9:1E:90:AA:3C'  # The MAC address of the server's Bluetooth adapter
port = 3  # Arbitrary choice, must be within valid RFCOMM port range (1-30)

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress, port))
s.listen(1)

try:
    client, address = s.accept()
    print(f"Accepted connection from {address}")
    while True:
        data = json.dumps({'Content': "Hello!"})
        client.send(data.encode('utf-8'))
        print("Sent data")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
    s.close()
