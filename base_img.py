#! /usr/bin/env python3

import os,sys
from PIL import Image

def tool_print(line,text):
	print("\033[7;31;47m"+str(line)+" \033[0m",text)

# split转换
def tool_img2split():
	if not os.path.exists("base_img/base_split"):
		os.makedirs("base_img/base_split")
	if not os.path.exists("base_img/base_a"):
		os.makedirs("base_img/base_a")

	tool_print(str(sys._getframe().f_lineno)+" "+"img2split","...")

	img = Image.open("base_img/base.png")
	r,g,b,a=img.split()
	# img0 = Image.merge('RGB',(g,g,b))
	color_split=[r,g,b]

	for x in range(3):
		for y in range(3):
			for z in range(3):
				if x==y and y==z:
					continue
				else:
					img0 = Image.merge('RGB',(color_split[x],color_split[y],color_split[z]))
					img0.save("base_img/base_split/base_"+str(x)+str(y)+str(z)+".png")
					tool_print(str(sys._getframe().f_lineno)+" "+"generated:","base_split/"+str(x)+str(y)+str(z)+".png")

# 透明背景
def tool_img2a ():
	tool_print(str(sys._getframe().f_lineno)+" "+"img2a","...")
	path = "base_img/base_split"
	files= os.listdir(path)
	for file in files: 
		if not os.path.isdir(file):
			img = Image.open(path+"/"+file).convert("RGBA")
			pixdata = img.load()
			bgcolor = pixdata[1, 1]
			for x in range(img.size[0]):
				for y in range(img.size[1]):
					if pixdata[x, y] ==  bgcolor:
						pixdata[x, y] = (0,0,0, 0)
			img.save("base_img/base_a/"+file)
			tool_print(str(sys._getframe().f_lineno)+" "+"generated","base_a/"+file)

if __name__ == "__main__":
	tool_img2split()
	tool_img2a()