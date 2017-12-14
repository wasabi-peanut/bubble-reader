# Author: mostly Alex Schor (see below)
# Last Updated: December 13 2017
# NOTE:	I adapted this code from pyimagesearch's bubble sheet code.

# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
from skimage.filters import threshold_adaptive
from skimage import img_as_ubyte
import numpy as np
import imutils
import cv2

def prepPhoto(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edgeMap = cv2.Canny(blurred, 75, 200)
	return (edgeMap, gray)


def getPaper(edgeMap, gray, image):
	# find contours in the edge map, then initialize
	# the contour that corresponds to the document
	cnts = cv2.findContours(edgeMap.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	targetCnt = None

	if len(cnts) > 0:
		# sort the contours according to their size in
		# descending order
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

		# loop over the sorted contours
		for c in cnts:
			# approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)

			# if our approximated contour has four points,
			# then we can assume we have found the paper
			if len(approx) == 4:
				targetCnt = approx
				break

	# apply a four point perspective transform to the
	# paper images to obtain a rectilinear view of the paper
	warped = four_point_transform(gray, targetCnt.reshape(4, 2))
	paper = four_point_transform(gray, targetCnt.reshape(4, 2))
	# apply scikit adaptive threshold to image.
	# this is better than a threshold if there is varied lighting on the paper
	thresh = img_as_ubyte(threshold_adaptive(warped, 301, offset = 10))

	return (thresh, paper)

def scanPaper(thresh, columns):
	# find contours in the thresholded image
	(_, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# the hierarchy gives each contour an ID (its position in cnts) and
	# tells which contours are children of which other contours.
	
	# we keep this so we can make sure no bubble is
	# counted twice (one would be inside the other)

	# initialize some stuff
	validHierarchy, validCnts = [[]], []
	questionCnts = []

	# this loop checks if the bubbles are filled in
	i = 0
	removedIDs = [-1]
	for c in cnts:
		# compute the bounding box and aspect ratio of the contour
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)

		# bubbles must be no more than 20% of screen width and height.
		# bubbles cannot be too small, to account for image noise
		# the bubble's bounding box has to be roughly square
		if w <= thresh.shape[1]*0.2 and h <= thresh.shape[0]*0.2 and w >= 20 and h >= 20 and ar >= 0.75 and ar <= 1.25:
			# if the bubble fits those conditions, the contour is added to the list.
			# the bubble's hierarchy information is added to the hierarchy list
			validCnts.append(c)
			validHierarchy[0].append(hierarchy[0][i])
		else:
			#otherwise the ID is added to the removed list
			removedIDs.append(i)
		i+=1
	i=0


	for c in validCnts:
		# if its parent is either -1 (no parent) or one of the contours that we removed, it's okay.
		# otherwise, it's inside another bubble and is invalid.
		if validHierarchy[0][i][3] in removedIDs:
			questionCnts.append(c)
		i+=1

	# sort the question contours top-to-bottom using imutils
	if len(questionCnts):
		questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

	
	selectedCnts = []
	c = 0
	answers = []
	for (q, i) in enumerate(np.arange(0, len(questionCnts), columns)): # this seperates the contours into rows
		cnts = contours.sort_contours(questionCnts[i:i + columns])[0]
		for (j, cnt) in enumerate(cnts):
			# construct a black image the size of the paper
			mask = np.zeros(thresh.shape, dtype="uint8")
			cv2.drawContours(mask, [cnt], -1, 255, -1)	# fill the contour's shape with white (we're making a mask)
			mask = cv2.bitwise_and(cv2.bitwise_not(thresh), mask) # we invert thresh so darker is bigger numbers
			if cv2.contourArea(cnt) > 0 and (cv2.countNonZero(mask)/cv2.contourArea(cnt) >= 0.75): # 75% seems like a good threshold
				selectedCnts.append(cnt) 
				answers.append((c // columns, c % columns)) # <= math to get the coordinates

			c+=1
	return (answers, questionCnts, selectedCnts)

correct_answers = [(0, 1), (0, 3), (0, 4), (0, 7), (1, 6), (2, 4), (2, 5), (3, 2), (4, 4), (5, 2), (5, 7), (6, 0), (7, 5), (7, 8)]

# if live is true it goes constantly, otherwise it goes when you press a key.
# the key defaults to spacebar (key code 32)

def photoBooth(live=False, key=32):
	cap = cv2.VideoCapture(0)
	while True:
		_, frame = cap.read()
		frame = frame[0:frame.shape[0],frame.shape[1]//2:frame.shape[1]]
		img = frame
		keypress = cv2.waitKey(10)
		if (keypress == key) or live:
			prepped = prepPhoto(img)
			paper = getPaper(*prepped, img)
			thresh = paper[0]
			paper = cv2.cvtColor(paper[1], cv2.COLOR_GRAY2BGR)
			scan = scanPaper(thresh, 9)
			cv2.drawContours(paper, scan[1], -1, (255,0,0), -1)
			cv2.drawContours(paper, scan[2], -1, (0,255,0), -1)
			print(scan[0]) # we should store it somewhere here, not just print it
			cv2.imshow("Answers Found", paper)
		cv2.imshow("Webcam", img)


if __name__ == "__main__":
	photoBooth(live=True)



