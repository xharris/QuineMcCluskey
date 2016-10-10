# Quine-McCluskey Method Solver
# by Xavier Harris
# 

# - - - - PROGRAM INPUTS - - - - -
input_letters = 'ABCD'
minterms = [4,8,10,11,12,15]
dont_cares = []
# - - - - - - - - - - - - - - - - 




import pprint
pp = pprint.PrettyPrinter(indent=4)

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
		if not (a[c] == '-' and b[c] == '-') and (a[c] != b[c]):
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
while changes > 0 and not err:
	old_tabs = tabs
	tabs = {}
	changes = 0

	#iterate through groups
	for i in old_tabs:
		tabs[i] = []
		group = old_tabs[i]
		if (i < len(old_tabs) - 1):

			# iterate through group members
			for t1 in group:
				indiv_results = 0

				if i + 1 in old_tabs:
					for t2 in old_tabs[i + 1]:
						result = bin_compare(t1, t2)

						if result != 0:
							indiv_results += 1
							changes += 1

							had_a_match.extend((t1,t2))

							tabs[i].append(result)

					if indiv_results == 0 and not t1 in had_a_match and not t1 in no_matches:
						no_matches.append(t1)

print 'TABLE REDUCTION RESULTS:'
printTabs(no_matches)
print ''

### PART 2 ### Weird grid thing

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

# move terms with a single number to the front
temp_t = []
for term in term_priority:
	for single in dec_num_singles:
		if str(single) in table_vals[term] and not term in temp_t:
			temp_t.append(term)

for term in term_priority:
	if not term in temp_t:
		temp_t.append(term)

term_priority = temp_t

end_terms = []
# remove implicants adn the numbers they cover until nothing is left
for term in term_priority:
	removed = 0
	for num in table_vals[term]:
		if int(num) in dec_nums:
			dec_nums.remove(int(num))
			removed += 1

			if not term in end_terms:
				end_terms.append(term)

### PART 3 ### Print results
end_str = 'Z = '

for t,term in enumerate(end_terms):
	end_str += termToLetters(term)

	if t < len(end_terms) - 1:
		end_str += ' + '

print end_str