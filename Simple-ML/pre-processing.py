#!/usr/bin/env python
# coding: utf-8

# In[4]:



import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')

img = cv.imread("speckled.0.jpg") # Read image
assert img is not None, "file could not be read, check with os.path.exists()"

# Setting All parameters
t_lower = 50  # Lower Threshold
t_upper = 100  # Upper threshold
aperture_size = 5  # Aperture size

edges = cv.Canny(img, t_lower, t_upper, 
                 apertureSize=aperture_size)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()


# In[ ]:




