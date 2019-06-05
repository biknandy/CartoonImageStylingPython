import edgeDetectLoG
import sys
import scipy.misc as skmi
import scipy.ndimage as skim
from skimage import color

def main(fileFull):
	#parse file name
	fileName = fileFull.split('.')[0]
	print fileName

	#open image as array, convert to grayscale if neccessary
	inputIm = skim.imread(fileFull)
	hsvIm = color.rgb2hsv(inputIm)
	hueChannel = hsvIm[:,:,0]
	arrIn = inputIm

	sigmas = [1,3,5,10]

	for i in range(len(sigmas)):
		print 'starting detect: '+str(i)
		result = edgeDetectLoG.edgeDetectLoG(arrIn, sigmas[i])
		print 'saving file: '+str(i)+'\n'
		finName = fileName+'_'+str(i)+'.bmp'
		skmi.imsave(finName,result)

main(sys.argv[1])
#main('lena.jpg')
#main('lena3.bmp')
#main('ucsb.bmp')
#main('up.bmp')