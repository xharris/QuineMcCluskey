# Quine-McCluskey Method Solver USING OOP
# by Xavier Harris
# 

from tabular_classes import *
from tabular_functions import *

# - - - - PROGRAM INPUTS - - - - -
input_letters = 'ABCD'

output_letters = 'z'
functions = {
	'z': {
		'm': [0,1,2,5,6,7,8,9,10,14],
		'd': []
	}
}
'''
output_letters = 'wxyz'

functions = {
			'w': {
				'm': [1, 3, 9, 11],
				'd': []
				},
			'x': {
				'm': [1, 4, 3, 5, 9, 12, 11],
				'd': []
				},
			'y': {
				'm': [4, 5, 12],
				'd': []
				},
			'z': {
				'm': [1, 3, 5, 6, 7, 14, 15],
				'd': []
				}
			}
'''
# - - - - -------------- - - - - - 

primes = {}

# create initial table
primes = createTable(output_letters, input_letters, functions)
sortTable(primes)
printPrimes(primes)

new_leftovers = []
leftovers = []
lefto_exclude = []
count = 1
table_count = 0

# prime implicant lists
while count > 0:
	table_count += 1
	print '\n\nTABLE',table_count
	new_leftovers = []
	count, new_leftovers, removed_lefto, primes = simplifyTable(primes)

	leftovers += [l for l in new_leftovers if l not in leftovers]
	lefto_exclude += [r for r in removed_lefto if r not in lefto_exclude]


for r in removed_lefto:
		if r in leftovers:
			leftovers.remove(r)

printTerms(leftovers)

# prime implicant chart