#put into the sink file and run it

import pdfkit
import os
currentpath = os.getcwd()
prepath = os.path.abspath("..")
loss = currentpath + "/loss.png"
test = currentpath + "/test.png"
log =  currentpath + "/log"
labelmap = prepath + "/labelmap.prototxt"
project_name = prepath.split("/")[-1]
classes = ""
count = -1
with open(labelmap, 'r') as flabel:
    for line in flabel:
        if "display_name" in line:
            count = count + 1
            if count>0:
                classes = classes + ", " + eval(line.split()[1])
classes = classes[1:]
para = []
accuracy = []
with open(log, 'r') as flog:
    for line in flog:
        if "test_iter" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "test_interval" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "base_lr" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "max_iter" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "lr_policy" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "gamma" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "momentum" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "weight_decay" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "solver_mode" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])
        if "eval_type" in line:
            para.append(line.split()[0])
            para.append(line.split()[1])

        if "detection_eval" in line:
            accuracy.append(line[line.find("detection_eval")+16:])


body = ""
body = body + "<html>"
body = body + "<head>"
body = body + "<title></title>"
body = body + "</head>"
body = body + "<body>"
body = body + "<center><font size=\"7\">"+ project_name +"</font></center>"
body = body + "<center><font size=\"6\">class :"+ classes +"</font></center>"
body = body + "<center><img src=\""+ loss +"\" width=\"600\"></center>"
body = body + "<center><img src=\""+ test +"\" width=\"600\"></center>"
body = body + "<br>"
body = body + "<center><font size=\"6\">Accuracy : " +accuracy[-1].strip('\n')+ "</font></center>"
body = body + "<br>"
body = body + "<table style=\"border:3px padding:3px solid\" rules=\"all\" cellpadding=\"5\" align=center>"
body = body + "<tr>"
body = body + "<td width=\"150px\"><font size=\"6\">" +para[6]+ "</font></td>"
body = body + "<td width=\"150px\"><font size=\"6\">" +para[2]+ "</font></td>"
body = body + "<td width=\"150px\"><font size=\"6\">" +para[0]+ "</font></td>"
body = body + "<td width=\"150px\"><font size=\"6\">" +para[10]+ "</font></td>"
body = body + "<td width=\"150px\"><font size=\"6\">" +para[12]+ "</font></td>"
body = body + "</tr>"
body = body + "<tr>"
body = body + "<td><font size=\"6\">" +para[7]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[3]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[1]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[11]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[13]+ "</font></td>"
body = body + "</tr>"
body = body + "<tr>"
body = body + "<td><font size=\"6\">" +para[8]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[16]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[18]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[4]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[14]+ "</font></td>"
body = body + "</tr>"
body = body + "<tr>"
body = body + "<td><font size=\"6\">" +para[9]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[17]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[19]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[5]+ "</font></td>"
body = body + "<td><font size=\"6\">" +para[15]+ "</font></td>"
body = body + "</tr>"
body = body + "</table>"
body = body + "</body>"
body = body + "</html>"


pdfkit.from_string(body,'report.pdf')



