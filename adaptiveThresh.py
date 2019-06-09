import skimage as skim
import scipy.ndimage as scim
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt

def otsuThresh(imIn):
	#implements Otsu's Method
	imIn.reshape(winSize,winSize)
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
	print bestT
	# resIm[resIm<bestT] = 0
	# resIm[resIm>=bestT] = 255
	# return resIm
	return bestT

def adaptiveThresh(inputFile):
	im = skim.io.imread(inputFile)
	im = skim.color.rgb2gray(im)*255
	print im	
	winSize = .05*((im.shape[0]*im.shape[1])**0.5)
	if winSize%2 !=0:
		winSize+=1
	print winSize
	# thresholds = np.zeros(im.shape)
	# scim.generic_filter(im,otsuThresh,winSize,output = thresholds)
	# threshIm = np.zeros(im.shape)
	# threshIm[im>thresholds] = 255
	thresholds = skim.filters.threshold_local(im, winSize, offset = 10)
	threshIm = np.zeros(im.shape)
	threshIm[im<thresholds] = 255
	plt.imshow(threshIm, cmap='gray', vmin=0, vmax=255)
	plt.show()
	fileName = inputFile.split('.')[0]
	fileName_save = fileName + '_thresh.bmp'
	misc.imsave(fileName_save,threshIm)

adaptiveThresh('cats-150x150.jpg')