import time
import math
import random
import string

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import *
import threading
import socket

CLIENTS = []
BANNED = [] #"9C:74:38:8D:AD:8C"

class Server:
	def __init__(self):
		self.connections = 0
		self.COMMANDS = {"keyPair": self.keyPair, "auth": self.auth, "closeConn": self.closeConn, "banAddr": self.banAddr, "end": self.end}
		self.END = False
		
		self.PORT = 60000
		self.HOST = 'localhost'
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.HOST, self.PORT))
		
		print("#: Commands: keyPair, auth, closeConn, banAddr, end")
		threading.Thread(target = self.control_client).start()
		self.listener()
		
	def listener(self):
		self.server.listen(10)
		while not self.END:
			try:
				self.conn, self.addr = self.server.accept()
				self.connections += 1
				print("#: Client connected")
				client = cClient(self.conn, self.addr)
				CLIENTS.append(client)
			except:
				pass
		
	def control_client(self):
		while not self.END:
			opt = input()
			try:
				self.COMMANDS[opt]()
			except Exception as E:
				print(E)
				print("#: Unkown command")
				
	def keyPair(self):
		client = self.get_client()
		client.keyPair()
		
	def auth(self):
		client = self.get_client()
		client.auth()
	
	def closeConn(self):
		client = self.get_client()
		client.end()
	
	def banAddr(self):
		'''Allow the server to ban MAC addresses'''
		print("#: Example addres: 9C:74:38:8D:AD:8C")
		addr = input("#: Enter address to ban: ")
		correct = 0
		
		#Check addr validity
		for char in addr.replace(":", ""):
			if char in string.ascii_uppercase[0:6] or char in string.digits:
				correct += 1
			else:
				correct -= 1
		if correct == 12:
			BANNED.append(addr)
			print("#: Address banned")
		else:
			print("#: Invalid address")
	
	def end(self):
		self.END = True
		for client in CLIENTS:
			client.end()
		self.server.close()

	def get_client(self):
		id = input("#: Enter client id: ")
		try:
			return CLIENTS[int(id) - 1]
		except:
			print("Not a valid option")
		
class cClient: #controlClient
	def __init__(self, conn, addr):
		self.END = False
		self.connection, self.addr = conn, addr
		
		self.MAC_addr = self.connection.recv(1024).decode("utf-8")
		print("#: Device MAC address: " + self.MAC_addr)
		if self.MAC_addr in BANNED:
			print("#: Client is banned")
			self.end()
		self.pub = "0"
	
	def keyPair(self):
		self.connection.send("keyPair".encode("utf-8"))
		self.pub = self.connection.recv(2048)
		if self.pub.decode("utf-8") == "no":
			print("#: User declined")
			return
		#RSA
		self.pub = RSA.importKey(self.pub)
		self.pub = PKCS1_OAEP.new(self.pub)
		print("#: Key pair created")
	
	def auth(self):
		'''Authenticate device, failure causes the client to be banned'''
		try:
			if self.pub == "0":
				print("#: Create keys first")
				return
		except: 
			pass
		
		test = self.pub.encrypt("8#3".encode())
		self.connection.send("auth".encode("utf-8"))
		self.connection.send(test)
		correct = 8+3
		if int(self.connection.recv(1024).decode("utf-8")) == correct:
			self.connection.send("success".encode("utf-8"))
			print("#: Authenticated")
		else:
			self.connection.send("failed".encode("utf-8"))
			print("#: Authentication failed, banning client")
			BANNED.append(self.MAC_addr)
			print(BANNED)
			self.end()
	
	def end(self):
		self.connection.send("end".encode("utf-8"))
		self.END = True
		print("#: Client closing")

server = Server()		
