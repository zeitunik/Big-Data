import numpy as np
import random as rnd
import string 
import copy

def create_documents(n, l):
	"""
		Creates a list of n strings of length l
		1st string has random characters, the rest have increasing noise 
	"""
	D = np.random.randint(0, 256, l, dtype=np.uint8)
	return [D]+[modify_string(D,i) for i in range(1,n)]

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
	# shift the polynomial until it and the shingle align
	poly <<= (pos - 16)
	
	while (pos >= 16 and not shingle == 0):# if the remainder has less than 16 bits, it won't change anymore
		# find the first 1 in the bit string of shingle
		bits = 0
		temp = 1<<pos
		while (not (temp & shingle)):
			temp >>= 1
			bits += 1

		poly >>= bits		 	# shift polynomial, so that the ones align
		shingle ^= poly 		# XOR - basically the remainder 
		pos -= bits 			# current position of the polynomial

	return shingle

def sketch_matrix(M, K):
	"""
		creates a sketch matrix from the matrix M, where the rows 
		correspond to the shingles and the columns to the documents
		K is the number of rows the resulting sketch matrix should have
	"""
	rows = M.shape[0]
	cols = M.shape[1]
	
	M_s = np.full((K,cols), rows)	# fill the matrix by rows (cannot be a number higher than this)

	# Generate hashing functions parameters
	P = 70657								# a prime number bigger than rows (for our purposes it works)
	H = np.random.randint(1, P-1, (K,2))	# 2 random numbers a and b for each of the K hash functions

	for i in range(rows):
		for j in range(cols):
			if M[i,j] == 1:
				for k in range(K):
					hash_val = ( (H[k][0]*i + H[k][1]) % P ) % rows
					if hash_val < M_s[k][j]:
						M_s[k][j] = hash_val
	return M_s

def calculate_similarity(M_s):
	"""
		Calculates the similarity between the 1st and the other
		columns of the sketch matrix M_s
	"""
	rows = M_s.shape[0]
	cols = M_s.shape[1]

	first_col = M_s[:,0]
	similarities = np.zeros(cols-1)

	for j in range(1, cols):
		j_col = M_s[:,j]
		sim = np.sum(np.equal(first_col, j_col))
		similarities[j-1] = sim/rows				# approximate similarity

	return similarities

##### main #####

# create 100 documents of length 1000
docs = create_documents(100, 1000)

# shingle list
Q = [i for i in range(2,10)] + [15, 20]

# open output file
f = open('output.txt', 'w')

for q in Q:
	# generate the shingles and their fingerprints for all docs
	M = np.array([shingles(doc, q) for doc in docs]).transpose()

	# get the sketch matrix for M
	M_s = sketch_matrix(M, 100)

	# calculate the similarities between the documents
	S = calculate_similarity(M_s)
	
	f.write("Number of shingles:\t{}", q)

	f.write([sim for sim in S])
	
	#print("Number of shingles:\t", q)
	#print([sim for sim in S])

f.close()