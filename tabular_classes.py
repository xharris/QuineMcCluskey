class PI_Table:
	def __init__(self, bits=1):
		self.reduced = False
		self.sections = []
		self.outputs = []

		self.num_bits = bits
		for i in range(bits + 1):
			self.sections.append(PI_TableSection())

	def addFunction(self, out_letter, terms):
		term = 0	

		for minT in terms['m']:
			term = self.addDecValue(minT)
			term.addFunc(out_letter)

		for dontC in terms['d']:
			term = self.addDecValue(dontC)
			term.is_dont_care = True
			term.addFunc(out_letter)

	def addDecValue(self, val):
		return self.addBinValue(bin(val))

	def addBinValue(self, val):
		if self.reduced:
			return

		one_count = val.count('1')
		new_PI = Prime(val)

		self.sections[one_count].add(new_PI)

		return new_PI

	def __str__(self):
		out_str = ''
		for s in self.sections:
			out_str += str(s) + ('-'*(self.num_bits*3)) + '\n'

		return out_str

class PI_TableSection:
	def __init__(self):
		self.primes = []

	def add(self, prime):
		found = False
		for p in self.primes:
			if p == prime:
				found = True
				p.addFuncs(prime.outputs)
		if not found:
			self.primes.append(prime)

			# sort terms
			self.primes = sorted(self.primes, key=lambda prime: int(prime.getDecValues()))

	def __str__(self):
		out_str = ''

		for p in self.primes:
			out_str += str(p) + '\n'
		return out_str

	def __add__(self, other):
		print self, other

	def __len__(self):
		return len(self.primes)

	def __getitem__(self, key):
		return self.primes[key]

class Prime:
	bit_count = 1
	total_outputs = []

	def __init__(self, val):
		# functions this PI is associated with
		self.outputs = []

		# was this value used to create a reduced value?
		self.was_simplified = False
		self.is_dont_care = False

		self.value = val.replace('0b', '')

		if len(self.value) > Prime.bit_count:
			Prime.bit_count = len(self.value)

	# check if this PI can be simplified with another
	def can_simplify(self, other_pi):
		return True

	# return decimal values this PI covers
	def getBinValues(self):
		binary = []
		decimal = self.getDecValues()
		for d in decimal:
			binary.append(dec(d))
		return binary

	# return decimal values this PI covers
	def getDecValues(self):
		result = self._getDecValues(self.value,[])
		for i,r in enumerate(result):
			if type(r) == list:
				del result[i]
		return result

	def _getDecValues(self, txt, values=[]):
		if '-' in txt:
			values.append(self._getDecValues(txt.replace('-','0',1),values))
			values.append(self._getDecValues(txt.replace('-','1',1),values))
		else:
			return str(int(txt, 2))

		return values

	def addFunc(self, letter):
		if not letter in Prime.total_outputs:
			Prime.total_outputs.append(letter)

		if not letter in self.outputs:
			self.outputs.append(letter)

	def addFuncs(self, letters):
		for l in letters:
			self.addFunc(l)

	def __str__(self):
		extra_zeroes = '0'*(Prime.bit_count - len(self.value)) if Prime.bit_count - len(self.value) > 0 else ''
		dont_care = ' (d)' if self.is_dont_care else ''

		out_str = self.getDecValues() + '\t\t' + extra_zeroes + self.value + ' : ' + ''.join('1' if f in self.outputs else '0' for f in Prime.total_outputs) + dont_care 

		return out_str

	def __eq__(self, other):
		return self.value == other.value

def createTable(letters, functions):
	primes = {}
	for m in letters:
		for minterm in functions[m]['m']:
			new_prime = Prime(bin(minterm))
			new_prime.addFunc(m)

			ones = new_prime.value.count('1')
			if not ones in primes:
				primes[ones] = []

			found = False
			for p in primes[ones]:
				if p == new_prime:
					found = True
					p.addFunc(m);

			if not found:
				primes[ones].append(new_prime)
	return primes

def sortTable(table):
	for sec in table:
		table[sec] = sorted(table[sec], key=lambda prime: int(prime.getDecValues()) )

def printPrimes(table):
	for sec in table:
		for prime in table[sec]:
			print prime
		print '-----'*Prime.bit_count