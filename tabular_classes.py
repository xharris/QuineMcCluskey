class Prime:
	bit_count = 1
	total_outputs = []
	input_letters = ''

	def __init__(self, val):
		# functions this PI is associated with
		self.outputs = []

		# was this value used to create a reduced value?
		self.checked = False
		self.is_dont_care = False

		self.value = val.replace('0b', '')

		if len(self.value) > Prime.bit_count:
			Prime.bit_count = len(self.value)

	# check if this PI can be simplified with another
	def can_simplify(self, other_pi):
		return True

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

	def getFuncBin(self):
		return ''.join('1' if f in self.outputs else '0' for f in Prime.total_outputs)

	def addFunc(self, letter):
		if not letter in Prime.total_outputs:
			Prime.total_outputs.append(letter)

		if not letter in self.outputs:
			self.outputs.append(letter)

	def getBoolValue(self):
		ret_str = ''
		for i, l in enumerate(self.value):
			if l == '1':
				ret_str += Prime.input_letters[i]
			elif l == '0':
				ret_str += Prime.input_letters[i]+'\''
		return ret_str

	def __str__(self):
		extra_zeroes = '0'*(Prime.bit_count - len(self.value)) if Prime.bit_count - len(self.value) > 0 else ''
		dont_care = ' (d)' if self.is_dont_care else ''
		checked = ' X' if self.checked else ''

		self.value = extra_zeroes + self.value

		self_dec_values = self.getDecValues()
		dec_values = ','.join(self_dec_values) if isinstance(self_dec_values, list) else self_dec_values

		out_str = dec_values + '\t\t' + self.value + ' : ' + self.getFuncBin() + dont_care + checked

		return out_str

	def __eq__(self, other):
		return self.value == other.value

	def __repr__(self):
		return self.value

def createTable(out_letters, in_letters, functions):
	Prime.input_letters = in_letters
	primes = {}
	for m in out_letters:
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

def getExtraZeroes(count, value):
	return '0'*(count - len(value)) if count - len(value) > 0 else ''

def diffPrimes(prime1, prime2):
	a = prime1.value
	b = prime2.value

	result_bin = ''

	diff_pos = -1

	for i, ca in enumerate(a):
		cb = b[i]

		# matching underscores
		if (ca == '-' or cb == '-') and ca != cb:
			return 0

		# one is 0 and other is 1
		elif ca != cb:
			if diff_pos == -1:
				result_bin += '-'
				diff_pos = i
			else:
				return 0

		# both are 1/0
		else:
			result_bin += ca

	new_prime = Prime(result_bin)
	# combine functions
	new_func_bin = bin(int(prime1.getFuncBin(), 2) & int(prime2.getFuncBin(), 2)).replace('0b','')
	new_func_bin = getExtraZeroes(len(Prime.total_outputs), new_func_bin) + new_func_bin

	new_outs = []
	for i, c in enumerate(new_func_bin):
		if c == '1':
			new_outs.append(Prime.total_outputs[i])
	new_prime.outputs = new_outs

	return new_prime

def simplifyTable(table):
	leftovers = []
	new_table = {}
	remove_lefto = []
	simplified_count = 0

	for sec in table:
		if sec < len(table) - 1:
			new_table[sec] = []

			sec1 = table[sec]
			sec2 = table[sec + 1]

			# compare section with section below it
			for p1 in sec1:
				for p2 in sec2:
					new_prime = diffPrimes(p1, p2)
		
					if (new_prime != 0 and new_prime.getFuncBin() != '0'*len(Prime.total_outputs)):
						simplified_count += 1
						
						if not new_prime in new_table[sec]:
							new_table[sec].append(new_prime)

					# can be checked off if they have same function
					if p1.getFuncBin() == p2.getFuncBin() and new_prime != 0:
						p1.checked = True
						remove_lefto.append(p1)
						p2.checked = True
						remove_lefto.append(p2)
					
				if not p1 in leftovers and not p1.checked:
					leftovers.append(p1)

		else:
			for p in table[sec]:
				if not p in leftovers and not p.checked:
					leftovers.append(p)

	printPrimes(table)
	return simplified_count, leftovers, remove_lefto, new_table

# prints a list of primes as equations
def printTerms(primes):
	outputs = {}

	#sort primes into function groups
	for p in primes:
		for f in p.outputs:
			if f not in outputs:
				outputs[f] = []

			outputs[f].append(p)

	for o in Prime.total_outputs:
		print o,'=',
		for i,p in enumerate(outputs[o]):
			print p.getBoolValue(),
			if i < len(outputs[o]) - 1:
				print '+',
			else:
				print ''

