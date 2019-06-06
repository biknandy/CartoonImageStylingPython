import sys
from scipy import misc
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np


def RGBfactor (input_file):
	image = misc.imread(input_file)
	print (image.shape)
	factor = 4

	red = image[:,:,0]
	print (red)

	green = image[:,:,1]

	blue = image[:,:,2]
	

	red_frac = red/factor
	print (red_frac)
	green_frac = green/factor
	blue_frac = blue/factor

	red_r = np.round(red_frac)
	green_r = np.round(green_frac)
	blue_r = np.round(blue_frac)
	

	reconstruct = (factor * red_r) + (factor * green_r) + (factor * blue_r)

	fileName = input_file.split('.')[0]

	fileNameSave = fileName + "_copy.bmp"
	misc.imsave(fileNameSave, reconstruct)

	#matplotlib.pyplot.imshow(reconstruct, cmap)
	# matplotlib.pyplot.show()

	# matplotlib.pyplot.imshow(grey, cmap = matplotlib.cm.Greys_r)
	# matplotlib.pyplot.show()

def bitManipulation(input_file):
	image = misc.imread(input_file)

	red = image[:,:,0]
	print(red)
	green = image[:,:,1]

	blue = image[:,:,2]

	#red_bit = np.array(map(bin, red.flatten())).reshape(red.shape)
	red_bit = np.left_shift(red, 1)
	red_bit = np.right_shift(red,1)
	print(red_bit)


	green_bit = np.left_shift(green, 1)
	green_bit = np.right_shift(green,1)

	blue_bit = np.left_shift(blue,1)
	blue_bit = np.right_shift(blue,1)

	reconstruct = red_bit + green_bit + blue_bit

	# fileName = input_file.split('.')[0]

	# fileNameSave = fileName + "_copy.bmp"
	# misc.imsave(fileNameSave, reconstruct)

	matplotlib.pyplot.imshow(reconstruct)
	matplotlib.pyplot.show()


# RGBfactor (sys.argv[1]);
bitManipulation(sys.argv[1])