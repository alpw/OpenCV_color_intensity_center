import cv2
import numpy as np

def empty(val):
    pass

#creating trackbars
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640,311)
cv2.createTrackbar("Hue Min", "TrackBars", 20, 255, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 32, 255, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 174, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 68, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 168, 255, empty)

cap = cv2.VideoCapture(0)   # Capturing video from webcaam, if not working: change 0 to 1
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

while True:
    #img = cv2.imread("photo.png")
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #trackbars
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    upperArr = np.array([hue_max, sat_max, val_max])
    lowerArr = np.array([hue_min, sat_min, val_min])
    #you can see the last values in console that you created on trackbars
    print("hue:",hue_min, hue_max, ":sat:", sat_min, sat_max, ":val:", val_min, val_max,":")
    masked = cv2.inRange(imgHSV, lowerArr, upperArr)
    result = cv2.bitwise_and(img, img, mask=masked)

    imgGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("dsaf",imgGray)

    # convert image to grayscale image
    # convert the grayscale image to binary image
    ret, thresh = cv2.threshold(imgGray, 0, 255, 0)
    # calculate moments of binary image
    M = cv2.moments(thresh)
    # calculate x,y coordinate of center
    if not all(x == 0 for x in M.values()):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX = 0
        cY = 0

    # put text and highlight the center
    cv2.putText(img, "centeroid", (cX + 10, cY - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    cv2.line(img, (cX+50, cY), (cX-50, cY), (0,255,0), 3)
    cv2.line(img, (cX, cY+50), (cX, cY-50), (0,255,0), 3)
    # display the image
    cv2.imshow("ImgGray", imgGray)
    cv2.imshow("Image", img)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break