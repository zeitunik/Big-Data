import numpy as np
import random as rnd
import string 
import copy

def create_documents():
	"""
		Creates a list of 100 strings of length 1000
		1st string has random characters, the rest have increasing noise 
	"""
	D = np.random.randint(0, 256, 1000, dtype=np.uint8)
	return [D]+[modify_string(D,i) for i in range(1,100)]

def modify_string(D, i):
	"""
		add noise to the string D
		i noise parameter
	"""
	k = 3*i 	# number of random replacements
	l = 2*i 	# number of random swaps
	D_new = copy.deepcopy(D)
	
	for j in range(k):
		idx = rnd.randint(0, len(D_new)-1)
		D_new[idx] = np.random.randint(0, 256)

	for j in range(l):
		idx1 = np.random.randint(0, len(D_new))
		idx2 = np.random.randint(0, len(D_new))
		temp = D_new[idx1]
		D_new[idx1] = D_new[idx2]
		D_new[idx2] = temp

	return D_new

def shingles(document, q):
	"""
		divides the document into q-shingles and calculates their fingerprint
	"""
	if q < 2:
		return document
	f_prints = np.zeros(1<<16, dtype=np.uint8)

	shingle = document[0]
	for i in document[1:q]:
		shingle <<= 8
		shingle |= i
	f_prints[fingerprint(shingle,q)] = 1

	for i in document[q:]:
		shingle <<= 8
		shingle &= 1<<(q*8) - 1
		shingle |= i
		f_prints[fingerprint(shingle,q)] = 1

	return f_prints


def fingerprint(shingle, q):
	"""
		returns the fingerprint of the shingle of size q
		Rabin's fingerprint is used for the following irreducible polynomial:
		x^16 + x^13 + x^12 + x^11 + x^10 + x^9 + x^8 + x^4 + 1 
	"""
	poly = 1<<16 | 1<<13 | 1<<12 | 1<<11 | 1<<10 | 1<<9 | 1<<8 | 1<<4 | 1

	pos = q*8 	# number of bits
    poly <<= (pos - 16)		# shift the polynomial until its and the shingle's most significant bits align
    bits = 0 
    while (pos >= 16 and not shingle == 0): 	# if the remainder has less than 16 bits, it won't change anymore 
    	# find the first one in the bit string of shingle
        temp = 1<<pos
        while (not (temp & shingle)):
        	temp >>= 1 	
        	bits += 1

        poly >>= bits		 	# shift polynomial, so that the ones align
        shingle ^= poly 		# XOR - basically the remainder 
        pos -= bits 			# current position of the polynomial

    return shingle


##### main ###

docs = documents()

Q = [i for i in range(2,10)] + [15, 20]

for q in Q:
	# generate the shingles and their fingerprints for all docs
	M = [shingles(doc, q) for doc in docs]

	
