import skimage as skim
from scipy import misc
import scipy.ndimage as scim
import numpy as np
import matplotlib.pyplot as plt
from kmean import *
import math

winSize = 5

def clusterColorsTest(inputFile):
	#Clustering algorithm was adapted by Griffin Danninger and Bik Nandy
	#from code written using pure python by Griffin Danninger in CS 165
	#Adaptability for Minkowski distance metric added for this project

	im = skim.io.imread(inputFile,as_gray=False)
	#load pixels to dict
	data_set = []
	stepSize = 3
	for a in range(0,im.shape[0],stepSize):
		for b in range(0,im.shape[1],stepSize):
			data_point = {}
			data_point['vals'] = im[a,b,:].tolist()
			data_set.append(data_point)

	iter_limit = 50

	xVals = []
	yVals = []
	zVals = []
	minSSS = 1
	mink = 0
	for k in range(2,30,5):
		init_centers = init_centers_random(data_set, k)
		centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
		print str(k) + ", " +str(num_iterations)+", "+ str(sum_of_within_group_ss(clusters, centers))
		#save data
		xVals.append(k)
		yVals.append(sum_of_within_group_ss(clusters, centers))
		zVals.append(num_iterations)
		if sum_of_within_group_ss(clusters, centers) < minSSS:
			minSSS = sum_of_within_group_ss(clusters, centers)
			mink = k
		# print np.asarray(centers).astype(int)
		#reconstruct image
		recolored = np.zeros(im.shape)
		for a in range(im.shape[0]):
			for b in range(im.shape[1]):
				data_point = im[a,b,:].tolist()
				cidx = get_nearest_center(data_point,centers)
				for rgb in range(3):
					recolored[a,b,rgb] = math.floor(centers[cidx][rgb])
		fileName = inputFile.split('.')[0]
		fileName_save = fileName +'_'+str(k) +'_k.bmp'
		misc.imsave(fileName_save,recolored)


	plt.plot(xVals,yVals)
	plt.title('SSS vs. k')
	plt.xlabel('Number of Centers')
	plt.ylabel('Sum of Within Group Sum of Squares')
	plt.show()
	print mink
	print len(data_set)

def clusterColors(im,numColors):
	#Clustering algorithm was adapted by Griffin Danninger and Bik Nandy
	#from code written using pure python by Griffin Danninger in CS 165
	#load pixels to dict
	data_set = []
	stepSize = 3
	for a in range(0,im.shape[0],stepSize):
		for b in range(0,im.shape[1],stepSize):
			data_point = {}
			data_point['vals'] = im[a,b,:].tolist()
			data_set.append(data_point)

	iter_limit = 25

	xVals = []
	yVals = []
	zVals = []
	minSSS = 1
	mink = 0
	k = numColors
	init_centers = init_centers_random(data_set, k)
	centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
	# print str(k) + ", " + str(sum_of_within_group_ss(clusters, centers))
	#save data
	xVals.append(k)
	yVals.append(sum_of_within_group_ss(clusters, centers))
	zVals.append(num_iterations)
	if sum_of_within_group_ss(clusters, centers) < minSSS:
		minSSS = sum_of_within_group_ss(clusters, centers)
		mink = k
	# print np.asarray(centers).astype(int)
	#reconstruct image
	recolored = np.zeros(im.shape)
	for a in range(im.shape[0]):
		for b in range(im.shape[1]):
			data_point = im[a,b,:].tolist()
			cidx = get_nearest_center(data_point,centers)
			for rgb in range(3):
				recolored[a,b,rgb] = math.floor(centers[cidx][rgb])
	# fileName = inputFile.split('.')[0]
	# fileName_save = fileName +str(k) +'_k.bmp'
	# misc.imsave(fileName_save,recolored)


	# plt.plot(xVals,yVals)
	# plt.title('SSS vs. k')
	# plt.xlabel('Number of Centers')
	# plt.ylabel('Sum of Within Group Sum of Squares')
	# plt.show()
	# print mink
	# print len(data_set)
	return recolored

# clusterColorsTest('lena3.bmp')