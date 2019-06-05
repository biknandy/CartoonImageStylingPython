import numpy as np
import math
import scipy.ndimage as skim
import scipy.signal as sksig

def edgeDetectLoG(imArray, sigma):
	#Create Gaussian based on sigma
	GaussFilter = makeGauss(sigma)
	#Create Lapalacian filter
	LapFilter = np.array([	[0,-1,0],
							[-1,4,-1],
							[0,-1,0]])
	#convolve Lap w/ Gauss
	cFilter = sksig.convolve2d(GaussFilter,LapFilter)
	#convolve im w/ filter
	result = sksig.convolve2d(imArray,cFilter,mode='same')
	#detect 0 crossings
	result = detectZero(result)
	#return result as np array
	return result

def makeGauss(sigma):
	n = 6*sigma + 1
	res = np.zeros((n,n))
	for r in range(res.shape[0]):
		for c in range(res.shape[1]):
			i = c-1-math.floor(n/2)
			j = r-1-math.floor(n/2)
			res[r,c] = (1.0/(2*math.pi*(sigma**2)))*math.exp(-((i**2)+(j**2))/(1.0*(sigma**2)))
	return res

def detectZero(arrIn):
	res = arrIn
	for r in range(arrIn.shape[0]):
		for c in range(arrIn.shape[1]):
			#check if comparison pixel is in bounds and of opposite sign
			if r < arrIn.shape[0]-1 and arrIn[r,c]*arrIn[r+1,c] < 0:
				res[r,c] = 1
			elif c < arrIn.shape[1]-1 and arrIn[r,c]*arrIn[r,c+1] < 0:
				res[r,c] = 1
			else:
				res[r,c] = 0
	#stub
	res = res*255
	return res