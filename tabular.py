# Quine-McCluskey Method Solver
# by Xavier Harris
# 

# - - - - PROGRAM INPUTS - - - - -
input_letters = 'ABCD'
minterms = [0,1,2,3,5,7,8,10,12,13,15]
dont_cares = []
# - - - - -------------- - - - - - 

# print the minterms/dont cares
out_str = 'f(' + ','.join(list(input_letters)) + ') = E m('
for m in minterms:
	out_str += str(m) + ', '
out_str = out_str[:-2] + ')'

if len(dont_cares) > 0:
	out_str += ' + d('
	for d in dont_cares:
		out_str += str(d) + ', '
out_str = out_str[:-2] + ')'
print out_str,'\n'

bin_inputs = []
max_bin_length = 0

minterms.extend(dont_cares)
inputs = minterms
inputs.sort()

def getIntValues(txt):
	result = _getIntValues(txt,[])
	for i,r in enumerate(result):
		if type(r) == list:
			del result[i]
	return result


def _getIntValues(txt, values=[]):
	if '-' in txt:
		values.append(_getIntValues(txt.replace('-','0',1),values))
		values.append(_getIntValues(txt.replace('-','1',1),values))
	else:
		return str(int(txt, 2))

	return values

def printTabs(the_tabs):
	for t in the_tabs:
		all_t = getIntValues(t)

		print ','.join(all_t)+((max_bin_length - len(all_t))*'  '), '\t\t', t

def termToLetters(term):
	ret_str = ''
	for i,d in enumerate(term):
		if d != '-':
			if d == '0':
				ret_str += '!'

			ret_str += input_letters[i]
	return ret_str

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

### PART 1 ### Reduction tables

# convert to binary
for i,term in enumerate(inputs):
	binary = bin(term)[2:]
	bin_inputs.append(binary)

	if (len(binary) > max_bin_length):
		max_bin_length = len(binary);

# give everything the same number of digits
bin_inputs = list(map(lambda item: ('0'*(  max_bin_length - len(item) if (max_bin_length - len(item) > 0) else 0   )) + item, bin_inputs))

# setup inital tab groups
tabs = {}
for i,term in enumerate(bin_inputs):
	if not tabs.has_key(term.count('1')):
		tabs[term.count('1')] = [];

	tabs[term.count('1')].append(term);

def bin_compare(a,b):
	diff_count = 0
	diff_pos = -1

	for c in range(len(a)):
		if (a[c] != b[c]):
			diff_count += 1
			diff_pos = c

	if diff_count == 1:
		new_a = list(a)
		new_a[diff_pos] = '-'
		return ''.join(new_a)
	
	return 0

changes = 1
no_matches = []
had_a_match = []
err = False
iteration = 1
while changes > 0 and not err:
	old_tabs = tabs
	tabs = {}
	changes = 0

	print 'TABLE',iteration
	for tab in old_tabs:
		if len(old_tabs[tab]) > 0:
			printTabs(old_tabs[tab])
			print '-'*(max_bin_length*5)
	iteration += 1
	print ''

	for k in old_tabs:
		tabs[k] = []

		if (k+1) in old_tabs and len(old_tabs[k+1]) > 0:
			for val1 in old_tabs[k]:
				for val2 in old_tabs[k+1]:

					result = bin_compare(val1, val2)

					if result:
						if result not in tabs[k]:
							tabs[k].append(result)
						changes += 1

						if not val1 in had_a_match:
							had_a_match.append(val1)
						if not val2 in had_a_match:
							had_a_match.append(val2)
						
						if val1 in no_matches:
							no_matches.remove(val1)
						if val2 in no_matches:
							no_matches.remove(val2)
					else:
						if not val1 in had_a_match and not val1 in no_matches:
							no_matches.append(val1)
						if not val2 in had_a_match and not val2 in no_matches:
							no_matches.append(val2)

		else:
			for val in old_tabs[k]:
				if not val in had_a_match and not val in no_matches:
					no_matches.append(val)


for d in dont_cares:
	if d in no_matches:
		no_matches.remove(d)

print 'TABLE REDUCTION RESULTS:'
printTabs(no_matches)
print ''

### PART 2 ### Prime implicant chart

if len(no_matches) > 1:
	print 'Using prime implicant chart... \n'

no_matches = sorted(no_matches, key=lambda term: term.count('-'), reverse=True)
dec_nums = []
dec_num_count = {}
dec_num_singles = []

for m in no_matches:
	for i in getIntValues(m):
		if not i in dec_num_count:
			dec_num_count[i] = 0

		dec_num_count[i] += 1

		if not int(i) in dec_nums:
			dec_nums.append(int(i))


# numbers that only occur once
dec_num_singles = [int(num) for num,count in dec_num_count.iteritems() if count == 1]
# sort numbers by number of occurrences in term dict
dec_nums = sorted(dec_nums, key=lambda num: dec_num_count[str(num)])

table_vals = {}
term_size = {}
for m in no_matches:
	table_vals[m] = getIntValues(m)

# sort by number of numbers the term covers
term_priority = sorted(no_matches, key=lambda term: len(table_vals[term]), reverse=True)

# FIND BEST TERM TO REMOVE
#	1. has a unique number
#	2. has the most numbers in remaining_nums

finalists = []
remaining_nums = dec_nums

def addFinalist(term):
	finalists.append(term)

	if term in no_matches:
		no_matches.remove(term)

	for num in table_vals[term]:
		if int(num) in remaining_nums:
			for t in table_vals:
				if t != term and num in table_vals[t]:
					table_vals[t].remove(num)

		if int(num) in remaining_nums:
			remaining_nums.remove(int(num))

		if int(num) in dec_num_singles:
			dec_num_singles.remove(int(num))

	del table_vals[term]

while len(remaining_nums) > 0:
	# FIND BEST TERM
	# sort by number array size
	term_priority = sorted(no_matches, key=lambda term: len(table_vals[term]), reverse=True)
	# bring singles to the front
	temp_t = []
	for term in term_priority:
		for single in dec_num_singles:
			if str(single) in table_vals[term] and not term in temp_t:
				temp_t.append(term)
				
	temp_t.extend(diff(term_priority,temp_t))
	term_priority = temp_t

	term = term_priority[0]

	#pick a single if it exists
	single_exists = False
	for s in dec_num_singles:
		# does term contain a single
		if not single_exists and str(s) in table_vals[term]:
			single_exists = True

			# remove terms numbers
			addFinalist(term)

	# remove largest term
	if not single_exists:
		addFinalist(term)

### PART 3 ### Print results
end_str = 'Z = '

for t,term in enumerate(finalists):
	end_str += termToLetters(term)

	if t < len(finalists) - 1:
		end_str += ' + '

print end_str
