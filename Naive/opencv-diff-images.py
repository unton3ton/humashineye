import numpy 
import cv2 
import imutils 
 
def compareOnCanvas(imagePath1, imagePath2): 
    img1 = cv2.imread(imagePath1) 
    img2 = cv2.imread(imagePath2) 
 
    img1 = imutils.resize(img1, height=640, width=480) 
    img2 = imutils.resize(img2, height=640, width=480) 
 
    diff = cv2.absdiff(img1, img2) 
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
 
    th = 1 
    imask = mask > th 
 
    canvas = numpy.zeros_like(img2, numpy.uint8) 
    canvas[imask] = img2[imask] 
 
    cv2.imshow("Differences on canvas", canvas) 
    cv2.imwrite("changesOnCanvas.png", canvas) 
    cv2.waitKey(0) 
    cv2.destroyWindow("Differences on canvas") 
 
 
def compareWithAreas(imagePath1, imagePath2): 
    original = cv2.imread(imagePath1) 
    new = cv2.imread(imagePath2) 
 
    original = imutils.resize(original, height=640, width=480) 
    new = imutils.resize(new, height=640, width=480) 
 
    diff = original.copy() 
    cv2.absdiff(original, new, diff) 
 
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
 
    for i in range(0, 3): 
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1) 
 
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY) 
 
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
    cnts = imutils.grab_contours(cnts) 
 
    for c in cnts: 
        (x, y, w, h) = cv2.boundingRect(c) 
        cv2.rectangle(new, (x, y), (x + w, y + h), (0, 0, 255), 2) 
 
    cv2.imshow("Differences with areas", new) 
    cv2.imwrite("changesWithAreas.png", new) 
    cv2.waitKey(0) 
    cv2.destroyWindow("Differences with areas") 
 
 
im1Path = "norma1.jpg" 
im2Path = "speckled.jpg" 
 
compareOnCanvas(im1Path, im2Path) 
compareWithAreas(im1Path, im2Path)