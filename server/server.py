import socket
import os 
import pickle

#Establishing connection through TCP
ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssFT.bind((socket.gethostname(), 8757))
ssFT.listen(1)
l = os.listdir("./Audiobook"); 
print("Server started.... Waiting for connection")

while True:
    (conn, address) = ssFT.accept()
    data=pickle.dumps(l)
    conn.send(data)
    for f in l:
        with open('./Audiobook/{}'.format(f), 'rb') as fa:
            print('Opened file.')
            fa.seek(0, 0)
            print("Sending file.")
            while True:
                data = fa.read(2048)
                conn.send(data)
                if not data:
                    conn.send(b"EOF")
                    break
            fa.close()
            print("File Sent..")
    conn.close()
    print("Connection closed.")