# Quine-McCluskey Method Solver USING OOP
# by Xavier Harris
# 

from tabular_classes import *
from tabular_functions import *

# - - - - PROGRAM INPUTS - - - - -
input_letters = 'ABCD'
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
dont_cares = []
# - - - - -------------- - - - - - 

primes = {}

# create initial table
primes = createTable(output_letters, functions)
sortTable(primes)
printPrimes(primes)

