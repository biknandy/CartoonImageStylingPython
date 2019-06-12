from PIL import Image
from clusterColor import clusterColors
from adaptiveThresh import adaptiveThresh, otsuThresh
import skimage as skim
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from edgeDetectLoG import edgeDetectLoG
from color import RGBfactor, bitManipulateColor
import sys

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

	otsuIm = otsuThresh(im)
	lapEdge = edgeDetectLoG(im,3)
	adIm = adaptiveThresh(im)
	edges = [lapEdge, otsuIm, adIm]

	clustIm30 = clusterColors(im,30)
	clustIm15 = clusterColors(im,15)
	clustIm7 = clusterColors(im,7)
	bitIm = bitManipulateColor(im)
	factorIm = RGBfactor(im)

	colors = [bitIm, factorIm, clustIm7, clustIm15, clustIm30]

	dim0 = im.shape[0]
	dim1 = im.shape[1]
	resGrid = np.zeros((len(edges)*dim0,len(colors)*dim1,3))
	for i in range(len(edges)):
		for j in range(len(colors)):
			resIm = np.minimum(colors[j],edgeTo3d(edges[i]))
			resGrid[i*dim0:(i+1)*dim0, j*dim1:(j+1)*dim1] = resIm


	fileName = inputFile.split('.')[0]
	fileName_save = fileName+'_grid.bmp'
	misc.imsave(fileName_save,resGrid)


def edgeTo3d(details):
	return np.dstack((details,details,details))


cartoonStyleGrid(sys.argv[1])