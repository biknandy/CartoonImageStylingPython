from PIL import Image
from clusterColor import clusterColors
from adaptiveThresh import adaptiveThresh, otsuThresh
import skimage as skim
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from edgeDetectLoG import edgeDetectLoG
from color import RGBfactor, bitManipulateColor

def cartoonStyle(inputFile):
	#import image
	im = skim.io.imread(inputFile)

	k = 15

	adIm = adaptiveThresh(im)
	clustIm = clusterColors(im,k)

	resIm = np.minimum(clustIm,edgeTo3d(adIm))

	fileName = inputFile.split('.')[0]
	fileName_save = fileName +str(k) +'_res.bmp'
	misc.imsave(fileName_save,resIm)

def cartoonStyleGrid(inputFile):
	#import image
	im = skim.io.imread(inputFile)

	k = 15

	otsuIm = otsuThresh(im)
	edges = edgeDetectLoG(im,3)
	adIm = adaptiveThresh(im)
	
	# clustIm = clusterColors(im,k)
	bitIm = bitManipulateColor(im)
	factorIm = RGBfactor(im)

	resIm = np.minimum(factorIm,edgeTo3d(adIm))

	fileName = inputFile.split('.')[0]
	fileName_save = fileName +str(k) +'_res.bmp'
	misc.imsave(fileName_save,resIm)


def edgeTo3d(details):
	return np.dstack((details,details,details))


cartoonStyle('windows_weird.jpg')