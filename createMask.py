#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python createmask.py [voc-like dir]
'''
import os, sys
import numpy as np
import cv2
import xml.etree.ElementTree as ET

def parsexml(xmlfile):
    tree = ET.parse(xmlfile)
    width = int(tree.find('size').find('width').text)
    height = int(tree.find('size').find('height').text)
    objs = tree.findall('object')
    for index, obj in enumerate(objs):
        name = obj.find('name').text.lower()
        bbox = obj.find('bndbox')
        x = int(bbox.find('x').text)
        y = int(bbox.find('y').text)
        a = int(bbox.find('a').text)
        b = int(bbox.find('b').text)
        angle = int(bbox.find('angle').text)
        break
    return width, height, x, y, a, b, angle


def createmask(argv):
    root = os.path.abspath(argv[1])
    annodir = os.path.join(root, 'Annotations')
    jpegdir = os.path.join(root, 'JPEGImages')
    maskdir = os.path.join(root, 'JPEGImagesMask')
    if not os.path.exists(maskdir):
        os.makedirs(maskdir)
    annofiles = sorted([os.path.join(annodir, x) for x in sorted(os.listdir(annodir)) if x.endswith('.xml')])
    
    for xmlfile in annofiles:
        w, h, x, y, a, b, angle = parsexml(xmlfile)
        delta = 10

        img1 = np.zeros(shape=(h, w, 1))
        cv2.ellipse(img1, (x, y), (a-delta, b-delta), angle, 0, 360, 255, -1)
        img2 = np.zeros(shape=(h, w, 1))
        cv2.ellipse(img2, (x, y), (a+delta, b+delta), angle, 0, 360, 255, -1)
        img_mask = cv2.bitwise_xor(img1, img2)

        
        img = cv2.imread(os.path.join(jpegdir, xmlfile[-10:-4] + '.jpg'))
        img = cv2.bitwise_and(img, img, mask=img_mask)

        cv2.imshow('img', img)
        cv2.waitKey(0)




def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    createmask(sys.argv)

if __name__ == "__main__":
    main()
