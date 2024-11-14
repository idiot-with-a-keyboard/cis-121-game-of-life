import backend
from PIL import Image, ImageDraw
import io
import random
colblk = (0,0,0)
colwht = (255,255,255)

data = []
with open ("input.txt", "r") as f:
	data = f.readlines()
for i in range(len(data)):
	data[i] = data[i].replace('\n', '')
while '' in data:
	data.remove('')

images = []





'''
for i in range(20):
	im = Image.new('RGB', (50, 50), colblk)
	draw = ImageDraw.Draw(im)
	for i in range(random.randint(5,12)):
		draw.point((random.randint(0,50),random.randint(0,50)),colwht)
	for i in range(10):
		images.append(im)
'''


#
for i in range(10):
	im = Image.new('RGB', (len(data[0]), len(data)), colblk)
	draw = ImageDraw.Draw(im)
	for i in range(len(data)):
		stng = data[i]
		for j in range(len(data[i])):
			if stng[j] == '1':
				draw.point((j,i), colwht)
	draw.point((random.randint(0,5), 1), (255,0,0))
	images.append(im)
	
			





images[0].save('pillow_imagedraw.gif', 
               save_all = True, append_images = images[1:], 
               optimize = False, duration = -1, loop = 0) 

