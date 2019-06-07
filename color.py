import sys
from scipy import misc, ndimage
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np
import skimage
from skimage import data
from skimage.color import rgb2hsv
from skimage.filters.rank import modal
from skimage.morphology import disk


def RGBfactor (input_file):
	image = skimage.io.imread(input_file)
	# image = image.astype(float)
	#print (image.shape)
	factor = 64

	red = image[:,:,0]
	#print (red)

	green = image[:,:,1]

	blue = image[:,:,2]
	

	red_frac = red/factor
	green_frac = green/factor
	blue_frac = blue/factor

	red_r = np.round(red_frac)
	green_r = np.round(green_frac)
	blue_r = np.round(blue_frac)

	#print (np.max(red_r))
	

	#Range of each color 
	maps = np.arange(factor).reshape((4,4,4))

	grey_version = maps[red_r,green_r,blue_r]

	print ("GREY")
	print(grey_version)



	reconstruct = np.dstack(((factor * red_r) , (factor * green_r) ,(factor * blue_r)))

	reconstruct = reconstruct + 32

	#print (reconstruct)

	reconstruct[reconstruct == 256] = 255

	

	#filtered = ndimage.median_filter(reconstruct, size = 2)
	# modalfilt = modal(reconstruct, disk(5))





	fileName = input_file.split('.')[0]

	fileNameSave = fileName + "_copy.jpg"
	misc.imsave(fileNameSave, reconstruct)

	matplotlib.pyplot.imshow(reconstruct)
	matplotlib.pyplot.show()

def bitManipulation(input_file):
	image = misc.imread(input_file)

	bitsize = 6

	red = image[:,:,0]
	print(red)
	green = image[:,:,1]

	blue = image[:,:,2]

	#red_bit = np.array(map(bin, red.flatten())).reshape(red.shape)
	red_bit = np.right_shift(red, bitsize)
	red_bit = np.left_shift(red_bit,bitsize)
	print(red_bit)


	green_bit = np.right_shift(green, bitsize)
	green_bit = np.left_shift(green_bit,bitsize)

	blue_bit = np.right_shift(blue,bitsize)
	blue_bit = np.left_shift(blue_bit,bitsize)

	reconstruct = np.dstack((red_bit , green_bit , blue_bit))

	fileName = input_file.split('.')[0]

	fileNameSave = fileName + "_copy.bmp"
	misc.imsave(fileNameSave, reconstruct)

	matplotlib.pyplot.imshow(reconstruct)
	matplotlib.pyplot.show()


RGBfactor (sys.argv[1]);
#bitManipulation(sys.argv[1])