import numpy as np
import random as rnd
import string 
import copy

def create_documents():
	"""
		Creates a list of 100 strings of length 1000
		1st string has random characters, the rest have increasing noise 
	"""
	D = np.random.randint(0, 256, 1000, dtype=uint8)
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

