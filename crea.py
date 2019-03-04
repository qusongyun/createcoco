import json
import os
import cv2
import shutil
import xml.etree.ElementTree as ET
dataset = {}
def readxml(dataset,xml,count,classes):
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
		'category_id': classes.index(ca_name) + 1,
		'id':1
		})
        

im_path="/home/qusongyun/data_training/"
trainimg = "/home/qusongyun/CornerNet/data/coco/images/trainval2014/"

classes = [ 'boat5', 'car9', 'riding7', 'person17', 'person8', 'group2', 'person28', 'wakeboard3', 'boat2', 'truck1', 
			'building2', 'wakeboard4', 'riding9', 'car24', 'car1', 'person22', 'riding3', 'group3', 'person3', 'car10', 
		   'drone1', 'person11', 'boat4', 'boat1', 'person1', 'riding15', 'person18', 'person19', 'wakeboard1', 
		   'boat3', 'drone2', 'person23', 'car22', 'boat8', 'person21', 'person6', 'car6', 'riding1', 'riding5', 
		   'wakeboard2', 'boat7', 'car16', 'car11', 'horseride1', 'riding2', 'person29', 'drone4', 'car12', 'whale1', 
		   'riding11', 'person9', 'person14', 'car3', 'car14', 'building1', 'person16', 'person26', 'paraglider1',
		    'car4', 'boat6', 'building3', 'car21', 'car18', 'person25', 'riding17', 'riding14', 'car20', 'person2', 
		    'person13', 'car8', 'person12', 'riding13', 'person24', 'riding4', 'riding10', 'car19', 'person10', 
		    'riding6', 'person7', 'person20', 'person4', 'car13', 'riding16', 'car5', 'car23', 'riding8', 'drone3', 
		    'car15', 'person27', 'person15', 'truck2', 'car17', 'riding12', 'car2', 'person5']	

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
			readxml(dataset,os.path.join(im_path + imgdir , file.split(".")[0] + ".xml"),count+cmax,classes)
			count += 1
			
for i, name in enumerate(classes, 1):
	dataset.setdefault("categories",[]).append({
		'id': i, 
		'name':name,
		'supercategory': 'None'
		})

folder = os.path.join('/home/qusongyun/CornerNet/data/coco/annotations/')
if not os.path.exists(folder):
	os.makedirs(folder)
json_name = os.path.join(folder+'instances_trainval2014.json')
with open(json_name, 'w') as f:
	json.dump(dataset, f)
