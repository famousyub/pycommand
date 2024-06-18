import socket
import sys
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []
host = ''
port = 23
chat = ""
print("\n"*50)

def threaded_client(conn):
    global chat
    
    conn.send(str.encode("Welcome to Telnet chat! Windows Only\n"))
    conn.send(str.encode(chat+"\n"))
    sentex = ""
    msgc = len(clients)
    
    while 1:
        try:
            data = conn.recv(2048)
            #print(data)
        except:
            print(data)
        try:
            reply = data.decode("utf-8")
        except:
            print("Device tried connect with incompatible codec (non-utf8)!")
            conn.send(str.encode("This Device tried connect with incompatible codec (non-utf8)!\n"))
            reply = ""
            conn.close()
            clients.remove(conn)
            break
        if not data:
            break
        if data != b'\r\n':
            sentex = sentex + reply
        else:
            if sentex == "":
                sentex = reply
            if sentex == "/help":
                conn.sendall(str.encode("/help - list all commands\n/info - server information and status\n/list - lists all clients connected\n"))
            elif sentex == "/info":
                for i in clients:
                    if i is not s:
                        msgc = msgc +1
                conn.sendall(str.encode(str(msgc)+" clients online!"))
            elif sentex == "/list":
                conn.send(str.encode(str(clients)+"\n"))
                        
            else:
                for i in clients:
                    if i is not s:
                        #print(clients)
                        try:
                            i.sendall(str.encode(sentex))
                            i.sendall(str.encode("\n"))
                            msgc = msgc +1
                        except:
                            clients.remove(i)
                            print("Removed the client: "+str(i))
                            msgc = msgc - 1
                chat = chat+sentex+"\n"
                print("Sent a message to "+str(msgc)+" clients!")
            msgc = 0
            print(sentex+"\n")
            sentex = ""
    conn.close()

    
while 1:
    print("\nTelnet Chat Room! " +host+":"+str(port))
    if 1:
        while 1:
            try:
                s.bind((host, port))
            except socket.error as e:
                print(str(e))
            s.listen(5)
            print("Waiting for new connections...\n")
            
            conn, addr = s.accept()
            print(addr[0]+":"+str(addr[1])+" Connected!")
            clients.append(conn)
            start_new_thread(threaded_client,(conn,))