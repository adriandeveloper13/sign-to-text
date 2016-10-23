import sys
import numpy as np
import cv2

def blackWhiteImage(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh = cv2.threshold(blurred, 150, 255,
        cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return thresh

# im = cv2.imread('./img/fingers.png')
# thresh = blackWhiteImage(im)
# contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]
print("hello")
cap = cv2.VideoCapture(0)
count = 0;
while (cap.isOpened()):
    ret, img = cap.read()
    cv2.imshow('Training', img)
    k = cv2.waitKey(10)
    if (k == 48):
        break
    elif (k != -1):
        thresh = blackWhiteImage(img)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt)>200:
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  h>28:
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    key = cv2.waitKey(10)
                    responses.append(k)
                    cv2.imwrite('./img/test{0}.png'.format(count), img)
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples, sample, 0)
                    count += 1
                    # samples = np.append(samples,sample,0)
                    # if key == 27:  # (escape to quit)
                    #     sys.exit()
                    # elif key in keys:
                    #     responses.append(int(chr(key)))010102010000000
                    #     sample = roismall.reshape((1,100))
                    #     samples = np.append(samples,sample,0)


responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print "training complete"

np.savetxt('./ml_data/generalsamples.data',samples)
np.savetxt('./ml_data/generalresponses.data',responses)