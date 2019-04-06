import json
import os
import cv2
import shutil
import xml.etree.ElementTree as ET
dataset = {}
def readxml(dataset,xml,count):
	tree = ET.parse(xml)
	root = tree.getroot()
	for child in root:
		if child.tag == "size":
			for s_ch in child:
				if s_ch.tag == "width":
					w = s_ch.text
				else :
					h = s_ch.text
		elif child.tag == "object":
			for s_ch in child:
				if s_ch.tag == "bndbox":
					for ss_ch in s_ch:
						if ss_ch.tag == "xmin":
							xmin = ss_ch.text
						elif ss_ch.tag == "ymin":
							ymin = ss_ch.text
						elif ss_ch.tag == "xmax":
							xmax = ss_ch.text
						elif ss_ch.tag == "ymax":
							ymax = ss_ch.text
				else: 
				    ca_name = s_ch.text

	dataset.setdefault("images",[]).append({
		'file_name': str(count) +'.jpg',
		'id': int(count),
		'width': int(w),
		'height': int(h) 
		})
	dataset.setdefault("annotations",[]).append({
		'image_id': int(count),
		'bbox': [int(xmin), int(ymin), int(xmax)-int(xmin), int(ymax)-int(ymin)],
		'category_id': 6,
                'area':int(w) * int(h),
                'iscrowd':0,
                'id':int(count),
                'segmentation':[]
		})
        

im_path="/home/qusongyun/images/"
trainimg = "/home/qusongyun/simpledet/data/coco/images/val2014/"

cmax = 0
dirpath = os.listdir(im_path)
for imgdir in dirpath:

	f1 = os.listdir(trainimg)
	for file in f1:
		cmax = max(cmax,int(file.split(".")[0]))
	count = 1

	for file in os.listdir(im_path + imgdir):

		if file.split(".")[1] == "jpg":
			oldname = os.path.join(im_path + imgdir, file)
			jpgname = os.path.join(trainimg, str(count+cmax) + ".jpg")
			shutil.copyfile(oldname, jpgname)
			readxml(dataset,os.path.join(im_path + imgdir , file.split(".")[0] + ".xml"),count+cmax)
			count += 1
			
for i in range(1,81):
	dataset.setdefault("categories",[]).append({
		'id': i, 
		'name':1,
		'supercategory': 'No'
		})

folder = os.path.join('/home/qusongyun/simpledet/data/coco/annotations/')
if not os.path.exists(folder):
	os.makedirs(folder)
json_name = os.path.join(folder+'instances_minival2014.json')
with open(json_name, 'w') as f:
	json.dump(dataset, f)
