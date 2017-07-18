#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python label.py [imgdir]
Usage:
d -> delete current label
n -> next picture
q -> exit
'''

import os, sys
import cv2
import numpy as np
import math
import copy
import xml.etree.ElementTree as ET


x1,y1, x2, y2 = 0,0,0,0
state = 0
# ellipse parameter
x0, y0 = 0, 0
angle  = 0
a, b = 0, 0

im = np.zeros((100,100,3))
filename = ""

def onmouse(event, x, y, flags, param):
    global im
    global x1, y1, x2, y2
    global x0, y0, a, b, angle
    global state

    img = im.copy()
    height, width = img.shape[:2]

    # draw two line
    if state == 0:
        # click one
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1 = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            state = 1

    elif state == 1:
        if event == cv2.EVENT_MOUSEMOVE:
            x2, y2 = x, y 
            cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)

        # click two
        elif event == cv2.EVENT_LBUTTONDOWN:
            state = 2 

            # compute angle
            x0 = int((x1+x2)/2)
            y0 = int((y1+y2)/2)
            if x1 != x2 and y1 != y2:
                angle = math.atan((y1-y2)/(x1-x2))/math.pi * 180
            elif x1 != x2:
                angle = 90
            elif y1 != y2:
                angle = 0

            cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)


    elif state == 2:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        # click three
        if event == cv2.EVENT_MOUSEMOVE:
            a = int(math.sqrt((x1-x2)**2 + (y1-y2)**2)/2)
            # compute Ax+By+1=0
            A = (y1-y2)/(x1*y2-x2*y1)
            B = -1*(x1-x2)/(x1*y2-x2*y1)
            dist = abs(A*x + B*y + 1)/math.sqrt(A**2 + B**2)
            b = int(dist)
            cv2.ellipse(img,(x0,y0),(a, b), angle, 0,360, (0,255,255))

        if event == cv2.EVENT_LBUTTONDOWN:
            state = 3

    elif state == 3:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.ellipse(img,(x0,y0),(a, b), angle, 0,360, (0,255,255))

    cv2.imshow('img', img)

def clear():
    global x1, y1, x2, y2
    global x0, y0, a, b, angle
    global state

    x1,y1, x2, y2 = 0,0,0,0
    x0, y0 = 0, 0
    angle  = 0
    a, b = 0, 0
    state = 0


# xml template
Annnotation = """<annotation>
	<folder>FetalHead</folder>
	<filename>{}</filename>
	<source>
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
		<flickrid>341012865</flickrid>
	</source>
	<size>
		<width>{}</width>
		<height>{}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
        {}
</annotation>
"""
Object = """
	<object>
		<name>{}</name>
		<pose>Left</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
                        <x>{}</x>
                        <y>{}</y>
                        <a>{}</a>
                        <b>{}</b>
                        <angle>{}</angle>
		</bndbox>
	</object>
"""


def save(annodir):
    global x0, y0, a, b, angle
    global filename
    global im

    height, width = im.shape[:2] 
    name = 'head'
    newObj = copy.deepcopy(Object).format(name, int(x0), int(y0), int(a), int(b), int(angle))
    newAnno = copy.deepcopy(Annnotation).format(filename, width, height, newObj)
    xmlfile = os.path.join(annodir, '{}.xml'.format(filename))

    print('annodir:', annodir)
    print("xmlfile:", xmlfile)

    if os.path.exists(xmlfile):
        os.remove(xmlfile)
    with open(xmlfile, 'w') as fid:
        fid.write(newAnno)
    print('Image No. {} saved.'.format(eval(filename)))
    

def load(xmlfile):
    global x0, y0, a, b, angle
    global im
    img = im.copy()

    tree = ET.parse(xmlfile)
    width = int(tree.find('size').find('width').text)
    height = int(tree.find('size').find('height').text)
    objs = tree.findall('object')
    for index, obj in enumerate(objs):
        name = obj.find('name').text.lower()
        bbox = obj.find('bndbox')
        x0 = int(bbox.find('x').text)
        y0 = int(bbox.find('y').text)
        a = int(bbox.find('a').text)
        b = int(bbox.find('b').text)
        angle = int(bbox.find('angle').text)
        cv2.ellipse(img,(x0,y0),(a, b), angle, 0,360, (0,255,255))
    cv2.imshow('img', img)


def label(argv):
    root = os.path.abspath(argv[1])
    if not os.path.exists(os.path.join(root, 'JPEGImages')):
        print("Use https://github.com/DuinoDu/BBox-Label-Tool/blob/master/tools/createDS.py to convert images to voc-format")
        return

    imgdir = os.path.join(root, 'JPEGImages')
    imgfiles = sorted([os.path.join(imgdir, x) for x in sorted(os.listdir(imgdir)) if x.endswith('.JPG') or x.endswith('.jpg')])

    annodir = os.path.join(root, 'Annotations')
    if not os.path.exists(annodir):
        os.makedirs(annodir)
    
    global im
    global filename
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', onmouse)

    #for f in imgfiles:
    while True:
        img_ind = 0
        if img_ind >= len(imgfiles):
            print("Finish.")
            break
        img_ind = 0 if img_ind < 0 else img_ind

        f = imgfiles[img_ind]
        print(f)
        filename = os.path.basename(f)[:-4]
        im = cv2.imread(f)
        xmlfile = os.path.join(annodir, '{}.xml'.format(filename))
        if os.path.exists(xmlfile):
            load(xmlfile)
        else:
            cv2.imshow('img', im)

        while True:
            ch = cv2.waitKey(0) & 0xff
            if ch == ord('q'):
                break
            elif ch == ord('n'):
                save(annodir)
                clear()
                img_ind += 1
                break
            elif ch == ord('b'):
                save(annodir)
                clear()
                img_ind -= 1
                break
            elif ch == ord('d'):
                im = cv2.imread(f)
                cv2.imshow('img', im)
                clear()

        if ch == ord('q'):
            break

def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    label(sys.argv)

if __name__ == "__main__":
    main()
