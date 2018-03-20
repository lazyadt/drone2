import numpy as np
import cv2
from functools import cmp_to_key

im1 = cv2.imread("/home/adu/Documents/take_1/DSC01798.JPG")
im2 = cv2.imread("/home/adu/Documents/take_1/DSC01886.JPG")
im3 = cv2.imread("/home/adu/Documents/take_1/DSC02209.JPG")
im4 = cv2.imread("/home/adu/Documents/take_1/DSC02407.JPG")
im5 = cv2.imread("/home/adu/Documents/take_1/DSC02426.JPG")
#cv2.imshow('image', im1)

#finding contours involves finding white object from black background, so object to be found should be white and background should be black
#convert image to grayscale
imgray1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY) 
imgray2 = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
imgray3 = cv2.cvtColor(im3,cv2.COLOR_BGR2GRAY)
imgray4 = cv2.cvtColor(im4,cv2.COLOR_BGR2GRAY)
imgray5 = cv2.cvtColor(im5,cv2.COLOR_BGR2GRAY)
while True:
	ret1,thresh1 = cv2.threshold(imgray1,127,255,0) 
	ret2,thresh2 = cv2.threshold(imgray2,127,255,0)
	ret3,thresh3 = cv2.threshold(imgray3,127,255,0)
	ret4,thresh4 = cv2.threshold(imgray4,127,255,0)
	ret5,thresh5 = cv2.threshold(imgray5,127,255,0)
#contours is a Python list of all the contours, each contour is a Numpy array of coordinates of boundary points of the object
contours1, hierarchy1 = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy2 = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours3, hierarchy3 = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours4, hierarchy4 = cv2.findContours(thresh4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours5, hierarchy5 = cv2.findContours(thresh5,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


def sortArea(x,y):
    return cv2.contourArea(y) - cv2.contourArea(x) #sort compare function that compares area of each contour
contours1.sort(key=cmp_to_key(sortArea)) #sorts contours by area in descending order
contours2.sort(key=cmp_to_key(sortArea))
contours3.sort(key=cmp_to_key(sortArea))
contours4.sort(key=cmp_to_key(sortArea))
contours5.sort(key=cmp_to_key(sortArea))

#finds 2nd largest contour because largest contour is image itself
maxContour1 = contours1[1] 
maxContour2 = contours2[1] 
maxContour3 = contours3[1] 
maxContour4 = contours4[1] 
maxContour5 = contours5[1] 

#finds rotated rectangle, bounding rectangle is drawn with minimum area, so it considers the rotation as well
#returns a Box2D structure which contains (top-left cornor,(width, height), angle of rotation)
rect1 = cv2.minAreaRect(maxContour1) 
rect2 = cv2.minAreaRect(maxContour2)
rect3 = cv2.minAreaRect(maxContour3)
rect4 = cv2.minAreaRect(maxContour4)
rect5 = cv2.minAreaRect(maxContour5)
#angle of rotation is third element of rect
angleofRotation1 = rect1[2] 
angleofRotation2 = rect2[2]
angleofRotation3 = rect3[2]
angleofRotation4 = rect4[2]
angleofRotation5 = rect5[2]

#fitEllipse finds the orientation, or the angle at which the object is directed,
# it also gives the (x,y) coordinates and the Major Axis (MA) and minor axis (ma) lengths
(x1,y1),(MA1,ma1),angle1 = cv2.fitEllipse(maxContour1) 
(x2,y2),(MA2,ma2),angle2 = cv2.fitEllipse(maxContour2)
(x3,y3),(MA3,ma3),angle3 = cv2.fitEllipse(maxContour3)
(x4,y4),(MA4,ma4),angle4 = cv2.fitEllipse(maxContour4)
(x5,y5),(MA5,ma5),angle5 = cv2.fitEllipse(maxContour5)

#draw a bounding box around the image
box1 = np.int0(cv2.cv.BoxPoints(rect1))
box2 = np.int0(cv2.cv.BoxPoints(rect2))
box3 = np.int0(cv2.cv.BoxPoints(rect3))
box4 = np.int0(cv2.cv.BoxPoints(rect4))
box5 = np.int0(cv2.cv.BoxPoints(rect5))
#draws bounding rectangle
im1 = cv2.drawContours(im1,[box1],0,(0,0,255),2) 
im2 = cv2.drawContours(im2,[box2],0,(0,0,255),2)
im3 = cv2.drawContours(im3,[box3],0,(0,0,255),2)
im4 = cv2.drawContours(im4,[box4],0,(0,0,255),2)
im5 = cv2.drawContours(im5,[box5],0,(0,0,255),2)

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#shows image
cv2.imshow('image', im1) 
cv2.imshow('image', im2)
cv2.imshow('image', im3)
cv2.imshow('image', im4)
cv2.imshow('image', im5)
cv2.waitKey(0) #waits for a pressed key, delay is forever (0 is a special value)
cv2.destroyAllWindows() #distroys windows (in this case 'image')
