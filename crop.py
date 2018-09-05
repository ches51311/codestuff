#coding: utf-8

from PIL import Image
from lxml import etree
import os

medicineyo="vitamin_C"

jpegimg = "/home/swimdi/Desktop/med_crop/"+medicineyo+"/JPEGImages"
anno = "/home/swimdi/Desktop/med_crop/"+medicineyo+"/Annotations"
save_dir = "/home/swimdi/Desktop/med_crop/"+medicineyo+"_crop"
num=0



for dirname, dirnames, filenames in os.walk(anno):
    for filename in filenames:
        jpegpath = jpegimg+"/"+filename.rstrip(".xml")+".jpg"
        annopath = anno+"/"+filename
        tree = etree.parse(annopath)
        name=[]
        xmin=[]
        ymin=[]
        xmax=[]
        ymax=[]

        for item in tree.xpath("//object/name"):
            name.append(item.text)
        for item in tree.xpath("//object/bndbox/xmin"):
            xmin.append(item.text)
        for item in tree.xpath("//object/bndbox/ymin"):
            ymin.append(item.text)
        for item in tree.xpath("//object/bndbox/xmax"):
            xmax.append(item.text)
        for item in tree.xpath("//object/bndbox/ymax"):
            ymax.append(item.text)
        if len(name)>0:
            i=0
            im = Image.open(jpegpath)
            for na in name:
                region = im.crop((int(xmin[i]),int(ymin[i]),int(xmax[i]),int(ymax[i])))
                region.save(save_dir+"/"+na+str(num)+".jpg")
                num=num+1
                i=i+1



#            medname = item.xpath("/name").text
#            aa = item.xpath("//bndbox/xmin").text
#            print aa
#            for xyitem in item.xpath("//bndbox"):
#                print xyitem.text







#for dirname, dirnames, filenames in os.walk(jpegimg):
 #   for filename in filenames:
  #      print os.path.join(dirname, filename)+"\n"
