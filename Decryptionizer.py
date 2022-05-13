# This class is used to make a guess of a password that uses default variations of common hashes
# It requires you initialize it, tell it what characters are valid, add the list of common passwords, and tell it what encryptions to use
# If it found a password, then its previous guess would be it (it increments after every guess)
import hashlib # for the hashing


class Decryptionizer:
	# GLOBAL VARIABLES
	numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
	lettersLower = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
	lettersUpper = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
	specialChars = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "`", "~", "[", "]", "{", "}", "\\", "|", ";", ":", "\'", "\"", ",", "<", ">", ".", "/", "?", " ")

	# CONSTRUCTOR
	def __init__(self, minLength, maxLength):
		self.minLength = minLength # minimum length of string to test (0 is smallest)
		self.maxLength = maxLength # max length of string to test (-1 for no limit)
		self.validCharacters = []; # empty list be default
		# For generating permutations
		self.totalPermutations = 0 # stores the possible permutations, -1 if infinite
		self.permutation = 0 # stores what permutation this decrtyptionizer is on
		self.digitPermutations = [] # stores what permutation for the one digit it is on
		self.validEncryptions = [] # a list of the names of the encryptions to apply in order they should be applied
		self.currentEncryption = 0
		self.commonPassword = 0 # what common password it is on
		self.commonPasswords = [] # list of common passwords
		
		# sets up the digitPermutations list to be the right starting length
		temp = 0
		while (temp < minLength):
			self.digitPermutations.append(0)
			temp = temp + 1

		#adds a blank common password, as the permutation doesn't support it
		self.commonPasswords.append("")

	# METHODS
	def addCommonPassword(self, string):
		self.commonPasswords.append(string)
	
	# setValidCharacters and addValidCharacters are for more exact control of valid characters

	# made to show an alternative for getting the individual characters that is simpler in setup, but slower in execution
	def permutationNumberToDigitPermutations(self):
		tempList = [self.permutation]
		temp = 0
		while (tempList[temp] > len(self.validCharacters())):
			# if a next one doesn't exist, then append, else increment next one
			if (temp + 1 >= len(tempList)):
				tempList.append(0)
				tempList[temp] = tempList[temp] - len(self.validCharacters()) # removes length of valid characters as that is the amount to trigger needing to go to next character
			else:
				tempList[temp + 1] = tempList[temp + 1] + 1
				tempList[temp] = tempList[temp] - len(self.validCharacters()) # removes length of valid characters as that is the amount to trigger needing to go to next character
		return tempList

	def getPermutationAsList(self):
		#convert each digit permutation to a character and adds it to the tempList
		tempList = []
		temp = 0
		while (temp < len(self.digitPermutations)):
			tempList.append(self.validCharacters[self.digitPermutations[temp]])
			temp = temp + 1
		return tempList

	def getPermutationAsString(self):
		tempList = self.getPermutationAsList()
		return ''.join(str(e) for e in tempList) # returns tempList as a string

	# intended to be the last thing called after finding the right guess, as it decrements the permutation in order to return the guess
	def getAnswer(self):
		# if not done with common passwords
		if (self.commonPassword < len(self.commonPasswords)):
			return self.commonPasswords[self.commonPassword]
		# if done with common passwords
		else:
			self.decrementPermutation()
			return self.getPermutationAsString()

	def incrementPermutation(self):
		self.permutation = self.permutation + 1
		self.digitPermutations[0] = self.digitPermutations[0] + 1
		# checks to see if digitPermutations needs to add or edit a character
		temp = 0
		while (self.digitPermutations[temp] >= len(self.validCharacters)):
			self.digitPermutations[temp] = 0
			if (len(self.digitPermutations) > (temp + 1)): # if next digitPermutation index of list exists
				self.digitPermutations[temp + 1] = self.digitPermutations[temp + 1] + 1
			else:
				self.digitPermutations.append(0) # make digitPermutations bigger
			temp = temp + 1

	def decrementPermutation(self):
		if (self.permutation != 0): # base case of preventing it going backwards if one the first permutation
			self.permutation = self.permutation - 1
			self.digitPermutations[0] = self.digitPermutations[0] - 1
			# checks to see if digitPermutations needs to remove or edit a character
			temp = 0
			while (self.digitPermutations[temp] < 0 and temp < len(self.digitPermutations)):
				self.digitPermutations[temp] = len(self.validCharacters) - 1 # sets to the last valid character
				if (len(self.digitPermutations) > (temp + 1)): # if next digitPermutation index of list exists
					if (self.digitPermutations[temp + 1] == 0): # if next one is at 0, remove it, else subtract 1
						del self.digitPermutations[temp + 1]
					else:
						self.digitPermutations[temp + 1] = self.digitPermutations[temp + 1] - 1
				else:
					self.digitPermutations.append(0) # make digitPermutations bigger
				temp = temp + 1

	def setValidCharacters(self, listOfChars):
		self.validCharacters = listOfChars
		self.calculateTotalPermutation()

	def addValidCharacters(self, listOfChars):
		temp = 0
		while (temp < len(listOfChars)):
			self.validCharacters.append(listOfChars[temp])
			temp = temp + 1
        # need to have it update the total permutations

	# this adds a preset list if it is mentioned by the variable name
	def addPresetList(self, name):
		if (name.lower() == 'numbers'):
			self.addValidCharacters(list(self.numbers))
		elif (name.lower() == 'lowercase letters'):
			self.addValidCharacters(list(self.lettersLower))
		elif (name.lower() == 'uppercase letters'):
			self.addValidCharacters(list(self.lettersUpper))
		elif (name.lower() == 'special characters'):
			self.addValidCharacters(list(self.specialChars))
		elif (name.lower() == 'all'):
			self.addValidCharacters(list(self.numbers))
			self.addValidCharacters(list(self.lettersLower))
			self.addValidCharacters(list(self.lettersUpper))
			self.addValidCharacters(list(self.specialChars))
		#else:
			# don't add anything
			# could add a print or print to a file to act as a debug
		self.calculateTotalPermutation()

	# Will add an encryption to the list to be used when making permutations
	# each encryption here needs a corresponding entry in encrypt()
	def addEncryptionToList(self, name):
		if (name.lower() == 'none'):
			self.validEncryptions.append('none')
		# SHA224
		elif (name.lower() == 'sha224'):
			self.validEncryptions.append('sha224')
		# SHA256
		elif (name.lower() == 'sha256'):
			self.validEncryptions.append('sha256')
		# SHA384
		elif (name.lower() == 'sha384'):
			self.validEncryptions.append('sha384')
		# SHA512
		elif (name.lower() == 'sha512'):
			self.validEncryptions.append('sha512')
		# MD5
		elif (name.lower() == 'md5'):
			self.validEncryptions.append('md5')
		#all of them
		elif (name.lower() == 'all'):
			self.validEncryptions.append('sha224')
			self.validEncryptions.append('sha256')
			self.validEncryptions.append('sha384')
			self.validEncryptions.append('sha512')
			self.validEncryptions.append('md5')
		#else:
			# adds nothing


	# ecryption is a string of the name of encryption wanted
	# returns the hexidecimal output of the hashes
	def encrypt(self, string, encryption):
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

	def guessLoop(self):
		breakLoop = false
		while (breakLoop != true):
			TODO# tries to make a guess until out of time, guesses, or while loop broken

	# returns a guess (if guess is None then it is out of guesses)
	# If added salting, it would have to be added here where currentSalt and timesSalted would be needed to track the salting
	def generateGuess(self):
		guess = ''
		# will make guesses of all of the common passwords first (encrypted with whatever they are supposed to be in)
		if (self.commonPassword < len(self.commonPasswords)):
			guess = self.commonPasswords[self.commonPassword] # make a guess using the common password it is on 
			# Encryption part
			if (len(self.validEncryptions) > self.currentEncryption): # if not done with encryptions, guess with current one
				guess = self.encrypt(guess, self.validEncryptions[self.currentEncryption])
				self.currentEncryption = self.currentEncryption + 1
			else:
				self.commonPassword = self.commonPassword + 1 # go to next common password
				self.currentEncryption = 0 # reset current encryption
				
		else: # tries guessing using permutations of valid characters
			guess = self.generatePermutation()
			# Encryption part
			if (len(self.validEncryptions) > self.currentEncryption): # if not done with encryptions, guess with current one
				guess = self.encrypt(guess, self.validEncryptions[self.currentEncryption])
				self.currentEncryption = self.currentEncryption + 1
			else: # if at the end of the encryption list, start at the beginning and guess
				self.currentEncryption = 0 # reset current encryption
				self.incrementPermutation() # goes to next permutation
				guess = self.encrypt(guess, self.validEncryptions[self.currentEncryption]) # makes a guess
				self.currentEncryption = self.currentEncryption + 1
		return guess


	# will generate a permutation and return it, if out of guesses it returns NULL
	def generatePermutation(self):
		tempList = []
		# gets the next permutation
		if (self.totalPermutations == -1 or self.permutation < self.totalPermutations):
			tempList = self.getPermutationAsList() # gets current permutation
		else:
			return None # returns null if out of guesses
		# encrypts it with the correct encryptions
		# returns the encrypted permutation
		#return (''.join(tempList)) 
		return ''.join(str(e) for e in tempList) # returns tempList as a string

    # Used to fill out totalPermutations
	def calculateTotalPermutation(self):
		if (self.maxLength == -1):
			self.totalPermutations = -1
		else:
			if (self.minLength > 0):
				self.totalPermutations = (self.calculatePermutations(len(self.validCharacters), self.maxLength) - self.calculatePermutations(len(self.validCharacters), self.minLength))
			else:
				self.totalPermutations = self.calculatePermutations(len(self.validCharacters), self.maxLength)

    # will return the total permutations possible based on the characters allowed and length
	def calculatePermutations(self, n, r):
		return (n**r)

	def calculatePermutationsNoRep(self, n, r):
		return (factorial(n) / factorial(n - r))

	def calculateCombinationsNoRep(self, n, r):
		return (factorial(n) / ((factorial(r) * factorial(n - r))))

	def calculateCombinations(self, n, r):
		return (factorial(n + r - 1) / ((factorial(r) * factorial(n - r))))

	def factorial(self, num):
		return (num * factorial(num - 1))
