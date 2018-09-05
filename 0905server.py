from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
from threading import Thread
from ast import literal_eval
import json
import shlex
import os
import numpy as np
import base64

app = Flask(__name__)

ip = "0.0.0.0"
port = 8101
sourcefile = "/home/swimdi/WebAPI/source"


caffe_bin = "/home/swimdi/caffe-ssd/build/examples/ssd/ssd_detect.bin "
deploy = "/home/swimdi/ssd-models-VGGNet/deploy.prototxt "
caffe_model = "/home/swimdi/ssd-models-VGGNet/VGG_VOC0712_SSD_300x300_iter_120000.caffemodel "
pic = "/home/swimdi/Pictures/test.jpg"
solver = ""

commanding = ""



fileimg = ""

@app.route('/command', methods = ['GET', 'POST'])
def command():
    if request.method == 'POST':
        try:
            file = request.files['file']
            global fileimg
            fileimg = "/home/swimdi/Pictures"+secure_filename(file.filename)
            with open(fileimg,'wb+') as img:
                img.write(file.read())
        except IOError:
	    print("Cannot get json file")


@app.route('/source', methods = ['GET', 'POST'])
def source():
    if request.method == 'POST':
        print "hello word, swimdi"
        try:
	    print "hello word, swimdi"



            return jsonify(result)
        except IOError:
	    print("Cannot upload source.")


#really need this?
@app.route('/execute')
def execute():
    if request.method == 'POST':
        print "hello word, swimdi"
        try:
	    cmd = caffe_bin
	    cmd += deploy
	    cmd += caffe_model
	    cmd += fileimg
	    process = Popen(shlex.split(cmd), stdout=PIPE)
	    (output, err) = process.communicate()
	    exit_code = process.wait()
	    print output
            result = {
                     'response': output,
                     'image_sent': 'di' }

            return jsonify(result)
        except IOError:
	    print("Cannot execute command.")




if __name__ == '__main__':
    print("[+] Web API SERVER started on " + ip)
    app.run(debug=False, host=ip, port=port, threaded=True)

