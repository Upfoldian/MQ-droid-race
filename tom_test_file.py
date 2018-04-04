import numpy as np
import cv2
import time



print(cv2.__version__)

cap = cv2.VideoCapture(0)
#Set Resolution (Default is 1344x376, Max is 2560x720)
#cap.set(3, 2560)
#cap.set(4, 720)

# Setting Resolution

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

else:

  
  
  #capture a buncha images from camera
  capTotal = 100
  count = 1
  start = time.time()
  while count < capTotal:
    # Captures a frame frome the camera
    ret, frame = cap.read()
    #Saves it to target dir
    filename = 'gao/test_%d.png' % count
    if ret == True:
      cv2.imwrite(filename, frame)
      count += 1
  
  end = time.time()
  # Time elapsed
  seconds = end - start
  print "Time taken : {0} seconds".format(seconds)
  # Estimated frames per second

  fps  = capTotal / seconds;
  print "Estimated frames per second : {0}".format(fps);

  # Been getting 15 fps at default resolution (camera max at this res is 60fps)
  # Only 4 fps at maximum resolution (camera max at this res is 30fps)
  
cap.release()