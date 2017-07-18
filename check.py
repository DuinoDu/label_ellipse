#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python check.py [voc-format ds path]
'''
import os, sys
import cv2
import numpy as np
import xml.etree.ElementTree as ET


def load(imgfile, xmlfile, ind):
    img = cv2.imread(imgfile)
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
    cv2.puttext(img, str(ind), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
    cv2.imshow('img', img)
    ch = cv2.waitKey(1000) & 0xff


def check(argv):
    root = os.path.abspath(argv[1])
    imgdir = os.path.join(root, 'JPEGImages')
    annodir = os.path.join(root, 'Annotations')
    imgfiles = sorted([os.path.join(imgdir, x) for x in sorted(os.listdir(imgdir)) if x.endswith('.jpg')])
    xmlfiles = sorted([os.path.join(annodir, x) for x in sorted(os.listdir(annodir)) if x.endswith('.xml')])

    for ind in range(len(xmlfiles)):
        imgfile = imgfiles[ind]
        xmlfile = xmlfiles[ind]
        load(imgfile, xmlfile, ind)


def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    check(sys.argv)

if __name__ == "__main__":
    main()
