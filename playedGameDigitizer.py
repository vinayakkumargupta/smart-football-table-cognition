from collections import deque
import cv2 as cv
import argparse
import imutils
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("a", nargs='?', default="empty")
args = parser.parse_args()

if args.a == 'empty':
    greenLower = (0,0,0)
    greenUpper = (0,0,0)
else:
    x = args.a.split(",")
    hsvminh = int(x[0])
    hsvmins = int(x[1])
    hsvminv = int(x[2])
    hsvmaxh = int(x[3])
    hsvmaxs = int(x[4])
    hsvmaxv = int(x[5])
    greenLower = (hsvminh,hsvmins,hsvminv)
    greenUpper = (hsvmaxh,hsvmaxs,hsvmaxv)


frameSize = 800

pts = deque(maxlen=20000)

pts.appendleft((0, 0, time.time()))
pts.appendleft((0, 0, time.time()))

cap = cv.VideoCapture(1)

cap.set(28, 0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = imutils.resize(frame, width=frameSize)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, greenLower, greenUpper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]), time.time())

        if radius > 1:
            cv.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)
            cv.circle(frame, (center[0], center[1]), 5, (0, 0, 255), -1)

    if(center == None):
        center = (-1, -1, time.time())
    pts.appendleft(center)

    if pts[0] is None or pts[1] is None:
        actualPointX, actualPointY = 0, 0
        previousPointX, previousPointY = 0, 0
    else:
        actualPointX = pts[1][0]
        actualPointY = pts[1][1]
        previousPointX = pts[0][0]
        previousPointY = pts[0][1]

    print("1|" + str(time.time()) + "|" + str(actualPointY) + "|" + str(actualPointX))

    # uncomment to see vid through test
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):

        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
