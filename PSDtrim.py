import math
import json
from psd_tools import PSDImage
import sys
from PIL import Image
from PIL import ImageColor
global atlas

def start():
	psd = PSDImage.load(sys.argv[1])
	textfile = open("offsets.txt", "w")
	parse_and_save(psd,textfile)
	textfile.close()

def parse_and_save(psd,textfile):
	global atlas
	global taken_pixels

	images = []
	layers = []
	atlas = Image.new("RGBA",(1000,2000),'hotpink')
	taken_pixels = [0] * atlas.width * atlas.height
	
	paste_posx = 0
	z_order = 0	

	#create a list of image object and a list of meta data voor the images, sort from large to small
	for layer in psd.layers:
		images.append(layer.as_PIL())
		layers.append({"z_order":z_order,"area":layer.bbox.width * layer.bbox.height, "filename":layer.name,"x":layer.bbox.x1,"y":layer.bbox.y1,"width":layer.bbox.width})
		z_order += 1	
	layers = sorted(layers, key=lambda k: k['area'],reverse=True) 

	#find where to paste image and then mark spot as taken
	for somelayer in layers:
		print 'looping over layer: ', somelayer['filename']
		index = somelayer['z_order'] 
		empty_pixel_number = find_empty_pixel(somelayer['width'])
		empty_x = int(empty_pixel_number % atlas.width)
		empty_y = int(math.ceil(empty_pixel_number / atlas.width))
		print ( "pasting " + somelayer['filename'] + ' at x=' + str(empty_x) + " y=" + str(empty_y))
		atlas.paste(images[index],(empty_x,empty_y))
		mark_taken(empty_pixel_number,images[index].width,images[index].height)

	#save
	atlas.save('atlas.png')
	textfile.write(json.dumps(layers,indent=4,sort_keys=True))

#find a spot with enough space to fit width of image
def find_empty_pixel(width):
	global atlas
	global taken_pixels
	i = 0 
	while (i < (atlas.width * atlas.height)):
		pix_from_value = taken_pixels[i]
		pix_to_value = taken_pixels[i + width]
		if (pix_from_value==0 and pix_to_value==0): #topleft and topright both empty - maybe not fully safe?
			if (math.ceil( i / atlas.width) == math.ceil( ( i + width ) / atlas.width)): #on same row
				print "found a spot at " + str(i) + "  between pix1 = " + str(i) + " and pix2 = " + str(i + width) 
				return i
		i = i + 1
	print 'end of while loop'
	return 0
		


def mark_taken(pixelnumber,width,height):
	global taken_pixels
	global atlas
	start = pixelnumber
	end = pixelnumber + (atlas.width * height)
	step = atlas.width
	for i in range(start,end,step):
		for j in range(i,i+width):
			taken_pixels[j]=1


	





start()
