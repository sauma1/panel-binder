import os,time,threading
jo=input("setup atau run (s/r)\n>> ")
if 's' in jo:
    tok=input("masukkan token ngrok\n>> ")
    os.system('curl https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz')
    os.system('tar xfzv ngrok.tgz')
    os.system('chmod 777 ngrok')
    os.system(f"""echo 'authtoken: {tok}\\nversion: "2"\\nregion: ap' > ngrok.yml""")
    with open("bind.py", "w") as file:
     file.write(r'''exec("""\nimport hashlib\nimport pty\nimport select\nimport socket\nimport subprocess\nimport os\nimport sys\nHOST = '0.0.0.0'\nPORT = 6081  \n\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.bind((HOST, PORT))\ns.listen(1)\nset_password = sys.argv[1]\nwhile True:\n    conn, addr = s.accept()\n    print('Connected by', addr)\n    if set_password == "blank":\n       password = "blank"\n    else:\n       conn.send(b'Enter password: ')\n       password = conn.recv(1024).strip().decode()\n    if password == set_password:\n        master, slave = pty.openpty()\n        p = subprocess.Popen(["/bin/bash"], stdin=slave, stdout=slave, stderr=slave)\n        while True:\n            r, w, e = select.select([conn, master], [], [])\n            if conn in r:\n                data = conn.recv(1024)\n                if not data:\n                    break\n                os.write(master, data)\n            if master in r:\n                data = os.read(master, 1024)\n                if not data:\n                    break\n                conn.send(data)\n    else:\n        conn.send(b'Incorrect password\\n')\n    conn.close()\n""")''')
    print ("done")
else:
    sleep_thread = threading.Thread(target=lambda: os.system("nohup python3 bind.py blank > logbind.txt"))
    #os.system("nohup python3 bind.py blank > logbind.txt")
    sleep_thread.start()
    time.sleep(1)
    sleep_thread2 = threading.Thread(target=lambda: os.system("nohup ./ngrok tcp 6081 --config=ngrok.yml --log=stdout > ngrok_stat.txt"))
    sleep_thread2.start()
    #os.system("nohup ./ngrok tcp 6081 --config=ngrok.yml --log=stdout > ngrok_stat.txt")
    time.sleep(2)
    with open("ngrok_stat.txt", "r") as file:
     content = file.read()
    ksw=content.split("url=tcp://")[1].split(" ")[0]
    print (f"run: stty raw -echo;nc {ksw.split(':')[0]} {ksw.split(':')[1]}")