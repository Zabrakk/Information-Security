import socket
import random
import string
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Key:
	def __init__(self):
		self.COMMANDS = {"keyPair": self.keyPair, "auth": self.auth, "end": self.end}
		self.MAC_addr = self.MAC_gen() #b'9C:74:38:8D:AD:8C' #Banning test value
		self.HOST = 'localhost'
		self.MASTER = 60000
		self.END = False
		self.priv = 0
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.connect((self.HOST, self.MASTER))
		self.socket.send(self.MAC_addr)
		threading.Thread(target = self.get_command).start()
		
	def get_command(self):
		'''Resieve command from server'''
		while not self.END:
			comm = self.socket.recv(1024).decode("utf-8")
			try:
				self.COMMANDS[comm]()
			except:
				print("#: Unkown command")
				
	def MAC_gen(self):
		'''Generate a MAC address for the device'''
		MAC = ""
		for i in range(6):
			opt = random.randint(0,3)
			if opt == 0: #Digit, char
				MAC += "".join([random.choice(string.digits), random.choice(string.ascii_uppercase[0:6])])
			elif opt == 1: #Digit, digit
				MAC += "".join([random.choice(string.digits), random.choice(string.digits)])
			elif opt == 2: #Char, digit
				MAC += "".join([random.choice(string.ascii_uppercase[0:6]), random.choice(string.ascii_uppercase[0:6])])
			else: #Char, char
				MAC += "".join([random.choice(string.ascii_uppercase[0:6]), random.choice(string.ascii_uppercase[0:6])])
			MAC += ":"
		return(MAC[0:-1].encode("utf-8"))
		
	def keyPair(self):
		'''Public/Private key pair creation with server. User must accept'''
		opt = input("#: Accept key pair creation? y/n: ")
		if opt == "y":
			self.key = RSA.generate(2048)
			self.pub = self.key.publickey().exportKey("PEM")
			self.socket.send(self.pub)
			self.decrypter = PKCS1_OAEP.new(self.key)
		else:
			self.socket.send("no".encode("utf-8"))
			
	def auth(self):
		'''Authentication with Diffie-Hellman'''
		nums = self.socket.recv(1024)
		nums = self.decrypter.decrypt(nums).decode("utf-8").split("#")
		answer = int(nums[0]) + int(nums[1]) + 1
		self.socket.send(str(answer).encode("utf-8"))
		answer = self.socket.recv(1024).decode("utf-8")
		if answer == "success":
			print("#: Authenticated")
		else:
			print("#: Authentication failed")		

	def end(self):
		'''Close Client'''
		self.socket.close()
		self.END = True
		print("#: Closing")
	
key = Key()
