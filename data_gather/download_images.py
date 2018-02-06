from imutils import paths
import argparse
import requests
import cv2
import os
import sys
import re

ap=argparse.ArgumentParser()
ap.add_argument("-u","--urls", required=False,
	help="path to file containing image URLs")
ap.add_argument("-o","--output", required=False,
	help="path to output directory of images")
args=vars(ap.parse_args())

directory_folder=os.path.dirname(os.path.abspath(__file__))

if args['urls'] is None:
	# sets the path of a default url file
	url_path=os.path.join(directory_folder,'urls_folder','urls.txt')
	if not os.path.exists(url_path):
		# if the url.txt file is not in this then it will print this message
		#  then terminate the program
		print("\"url.txt\" not in the folder. Have url.txt file with lists of urls before running")
		sys.exit()
	args['urls']=url_path


if args['output'] is None:
	# sets the path of a default picture folder
	picture_dir=os.path.join(directory_folder,'images','chickens')
	# checks to see if a folder called pictures exists
	if not os.path.isdir(picture_dir):
		# if it doesnt see the folder, it'll make it
		os.makedirs(picture_dir)
		total = 0
	args['output']=picture_dir


# checking to make sure that the folder can be appended
# by checking the format of the last file in the folder\
# if the format of the last file in the folder is set,
# we set total to the number after the number of the last file
picture_list=os.listdir(args['output'])
if picture_list !=[]:
	last=picture_list[-1].strip('.jpg')
	match=re.match(r'\d\d\d\d\d\d\d\d',last)
	if match is None:
		print("picture file is in wrong format. format needs to have 8 digits with leading zeroes")
		sys.exit()
	else:
		match_num=match.group(0)
		if match_num.zfill(8)==last:
			print("format seems good. Moving on")
			total=int(last)
			total+=1
		else:
			print("picture file is in wrong format. format needs to have 8 digits with leading zeroes")
			sys.exit()


# will read in the file as a whole
# .strip will take out any white space from the begingging and end 
rows = open(args["urls"]).read().strip().split("\n")

for url in rows:
	try:
		
		# try to download the image
		r=requests.get(url, timeout=60)
		print(' request is done')

		# save the image to disk
		p=os.path.join(args["output"], "{}.jpg".format(str(total).zfill(8)))
		f=open(p,'wb')
		f.write(r.content)
		f.close()

		# update the counter
		print("[INFO] downloaded: {}".format(p))
		total+=1

	except:
		print("[INFO] error downloading {}...skipping".format(p))


#  loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete=False


	# try to load the image
	try:
		image=cv2.imread(imagePath)

		# if the image is 'None' then we could not properly load it
		# from disk, so delete it
		if image is None:
			delete=True

	# if OpenCV cannot load the image then the image ie likely 
	# corrupt so we should delete it
	except:
		print("Except")
		delete=True

	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)



