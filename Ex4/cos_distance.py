##python 2.7
import numpy as np
import math

def test(u, n):
	"""
		tests on which side of the plane (given by the normal n) vector u is
	"""
	if np.dot(u,n) >= 0:
		return 1
	else:
		return 0

def cosine_distance(d,x,y):
	"""
		calculates the approximate angle between vectors x and y of 
		dimension d by counting the number of times they both are on
		the same side of the plane
	"""
	print '# of iter\t\tangle'
	for itr in [10,50]+list(xrange(100, 1000, 100))+[5000, 10000]:
		n_hits = 0
		for i in xrange(1,itr):
			normal = np.random.randn(d)
			h_x = test(x, normal)
			h_y = test(y, normal)
			if h_x == h_y:
				n_hits = n_hits + 1
		angle = (1 - n_hits/(itr*1.0)) * np.pi
		print '%d\t\t\t\t%.6f' %(itr, angle) 

##dimension of the data
d=2;
for r in xrange(10):
	x = np.random.randn(d)
	y = np.random.randn(d)
	true_angle = np.arccos(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)))
	print
	print 'x = %s,    y = %s' %(x, y)
	print 'true angle = %.6f' %(true_angle)
	cosine_distance(d,x,y)
