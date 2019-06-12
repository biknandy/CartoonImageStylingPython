import skimage as skim
import scipy.ndimage as scim
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt

def otsuThresh(imIn):
	#implements Otsu's Method
	imIn = skim.color.rgb2gray(imIn)*255
	# imIn.reshape(winSize,winSize)
	resIm = imIn
	imHist, histBins = skim.exposure.histogram(imIn,256)
	imHist = imHist.astype(float)
	probs = imHist / sum(imHist)

	bestT = 0

	mT = sum(probs*histBins)
	for t in range(1,255):
		w0 = sum(probs[:t])
		w1 = sum(probs[t:])
		if w0 == 0 or w1 == 0:
			continue
		m0 = sum(probs[:t]*histBins[:t])/w0
		m1 = sum(probs[t:]*histBins[t:])/w1
		# print(w0*m0+w1*m1)
		var2 = w0*w1*((m0-m1)**2)
		# print var2
		if bestT==0:
			var2max = var2
			bestT = t
		else:
			if var2>var2max:
				var2max = var2
				bestT = t
	# print bestT
	resIm[resIm>bestT] = 255
	resIm[resIm<=bestT] = 0
	return resIm
	# return bestT

def adaptiveThresh(im):
	
	im = skim.color.rgb2gray(im)*255
	# print im	
	
	winSize = .05*((im.shape[0]*im.shape[1])**0.5)
	if winSize%2 !=0:
		winSize+=1
	
	offset = 10

	gaussSigma = winSize/6.0
	thresholds = scim.gaussian_filter(im,gaussSigma,mode='reflect') - offset


	threshIm = np.zeros(im.shape)
	threshIm[im>thresholds] = 255
	return threshIm

inputFile = 'cameraman_md.png'
im = skim.io.imread(inputFile)
tIm = adaptiveThresh(im)
fileName = inputFile.split('.')[0]
fileName_save = fileName + '_adaptiveThresh.bmp'
misc.imsave(fileName_save,tIm)
