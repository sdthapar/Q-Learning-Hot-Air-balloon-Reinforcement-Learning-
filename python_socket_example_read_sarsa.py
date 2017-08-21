""" Python Example for reading (s, a, r, s') information from the game 
through the socket"""

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 24383)
sock.connect(server_address) # connect 

while True:
    d = sock.recv(1024).strip()
    if not d: 
    	break
    print "received data:", d
    old_state, action, reward, new_state = d.split(",")
    reward = float(reward)
    print "old_state", old_state
    print "action", action
    print "reward", reward
    print "new_state", new_state

