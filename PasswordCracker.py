# Make a class that accepts the input and some settings to try and create an output that it returns
#Have it return NULL if it fails

# Testing using input from terminal
from Decryptionizer import *
import time # for time tracking
import hashlib # for the hashing

#functions
# ecryption is a string of the name of encryption wanted
# returns the hexidecimal output of the hashes
def encrypt(string, encryption):
	if (encryption == 'none'):
		return string
	elif (encryption == 'sha224'): #sha224
		return hashlib.sha224(bytes(string, encoding = 'utf8')).hexdigest()
	elif (encryption == 'sha256'): #sha256
		return hashlib.sha256(bytes(string, encoding = 'utf8')).hexdigest()
	elif (encryption == 'sha384'): #sha384
		return hashlib.sha384(bytes(string, encoding = 'utf8')).hexdigest()
	elif (encryption == 'sha512'): #sha512
		return hashlib.sha512(bytes(string, encoding = 'utf8')).hexdigest()
	elif (encryption == 'md5'): #md5
		return hashlib.md5(bytes(string, encoding = 'utf8')).hexdigest()
	else: # defaults to returning it unecrypted if encryption isn't known
		return string
		# could add a debug thing so it says it couldn't encrypt it
		
def addEncryption(name, decrypter):
	if (name.lower() == 'none'):
		self.validEncryptions.append('none')
	# RSA
	# SHA224
	elif (name.lower() == 'sha224'):
		decrypter.addEncryptionToList('sha224')
	# SHA256
	elif (name.lower() == 'sha256'):
		decrypter.addEncryptionToList('sha256')
	# SHA384
	elif (name.lower() == 'sha384'):
		decrypter.addEncryptionToList('sha384')
	# SHA512
	elif (name.lower() == 'sha512'):
		decrypter.addEncryptionToList('sha512')
	# MD5
	elif (name.lower() == 'md5'):
		decrypter.addEncryptionToList('md5')
	#else:
		# adds nothing
		

#Input variables
userInput = input('Encrypted input - 1\nTesting - 2\n')
userInput2 = ''
encryptedInput = ''
minimum = 1
maximum = 100
#Asks for type of input
while (userInput != '1' and userInput != '2'):
	userInput = input('Encrypted input - 1\nTesting - 2\n')

if (userInput == '1'):
	userInput = input('Insert string: ')
else:
	userInput = input('Insert plain text string: ')
	userInput2 = input('Insert encryption: ')
	while (userInput2 != 'sha224' and userInput2 != 'sha256' and userInput2 != 'sha384' and userInput2 != 'sha512' and userInput2 != 'md5'):
		print("Enter sha224 or sha256 or sha384 or sha512 or md5\n")
		userInput2 = input('Insert encryption: ')

encryptedInput = encrypt(userInput, userInput2)

#Gets minimum length to test
minimum = int(input('Minimum characters: '))
if (minimum <= 0):
 	minimum = 1
 
#Gets maximum length to test
maximum = int(input('Maximum characters: '))
if (maximum < 1):
	maximum = 1

decrypter = Decryptionizer(minimum, maximum) # makes decrypter
 
# adds encryptions to check with
userInput2 = input('Insert encryption or STOP: ')
while (userInput2 != 'STOP'):
	if (userInput2 != 'sha224' and userInput2 != 'sha256' and userInput2 != 'sha384' and userInput2 != 'sha512' and userInput2 != 'md5'):
			print("Enter sha224 or sha256 or sha384 or sha512 or md5 or all\n")
			userInput2 = input('Insert encryption or STOP: ')
	else:
		addEncryption(userInput2, decrypter)
		print("Encryption added.\n")
		userInput2 = input('Insert encryption or STOP: ')

# adds validCharacters to check with
userInput2 = input('Insert characters to use or STOP: ')
while (userInput2 != 'STOP'):
	if (userInput2 != 'lowercase letters' and userInput2 != 'numbers' and userInput2 != 'uppercase letters' and userInput2 != 'special characters' and userInput2 != 'all'):
			print("Enter numbers, lowercase letters, uppercase letters, special characters, or all\n")
			userInput2 = input('Insert characters to use or STOP: ')
	else:
		decrypter.addPresetList(userInput2)
		print("Characters added.\n")
		userInput2 = input('Insert characters to use or STOP: ')

# add the common passwords
f = open('CommonPasswords.txt', 'r') # opens the file
lines = f.readlines()
lineNum = 0
for line in lines:
	line = line.replace("\n", "")
	decrypter.addCommonPassword(line)
f.close()

startTime = time.time()
temp = decrypter.generateGuess()
temp2 = 0 # tracks number of attempts
while (encryptedInput != temp and temp != None):
	print(temp, '\n')
	temp = decrypter.generateGuess()
	temp2 = temp2 + 1
if (temp == None):
	print("Unable to find an answer.")
else:
	print('Found!: ', decrypter.getAnswer(), 'in ', temp2, 'attempts and ', time.time() - startTime, ' seconds\n')
