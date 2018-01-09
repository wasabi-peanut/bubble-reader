# thunder_grader.py

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
			approx = cv2.approxPolyDP(c, 0.1 * peri, True)

			# if our approximated contour has four points,
			# then we can assume we have found the paper
			if len(approx) == 4:
				targetCnt = approx
				break

	# apply a four point perspective transform to the
	# paper images to obtain a rectilinear view of the paper
	print(type(targetCnt.reshape(4, 2)))
	warped = four_point_transform(gray, targetCnt.reshape(4, 2))
	paper = four_point_transform(gray, targetCnt.reshape(4, 2))
	# apply scikit adaptive threshold to image.
	# this is better than a threshold if there is varied lighting on the paper
	thresh = img_as_ubyte(threshold_adaptive(warped, 257, offset = 10))
	return (thresh, paper)

def getColumns(paper):
	thresh = img_as_ubyte(threshold_adaptive(paper, 15, offset = 10))
	(_, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("debug", cv2.drawContours(cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR), cnts, -1, (255,0,0), 1))
	cnts = contours.sort_contours(cnts, method="top-to-bottom")[0]


	mask = np.zeros(thresh.shape, dtype="uint8")
	(_, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	validHierarchy, validCnts = [[]], []
	markerCnts = []
	i = 0
	removedIDs = [-1]
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		if ar >= 0.75 and ar <= 1.25 and len(cv2.approxPolyDP(c, 0.1 * cv2.arcLength(c, True), True)) == 4:
			validCnts.append(c)
			validHierarchy[0].append(hierarchy[0][i])
		else:
			removedIDs.append(i)
		i+=1
	i=0


	for c in validCnts:
		if validHierarchy[0][i][3] not in removedIDs:
			markerCnts.append(c)
		i+=1
	markerCnts = sorted(markerCnts, key=cv2.contourArea, reverse=True)[:8]

	display = cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR)
	cv2.drawContours(display, markerCnts, -1, (0,255,0), -1)
	cv2.line(display, (len(display[0])//2, 0), ((len(display[0])//2), len(display)), (0,0,255), 3)
	cv2.imshow("current markers", display)
	if len(markerCnts):
		markerCnts = contours.sort_contours(markerCnts, method="left-to-right")
		leftCnts = markerCnts[0][:4]
		rightCnts = markerCnts[0][4:]
		if len(leftCnts) and len(rightCnts):
			print(len(markerCnts[0]))

			#  1   2
			#
			#
			#  3   4

			cL1 = contours.sort_contours(leftCnts[:2], method="top-to-bottom")[0][0]
			cL2 = contours.sort_contours(leftCnts[2:], method="top-to-bottom")[0][0]
			cL3 = contours.sort_contours(leftCnts[2:], method="top-to-bottom")[0][1]
			cL4 = contours.sort_contours(leftCnts[:2], method="top-to-bottom")[0][1]

			pL1 = list(min(cL1, key=(lambda c : c[0][0] + c[0][1]))[0])
			pL2 = list(min(cL2, key=(lambda c : c[0][1] - c[0][0]))[0])
			pL3 = list(max(cL3, key=(lambda c : c[0][0] + c[0][1]))[0])
			pL4 = list(min(cL4, key=(lambda c : c[0][0] - c[0][1]))[0])


			cR1 = contours.sort_contours(rightCnts[:2], method="top-to-bottom")[0][0]
			cR2 = contours.sort_contours(rightCnts[2:], method="top-to-bottom")[0][0]
			cR3 = contours.sort_contours(rightCnts[2:], method="top-to-bottom")[0][1]
			cR4 = contours.sort_contours(rightCnts[:2], method="top-to-bottom")[0][1]

			pR1 = list(min(cR1, key=(lambda c : c[0][0] + c[0][1]))[0])
			pR2 = list(min(cR2, key=(lambda c : c[0][1] - c[0][0]))[0])
			pR3 = list(max(cR3, key=(lambda c : c[0][0] + c[0][1]))[0])
			pR4 = list(min(cR4, key=(lambda c : c[0][0] - c[0][1]))[0])

			print(pL1)
			bubbleThresh = img_as_ubyte(threshold_adaptive(paper, 257, offset = 10))
			
			leftBox = np.array([pL1, pL2, pL3, pL4])
			rightBox = np.array([pR1, pR2, pR3, pR4])

			print(leftBox)

			left  = four_point_transform(bubbleThresh, leftBox)
			right = four_point_transform(bubbleThresh, rightBox)

			return (left, right)
		return None


		# CODE THAT DRAWS BOXES
		# example = cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR)

		# cv2.line(example, pL1, pL2, (0,0,255), 3)
		# cv2.line(example, pL2, pL3, (0,0,255), 3)
		# cv2.line(example, pL3, pL4, (0,0,255), 3)
		# cv2.line(example, pL4, pL1, (0,0,255), 3)

		# cv2.line(example, pR1, pR2, (255,0,0), 3)
		# cv2.line(example, pR2, pR3, (255,0,0), 3)
		# cv2.line(example, pR3, pR4, (255,0,0), 3)
		# cv2.line(example, pR4, pR1, (255,0,0), 3)

		# cv2.imshow("example", example)

def cutGrid(image, rows, columns):
	sections = []
	rowHeight = len(image) // rows
	colWidth = len(image[0]) // columns
	for r in range(1, rows + 1):
		rowImg = image[  (r-1)*rowHeight : r * rowHeight  ]
		row = []
		for c in range(1, columns + 1):
			bubble = rowImg[ : , (c-1)*colWidth : c * colWidth  ]
			row.append(bubble)
		sections.append(row)
	return sections


def getBubbles(left, right):
	left = cv2.resize(left, (80,140))
	right = cv2.resize(right, (80,140))

	left = left[15:125, 10:70]
	cv2.cvtColor(left, cv2.COLOR_GRAY2BGR)
	cv2.imshow("left cropped", left)

	right = right[15:125, 10:70]
	cv2.cvtColor(right, cv2.COLOR_GRAY2BGR)
	cv2.imshow("right cropped", right)

	bubblesLeft  = cutGrid(left, 10, 5)
	bubblesRight =  cutGrid(right, 10, 5)
	kernel = np.ones((2,2), np.uint8)

	shadesLeft = []

	for row in bubblesLeft:
		shadeRow = []
		for bubble in row:
			_, bubble = cv2.threshold(bubble,127,255,cv2.THRESH_BINARY)
			shade = cv2.countNonZero(bubble)
			shadeRow.append(shade < 100)
		shadesLeft.append(shadeRow)
	
	shadesRight = []

	for row in bubblesRight:
		shadeRow = []
		for bubble in row:
			_, bubble = cv2.threshold(bubble, 127, 255, cv2.THRESH_BINARY)
			shade = cv2.countNonZero(bubble)
			shadeRow.append(shade < 100)
		shadesRight.append(shadeRow)

	print( "LEFT:")
	print( prettyPrintBubbles(shadesLeft) )
	print( "RIGHT:" )
	print( prettyPrintBubbles(shadesRight) )


def prettyPrintBubbles(shades):
	prettyString = ""
	for row in shades:
		for s in row:
			if s:
				prettyString += "| X |"
			else:
				prettyString += "|   |"
		prettyString += "\n"
	return prettyString



def photoBooth(live=False, key=32):
	cap = cv2.VideoCapture(0)
	while True:
		_, img = cap.read()
		keypress = cv2.waitKey(10)
		processed = []
		if (keypress == key) or live:
			processed = getPaper(*prepPhoto(img), img)
			columns = getColumns(processed[1])
			if columns:
				getBubbles(*columns)
		cv2.imshow("Webcam", img)


photoBooth()



