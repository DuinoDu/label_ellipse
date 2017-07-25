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
        x0 = int(bbox.find('x').text)
        y0 = int(bbox.find('y').text)
        a = int(bbox.find('a').text)
        b = int(bbox.find('b').text)
        angle = int(bbox.find('angle').text)
        break
    return width, height, x, y, a, b, angle


def createmask(argv):
    root = os.path.abspath(argv[1])
    annodir = os.path.join(root, 'Annotations')
    maskdir = os.path.join(root, 'JPEGImagesMask')
    if not os.path.exists(maskdir):
        os.makedirs(maskdir)
    annofiles = sorted([os.path.join(annodir, x) for x in sorted(os.listdir(annodir)) if x.endswith('.xml')])
    
    for xmlfile in annofiles:
        w, h, x, y, a, b, angle = parsexml(xmlfile)
        img = np.zeros(shape=(h, w, 1))
        delta = 4
        cv2.ellipse(img, (x, y), (a-delta, b-delta), anble, 0, 360, 255, -1)
        cv2.imshow(img)
        cv2.waitKey(0)
        return




def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    createmask(sys.argv)

if __name__ == "__main__":
    main()
