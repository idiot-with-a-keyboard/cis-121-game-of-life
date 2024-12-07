import backend
#import input.py
from PIL import Image, ImageDraw
import io
import random
colblk = (0,0,0)
colwht = (255,255,255)

#data = backend.grid_list
length = 50


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


'''
for i in range(10):
	im = Image.new('RGB', (len(data[0]), len(data)), colblk)
	draw = ImageDraw.Draw(im)
	for i in range(len(data)):
		stng = data[i]
		for j in range(len(data[i])):
			if stng[j] == '1':
				draw.point((j,i), colwht)
	images.append(im)
'''
#^test cases for the gif creation function


def creategif(steps:list[list[str]], length, width, height):
	for f in range(length-1):
		data = steps[f]
		frame = Image.new('RGB', (width, height), colblk)
		draw = ImageDraw.Draw(frame)
		for y in range(height):
			grid = data[f]
			for x in range(width):
				if data[y][x] == '1':
					draw.point((y,int(x)), colwht)
		images.append(frame)
		images[0].save('animation.gif', 
               save_all = True, append_images = images[1:], 
               optimize = False, duration = -1, loop = 0)
	
