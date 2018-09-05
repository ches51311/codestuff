#coding: utf8
from datetime import datetime
from threading import Thread
import requests
import json
import shutil
import os
import time
import socket
import base64
import argparse



"""
#train
#detect_img detect_lmdb detect_video detect_
#get_result get_image_list get_status


command = "detect"
command_type = "image"


#image, video, lmdb, training_file
source = "/home/swimdi/Pictures/cat.jpg"



base_url = "http://10.24.120.31:8101"



fileimg = source
files = {'file': open(fileimg,'rb')}
requests.post(url=base_url+"/upload", files=files)



files = {'detect': 'image'}



ret = requests.post(url=base_url+"/detect", files=files)
print ret.json()
"""


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Create AnnotatedDatum database")
  parser.add_argument("root",
      help="The root directory which contains the images and annotations.")

  args = parser.parse_args()
  root_dir = args.root
  print root_dir



















