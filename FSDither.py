from PIL import Image

#open image in 8 bit black and white
im = Image.open('test3.jpg').convert('L')

#converts to pixel map
mat = im.load()

#creates result image and direct quantified image

result = Image.new('1',im.size,im.width) 
res = result.load()

quantified = Image.new('1',im.size,im.width) 
quant = quantified.load()

for r in range(im.size[1]):
	for c in range(im.size[0]):
		if(mat[c,r]<128):
			quant[c,r]=0
		else:
			quant[c,r]=255

#checks pixels are in range
def inRange((x,y)):
	if x<im.width and y<im.height and x>0 and y>0:
		return True
	else:
		return False

for r in range(im.size[1]):
	for c in range(im.size[0]):
		if(mat[c,r]<128):
			res[c,r]=0
		else:
			res[c,r]=255
		error = mat[c,r]-res[c,r]
		if inRange((c+1,r)):
			mat[c+1,r] += 7*error/16
		if inRange((c+1,r+1)):
			mat[c+1,r+1] += error/16
		if inRange((c,r+1)):
			mat[c,r+1] += 5*error/16
		if inRange((c-1,r+1)):
			mat[c-1,r+1] += 3*error/16
			
result.show()
result.save("fsDither.tiff")
quantified.show()
quantified.save("uniformQuant.tiff")
