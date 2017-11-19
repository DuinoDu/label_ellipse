#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import argparse
import os, sys
import cv2
import numpy as np
import math
import copy
import xml.etree.ElementTree as ET
from termcolor import cprint

x1,y1, x2, y2 = 0,0,0,0
state = 0
angle = 0

im = np.zeros((100,100,3))

def onmouse(event, x, y, flags, param):
    global im
    global x1, y1, x2, y2
    global state
    global angle

    img = im.copy()
    height, width = img.shape[:2]

    # draw two points
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
            if x1 != x2 and y1 != y2:
                angle = math.atan((y1-y2)/(x1-x2))/math.pi * 180
                if angle < 0:
                    angle += 180
                angle = round(angle, 1)

            elif x1 != x2: # wired!!!
                angle = 0.0 
            elif y1 != y2:
                angle = 90.0

            cprint(angle, 'green', end=' ')
            print(x1, y1, x2, y2)
    
    if state == 2:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)

    cv2.imshow('img', img)

def clear():
    global x1, y1, x2, y2
    global angle
    global state

    x1,y1, x2, y2 = 0,0,0,0
    state = 0
    angle = 0

def label(args):
    img_ind = 0

    annos_dict = {}
    annofile = os.path.join(args.imgdir, '../annos.txt')
    if os.path.exists(annofile):
        for anno in [x.strip() for x in open(annofile, 'r')]:
            annos_dict[anno.split(' ')[0]] = anno.split(' ')[1:]

    img_ind = len(annos_dict.keys())

    imgfiles = sorted([os.path.join(args.imgdir, x) for x in sorted(os.listdir(args.imgdir)) if x.endswith('.jpg')])

    global im, angle
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', onmouse)


    def resume(img, anno):
        global x1, y1, x2, y2
        global angle
        x1 = int(anno[1])
        y1 = int(anno[2])
        x2 = int(anno[3])
        y2 = int(anno[4])
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        angle = float(anno[0])
        return img


    def save():
        with open(annofile, 'w') as fid:
            for key in sorted(annos_dict.keys()):
                fid.write(key + ' ')
                for c in annos_dict[key]:
                    fid.write(str(c) + ' ')
                fid.write('\n' )
        print('saving to file')


    while True:

        if img_ind >= len(imgfiles):
            print("Finish.")
            break
        img_ind = 0 if img_ind < 0 else img_ind

        f = imgfiles[img_ind]
        filename = f.split('/')[-1]

        im = cv2.imread(f)
        try:
            im = resume(im, annos_dict[imgfiles[img_ind].split('/')[-1]])
            cprint('angle {}'.format(angle), 'green', end=' ')
            print(' || {}/{} || '.format(img_ind+1, len(imgfiles)), filename)

        except Exception as e:
            print('{}/{} || '.format(img_ind, len(imgfiles)), filename)
        cv2.imshow('img', im)


        while True:
            ch = cv2.waitKey(0) & 0xff
            if ch == ord('q'):
                save()
                break

            elif ch == ord('n'):
                annos_dict[filename] = [angle, x1, y1, x2, y2]
                clear()
                if img_ind < len(imgfiles)-1:
                    img_ind += 1
                break

            elif ch == ord('b'):
                annos_dict[filename] = [angle, x1, y1, x2, y2]
                clear()
                if img_ind > 0:
                    img_ind -= 1
                break

            elif ch == ord('d'):
                im = cv2.imread(f)
                cv2.imshow('img', im)
                clear()

            elif ch == ord('s'):
                save()

        if ch == ord('q'):
            break

def main(args):
    label(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Label insulator angle. [d delete] [n next] [b back] [q quit] [s save]')
    parser.add_argument('--imgdir', default='', type=str, help='image path')
    args = parser.parse_args()
    main(args)
