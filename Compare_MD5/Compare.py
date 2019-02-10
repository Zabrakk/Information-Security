import string
import random
import hashlib
import sys

symbol_list = []
used = []
data = []
def create_list():
    """Creates a list that includes character a-z and number 0-9"""
    
    for i in range(26):
        symbol_list.append(string.ascii_lowercase[i])
        #symbol_list.append(string.ascii_lowercase[i].upper())
    for i in range(10):
        symbol_list.append(str(i))

def create_passwd():
    """Creates possible passwords (4-9 symbols long) from the symbols in symbol list. All of the created passwords
    are saved in used array so we won't waste time checking them again."""

    passwd = ""
    symbols = random.randint(4,5)
    while True:
        for o in range(symbols):
            if passwd in used:
                continue
            else:
                passwd += symbol_list[random.randint(0, len(symbol_list) - 1)]     
        used.append(passwd)
        return passwd

def toMd5(salasana):
    """Turns the created passwords in to md5 hashes"""
    
    m = hashlib.md5()
    m.update(salasana.encode('utf-8'))
    return m.hexdigest()

def open_file(file):
    """Opens the file that includes md5 hashes and user names."""
    
    try:
       with open(file) as source:
           data = source.readlines()
           return data
    except IOError:
        print("File does not excist")

def split_user_pass(file):
    data = open_file(file)
    for i, line in enumerate(data):
        data[i] = line.split(":")
    return data

def success(user, passwd):
    """Saves the found passwords and usernames into a new file."""
 
    try:
       f = open("succeess.txt", 'a')
       f.write(user + " " + passwd + "\n")
    except IOError:
        print("File does not excist")

def compare(file):
    """Compares the created hashes to the hashes included in the file."""

    data = split_user_pass(file)
    while True:
        passwd = create_passwd()
        hashed = toMd5(passwd)
        for line in data:
            user = line[0]
            if hashed == line[1].strip():
                print(user, passwd)
                success(user, passwd)

create_list() 
compare(sys.argv[1])
