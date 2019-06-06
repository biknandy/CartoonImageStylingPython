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



RGBfactor (sys.argv[1]);