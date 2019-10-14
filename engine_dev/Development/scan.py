from scanner import Transform 
from skimage.filters import threshold_local
import numpy as numpy
import argparse
import cv2
import imutils

# ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image', required = True,
# 	help = 'Path to the image to be scanned')
# args = vars(ap.parse_args())

class scan:
	def __init__(self,image):
		self.image = cv2.imread(image)

	def process(self):
		ratio = self.image.shape[0] / 500.0
		orig = self.image.copy()
		self.image = imutils.resize(self.image,height = 500)
		print(self.image.shape)
		#image processing
		#Step 1. convert to grayscale
		#Step 2. blur image (gaussian)
		#Step 3. utilize Canny edge detection algorithm, uses edge gradients and Sobel kernel

		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5,5), 0)
		edged = cv2.Canny(gray,100,200)

		# print('Edge Detection...\n')
		# cv2.imshow('Image',image)
		# cv2.imshow('Edged',edged)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

		for c in cnts:
			peri = cv2.arcLength(c,True)
			approx = cv2.approxPolyDP(c, 0.01 * peri, True)

			if len(approx) == 4:
				screenCnt = approx
				break

		# print('Contour Detection... ')
		# cv2.drawContours(image,[screenCnt],-1,(255,0,0), 2)
		# cv2.imshow('Outline', image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		screenCnt = screenCnt.reshape(4,2) * ratio
		trans = Transform()	
		warped = trans.four_point_transform(orig,screenCnt)

		#color and post processing
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
		T = threshold_local(warped, 11, offset = 10, method = 'gaussian')
		warped = (warped > T).astype('uint8') * 255

		return warped
		# cv2.imshow('Original',imutils.resize(image,height = 650))
		# cv2.imshow('Transformed',imutils.resize(warped,height = 650))
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
