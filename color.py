import sys
from scipy import misc
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np


def main (input_file):
	image = misc.imread(input_file)
	
	factor = 2

	red = image[:,:,0]
	green = image[:,:,1]
	blue = image[:,:,2]

	red_frac = red/factor
	green_frac = green/factor
	blue_frac = blue/factor

	red_r = np.round(red_frac)
	green_r = np.round(green_frac)
	blue_r = np.round(blue_frac)
	

	reconstruct = (factor * red) + (factor * green) + (factor * blue)

	matplotlib.pyplot.imshow(reconstruct)
	matplotlib.pyplot.show()

	# matplotlib.pyplot.imshow(grey, cmap = matplotlib.cm.Greys_r)
	# matplotlib.pyplot.show()



main (sys.argv[1]);