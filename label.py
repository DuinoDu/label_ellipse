#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python label.py [imgdir]
'''
import os, sys
import cv2
import numpy as np
import math


x1,y1, x2, y2 = 0,0,0,0
x3,y3, x4, y4 = 0,0,0,0
points = []
k = 0.0
x0, y0 = 0, 0
angle  = 0


state = 0
im = np.zeros((100,100,3))

def onmouse(event, x, y, flags, param):
    global im
    global x1, y1, x2, y2
    global x3, y3, x4, y4
    global points
    global k, x0, y0, angle
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
        # click two
        if event == cv2.EVENT_MOUSEMOVE:
            x2, y2 = x, y 
            cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)

        elif event == cv2.EVENT_LBUTTONDOWN:
            state = 2 

            x0 = int((x1+x2)/2)
            y0 = int((y1+y2)/2)
            if x1 != x2 and y1 != y2:
                k = -1.*(x1-x2)/(y1-y2) 
                y_s1 = int(k*(0-x0) + y0)
                y_s2 = int(k*(width-x0) + y0)
                x_s1 = int((0-y0)/k + x0)
                x_s2 = int((height-y0)/k + x0)

                if y_s1 >= 0 and y_s1 <= height:
                    points.append([0, y_s1])
                if y_s2 >= 0 and y_s2 <= height:
                    points.append([width, y_s2])
                if x_s1 >= 0 and x_s1 <= width:
                    points.append([x_s1, 0])
                if x_s2 >= 0 and x_s2 <= width:
                    points.append([x_s2, height])
                angle = math.atan((y1-y2)/(x1-x2))/math.pi * 180

            elif x1 != x2:
                points.append([x0, 0])
                points.append([x0, height])
                angle = 90
            elif y1 != y2:
                points.append([0, y0])
                points.append([width, y0])
                angle = 0

            cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0,0,255), 1)

    elif state == 2:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0,0,255), 1)
        # click three
        if event == cv2.EVENT_LBUTTONDOWN:
            points[0][0], points[0][1] = x, y
            state = 3

    elif state == 3:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0,0,255), 1)
        # click four
        if event == cv2.EVENT_LBUTTONDOWN:
            points[1][0], points[1][1] = x, y
            state = 4

    elif state == 4:
        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0,0,255), 1)
        a = int(math.sqrt((x1-x2)**2 + (y1-y2)**2)/2)
        b = int(math.sqrt((points[0][0]-points[1][0])**2 + (points[0][1]-points[1][1])**2)/2)
        cv2.ellipse(img,(x0,y0),(a, b), angle, 0,360, (0,255,255))

    cv2.imshow('img', img)


def label(argv):
    root = os.path.abspath(argv[1])
    imgfiles = sorted([os.path.join(root, x) for x in sorted(os.listdir(root)) if x.endswith('.JPG')])
    
    global im
    global x1, y1, x2, y2
    global x3, y3, x4, y4
    global points
    global k, x0, y0
    global state

    cv2.namedWindow('img')
    cv2.setMouseCallback('img', onmouse)

    for f in imgfiles:
        print(f)
        im = cv2.imread(f)
        cv2.imshow('img', im)

        #while True:
        #    ch = cv2.waitKey(0) & 0xff
        #    if ch == ord('q'):
        #        break
        ch = cv2.waitKey(0) & 0xff
        if ch == ord('q'):
            break
        elif ch == ord('n'):
            x1,y1, x2, y2 = 0,0,0,0
            x3,y3, x4, y4 = 0,0,0,0
            points = []
            k = 0.0
            x0, y0 = 0, 0
            angle = 0
            state = 0


state = 0

def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    label(sys.argv)

if __name__ == "__main__":
    main()
