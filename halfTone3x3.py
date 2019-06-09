from PIL import Image

#open image in 8 bit black and white
orig = Image.open('test3.jpg').convert('L')

#halftone pattern size
x=3

#check width & height, add black border
imw = orig.size[0]
imh = orig.size[1]

if(orig.size[0]%x!=0):
	imw += x-orig.size[0]%x
if(orig.size[1]%x!=0):
	imh += x-orig.size[1]%x

im = Image.new('L', (imw,imh),0)
im.paste(orig, (0,0))

result = Image.new('1',im.size) 
#converts to pixel map
mat = im.load()
res = result.load()

#halftone operation
for r in range(0,im.size[1],x):
	for c in range(0,im.size[0],x):
		#find avg
		avg = 0.0
		n=0
		for i in range(x):
			for j in range(x):
				avg+=mat[c+i,r+j]
				n+=1
		avg = avg/(n*255)
		
		#match pattern (edit for each x)
		if(avg>0.1):
			res[c,r+2]=255
		if(avg>0.2):
			res[c+1,r]=255
		if(avg>0.3):
			res[c+2,r+1]=255
		if(avg>0.4):
			res[c+1,r+2]=255
		if(avg>0.5):
			res[c,r+1]=255
		if(avg>0.6):
			res[c+2,r]=255
		if(avg>0.7):
			res[c+2,r+2]=255
		if(avg>0.8):
			res[c,r]=255
		if(avg>0.9):
			res[c+1,r+1]=255
result.save("3x3halfTone.tiff")		
result.show()
