#Use fitline?
#goodFeaturesToTrack


#notes
# image size has a huge effect on processing speed.
#cropping matters, but not as much as degrading the image quality.


import numpy as np
import cv2

blurkernel = np.ones((5,5),np.uint8)
dilatekernel = np.ones((5,5),np.uint8)

#cap = cv2.VideoCapture('TEST_VIDEO_FOR_SL_240x320.avi')
cap = cv2.VideoCapture(0)
_, frame0 = cap.read()

#some image degradation steps - may not be necessary.
#topcrop=60


scl=2  			#SCALE DOWN PARAMETER (2 = half)


while(cap.isOpened()):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, blurkernel)	#blur it. resolution is for chumps
    frame=cv2.resize(frame,(0,0),fx=1./scl,fy=1./scl)				#rescale it. 
#    frame=frame3[topcrop:frame3.shape[0],0:frame3.shape[1],:]		#crop it
    # Convert BGR to HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV

    lower_blue = np.array([80,75,75])
    upper_blue = np.array([130,255,255])

    lower_red = np.array([150,75,75])
    upper_red = np.array([200,255,255])

    lower_yellow = np.array([15,50,100])
    upper_yellow = np.array([25,255,255])
    

    # Threshold the HSV image to get only blue colors
    maskblue = cv2.inRange(hsv, lower_blue, upper_blue)
    maskyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskred = cv2.inRange(hsv, lower_red, upper_red)

    # Blank out corners in blue, yellow, that definitely wont have the line.
    # Removed on the grounds it's not obviously useful.. 
#    x, y = np.meshgrid(np.linspace(0,maskblue.shape[1],maskblue.shape[1]), np.linspace(0,maskblue.shape[0],maskblue.shape[0]))
#    diagmask=x<(y*1.0*maskblue.shape[1]/maskblue.shape[0])
#    diagmask=1.0*diagmask.astype(int)
#    maskblue=maskblue*diagmask
#    maskyellow=maskyellow*np.flip(diagmask,1)
#    

	#Apply a dilation - it makes things bigger.. 
    maskyellowdilate = cv2.dilate(maskyellow,dilatekernel,iterations = 1)
    maskbluedilate = cv2.dilate(maskblue,dilatekernel,iterations = 1)
    maskreddilate = cv2.dilate(maskred,dilatekernel,iterations = 1)
    
    #now make it grey, so I can change it to the colour I want.
    
#    red = RGBTransform().mix_with((255, 0, 0),factor=.30).applied_to(lena)  
    
	#Convert type
    maskyellowdilate=maskyellowdilate.astype(frame.dtype)
    maskbluedilate=maskbluedilate.astype(frame.dtype)
    maskreddilate=maskreddilate.astype(frame.dtype)
    

#Build a cumulative mask (abandonded on the grounds we dont need it.)
#    bluebias=((bluebias*(loopcounter-1))+maskbluedilate)/loopcounter
#    yellowbias=((yellowbias*loopcounter-1)+maskyellowdilate)/loopcounter

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=maskyellowdilate+maskbluedilate+maskreddilate)
    red = cv2.bitwise_and(frame,frame, mask=maskreddilate)
    blu = cv2.bitwise_and(frame,frame, mask=maskbluedilate)
    yel = cv2.bitwise_and(frame,frame, mask=maskyellowdilate)
 
    
    cv2.imshow('frame',frame)
    cv2.imshow('res',res)
    cv2.imshow('red',red)
    cv2.imshow('blue',blu)
    cv2.imshow('yel',yel)
    k = cv2.waitKey(50) & 0xFF
    if k == 27:
        break

#cv2.imwrite('bluebias.png',bluebias)
#cv2.imwrite('yellowbias.png',yellowbias)
cap.release()
cv2.destroyAllWindows()
