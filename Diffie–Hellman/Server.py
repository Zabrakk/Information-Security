import socket

prime = 23
base = 5
secret = 15
final = False

def D_H(base, secret):
    return str(int(base) ** secret % prime)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 6669))
server.listen(2)

while not final:
    connec, addr = server.accept()
    print("Connected from " + str(addr) + "\n")
    
    other = connec.recv(1024).decode()

    print("Sending: " + D_H(base, secret))
    connec.send(D_H(base, secret).encode())
    print("Recieved: " + other + "\n")

    print("Sending: " + D_H(other, secret))
    connec.send(D_H(other, secret).encode())
    final = connec.recv(1024).decode()
    
print("Recieved: " + final + "\n")
server.close()
