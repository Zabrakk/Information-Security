import socket
import string

prime = 23
base = 5
secret = 6
final = False

def D_H(base, secret):
    return str(int(base) ** secret % prime)

address = ('localhost', 6669)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

while not final:
    print("Sending: " + D_H(base, secret))
    client.sendto(D_H(base, secret).encode(), address)
    
    other = client.recv(1024).decode()
    print("Recieved: " + other + "\n")

    print("Sending: " + D_H(other, secret))
    client.sendto((D_H(other, secret)).encode(), address)
    final = client.recv(1024).decode()


print("Recieved: " + final + "\n")
client.close()
