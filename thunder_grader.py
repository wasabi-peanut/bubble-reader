# thunder_grader.py

from imutils.perspective import four_point_transform
from imutils import contours
from skimage.filters import threshold_adaptive
from skimage import img_as_ubyte
import numpy as np
import imutils
import cv2
import math

# SHEET READING CONSTANTS
k_leftBoxDimensions = (0,0)
k_leftBoxGrid = (0,0)
k_rightBoxDimensions = (0,0)
k_rightBoxGrid = (0,0)



def prepPhoto(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edgeMap = cv2.Canny(blurred, 75, 200)
	return (edgeMap, gray)


def getPaper(edgeMap, gray, image):
	cnts = cv2.findContours(edgeMap.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	targetCnt = None

	if len(cnts) > 0:
		# sort the contours according to their size in
		# descending order
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

		
		for c in cnts:
			# approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.1 * peri, True)

			# if our approximated contour has four points,
			# then we can assume we have found the target
			if len(approx) == 4:
				targetCnt = approx
				break

	# apply a four point perspective transform to the
	# paper images to obtain a rectilinear view of the paper
	# print(type(targetCnt.reshape(4, 2)))
	warped = four_point_transform(gray, targetCnt.reshape(4, 2))
	paper = four_point_transform(gray, targetCnt.reshape(4, 2))
	# apply scikit adaptive threshold to image.
	# this is better than a threshold if there is varied lighting on the paper
	thresh = img_as_ubyte(threshold_adaptive(warped, 257, offset = 10))
	return (thresh, paper)

def getColumns(paper):
	thresh = img_as_ubyte(threshold_adaptive(paper, 15, offset = 10))
	(_, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# cv2.imshow("debug", cv2.drawContours(cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR), cnts, -1, (255,0,0), 1))
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
	markerCnts = sorted(markerCnts, key=cv2.contourArea, reverse=True)[:6]

	display = cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR)
	cv2.drawContours(display, markerCnts, -1, (0,255,0), -1)
	cv2.line(display, (len(display[0])//2, 0), ((len(display[0])//2), len(display)), (0,0,255), 3)
	# cv2.imshow("current markers", display)
	if len(markerCnts):
		markerCnts = contours.sort_contours(markerCnts, method="left-to-right")
		leftCnts = markerCnts[0][:4]
		rightCnts = markerCnts[0][2:]
		if len(leftCnts) and len(rightCnts):
			# print(len(markerCnts[0]))

			#  1   2
			#
			#
			#  3   4

			cL1 = contours.sort_contours(leftCnts[:2], method="top-to-bottom")[0][0]
			cL2 = contours.sort_contours(leftCnts[2:], method="top-to-bottom")[0][0]
			cL3 = contours.sort_contours(leftCnts[2:], method="top-to-bottom")[0][1]
			cL4 = contours.sort_contours(leftCnts[:2], method="top-to-bottom")[0][1]

			pL1 = list(max(cL1, key=(lambda c : c[0][0] + c[0][1]))[0])
			pL2 = list(max(cL2, key=(lambda c : c[0][1] - c[0][0]))[0])
			pL3 = list(min(cL3, key=(lambda c : c[0][0] + c[0][1]))[0])
			pL4 = list(max(cL4, key=(lambda c : c[0][0] - c[0][1]))[0])


			cR1 = contours.sort_contours(rightCnts[:2], method="top-to-bottom")[0][0]
			cR2 = contours.sort_contours(rightCnts[2:], method="top-to-bottom")[0][0]
			cR3 = contours.sort_contours(rightCnts[2:], method="top-to-bottom")[0][1]
			cR4 = contours.sort_contours(rightCnts[:2], method="top-to-bottom")[0][1]

			pR1 = list(max(cR1, key=(lambda c : c[0][0] + c[0][1]))[0])
			pR2 = list(max(cR2, key=(lambda c : c[0][1] - c[0][0]))[0])
			pR3 = list(min(cR3, key=(lambda c : c[0][0] + c[0][1]))[0])
			pR4 = list(max(cR4, key=(lambda c : c[0][0] - c[0][1]))[0])

			# print(pL1)
			bubbleThresh = img_as_ubyte(threshold_adaptive(paper, 257, offset = 10))
			
			leftBox = np.array([pL1, pL2, pL3, pL4])
			rightBox = np.array([pR1, pR2, pR3, pR4])

			# print(leftBox)

			left  = four_point_transform(bubbleThresh, leftBox)
			right = four_point_transform(bubbleThresh, rightBox)


			display = cv2.cvtColor(paper.copy(), cv2.COLOR_GRAY2BGR)

			cv2.line(display, tuple(pL1), tuple(pL2), (0,0,255), 3)
			cv2.line(display, tuple(pL2), tuple(pL3), (0,0,255), 3)
			cv2.line(display, tuple(pL3), tuple(pL4), (0,0,255), 3)
			cv2.line(display, tuple(pL4), tuple(pL1), (0,0,255), 3)

			cv2.line(display, tuple(pR1), tuple(pR2), (255,0,0), 3)
			cv2.line(display, tuple(pR2), tuple(pR3), (255,0,0), 3)
			cv2.line(display, tuple(pR3), tuple(pR4), (255,0,0), 3)
			cv2.line(display, tuple(pR4), tuple(pR1), (255,0,0), 3)

			cv2.imshow("OUTPUT", display)

			return (left, right)

		return None

def cutGrid(image, columns, rows):
	sections = []
	rowHeight = len(image) // columns
	colWidth = len(image[0]) // rows
	for r in range(1, columns + 1):
		rowImg = image[  (r-1)*rowHeight : r * rowHeight  ]
		row = []
		for c in range(1, rows + 1):
			bubble = rowImg[ : , (c-1)*colWidth : c * colWidth  ]
			row.append(bubble)
		sections.append(row)
	return sections


def getBubbles(left, right):
	left = cv2.resize(left, (203,260))
	right = cv2.resize(right, (100,350))

	# left = left[26:255, 20:140]
	cv2.cvtColor(left, cv2.COLOR_GRAY2BGR)
	# cv2.imshow("left cropped", left)

	cv2.cvtColor(right, cv2.COLOR_GRAY2BGR)
	# cv2.imshow("right cropped", right)

	bubblesLeft  = cutGrid(left, 15, 8)
	bubblesRight =  cutGrid(right, 15, 3)
	kernel = np.ones((2,2), np.uint8)

	shadesLeft = []
	for row in bubblesLeft:
		shadeRow = []
		for bubble in row:
			_, bubble = cv2.threshold(bubble,127,255,cv2.THRESH_BINARY)
			shade = cv2.countNonZero(bubble)
			shadeRow.append((shade / (len(bubble) * len(bubble[0]))) < 0.7)
		shadesLeft.append(shadeRow)
	
	shadesRight = []

	for row in bubblesRight:
		shadeRow = []
		for bubble in row:
			_, bubble = cv2.threshold(bubble,127,255,cv2.THRESH_BINARY)
			shade = cv2.countNonZero(bubble)
			shadeRow.append((shade / (len(bubble) * len(bubble[0]))) < 0.8)
		shadesRight.append(shadeRow)

	cv2.imshow("left bubbles", bubbleDisplay(left, shadesLeft, 15, 8))
	cv2.imshow("right bubbles", bubbleDisplay(right, shadesRight, 15, 3))

	# print( "LEFT:")
	# print( prettyPrintBubbles(shadesLeft) )
	# print( "RIGHT:" )
	# print( prettyPrintBubbles(shadesRight) )

	return (shadesLeft, shadesRight)

def bubbleDisplay(image, bubbles, rows, columns):
	output = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)
	# cv2.rectangle(output, (0,0), (100,100), (255,0,0), 10)
	x = 0
	y = 0
	dx = len(image[0]) / columns
	print("width: %d, columns: %d, dx: %f" % (len(image[0]), columns, dx))
	dy = len(image) / rows
	print(len(image[0]))
	print(dx)
	print(len(image))
	print(dy)
	cease = False

	while not cease:
		# roi = image[math.floor(y*dy):math.floor((y+1)*dy), math.floor(x*dx):math.floor((x+1)*dx)]
		# roi2 = roi.copy()
		# cv2.imshow("roi", roi)
		# print(cv2.countNonZero(roi) / (len(roi) * len(roi[0])))
		# cv2.waitKey(0)
		color = (0,255,0) if bubbles[y][x] else (255,0,0)
		thickness = 3 if bubbles[y][x] else 1
		cv2.rectangle(output, (math.floor(x*dx), math.floor(y*dy)), (math.floor((x+1)*dx), math.floor((y+1)*dy)), color, thickness)
		# cv2.imshow("progress", output)
		x+=1
		if (x >= len(bubbles[0])):
			y+=1
			x=0
		cease = (y >= len(bubbles))
	return output


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

def writeDataToCSV(data):
	print("SAVING...")
	with open('data.csv', 'a') as f:
		line = ""
		for item in data:
			line+="\"" + str(item)+"\", "
		print(line)
		f.write(line+ "\n")

def boolArrToInt(arr):
	print([str(int(x)) for x in list(np.array(arr).flatten())])
	return int("".join([str(int(x)) for x in list(np.array(arr).flatten())]))

def boolArrToRating(arr):
	arr = list(np.array(arr).flatten())
	rating = 0
	if any(arr):
		for x in arr:
			rating+=1
			if x:
				return rating
	return rating
def boolArrToSum(arr):
	return sum(int(x) for x in list(np.array(arr).flatten()))

def processMatchScout(bubbles):
	

	#METADATA
	scoutID = boolArrToInt(bubbles[1][1:3])
	scoutTable = {
		0: "NO NAME",
		1: "Alex",
		10: "Elaina",
		100: "Taya",
		1000: "Jazmyne",
		10000: "Owen",
		100000: "Ella",
		110000: "Gabby",
		101000: "Dani"
	}
	scoutName = scoutTable[scoutID]
	compID = boolArrToInt(bubbles[1][6])
	compTable = {
		0: "PRACTICE",
		11: "SCOUTING TEST",
		1: "UTAH REGIONAL",
		10: "COLORADO REGIONAL",
		100: "HOUSTON"
	}
	compName = compTable[compID]
	botID = boolArrToInt(bubbles[1][8:10])
	matchID = boolArrToInt(bubbles[1][11:14])
		
	#AUTONOMOUS

	driveForward = [row[0] for row in bubbles[0][12:14]]
	dfString = "NO ATTEMPT"
	if driveForward[0]:
		dfString = "SUCCESS"
	elif driveForward[1]:
		dfString = "FAIL"

	switch = [row[2:4] for row in bubbles[0][12:14]]
	swString = str(boolArrToSum(switch[0]))
	swAttemptString = str(boolArrToSum(switch[0]) + boolArrToSum(switch[1]))

	scale = [row[5:7] for row in bubbles[0][12:14]]
	scString = str(boolArrToSum(scale[0]))
	scAttemptString = str(boolArrToSum(scale[0]) + boolArrToSum(scale[1]))

	autoIntookCubesString = str(boolArrToSum(bubbles[0][10]))



	#TELEOP
	climb = boolArrToInt(bubbles[0][1][3:])
	print(bubbles[0][1][3:])
	climbTable = {
	1000: "LEVITATED",
	1001: "ASSISTED FROM OFF PLATFORM",
	1011: "ASSISTED FROM PLATFORM",
	1100: "FAILED CLIMB",
	1101: "FAILED ASSISTED CLIMB",
	  10: "PLATFORM, NO CLIMB",
	1010: "SUCCESSFUL CLIMB"}
	climbString = climbTable[climb]

	cubeCounts = bubbles[0][2:6]
	scTeleopString  = str(boolArrToSum(cubeCounts[0][3:]))
	swTeleopString  = str(boolArrToSum(cubeCounts[1][3:]))
	oswTeleopString = str(boolArrToSum(cubeCounts[2][3:]))
	exTeleopString  = str(boolArrToSum(cubeCounts[3]))

	fieldConfigString = str(boolArrToInt(bubbles[0][6][:3]))
	startPosString = str(boolArrToInt(bubbles[0][6][5:]))
	cubeRatingString = str(boolArrToRating(bubbles[0][7][:4]))	
	foulsString = str(boolArrToSum(bubbles[0][7][5:]))
	droppedCubesString = str(boolArrToSum(bubbles[0][8]))
	intookCubesTeleopString = str(boolArrToSum(bubbles[0][9]))



	# SCOUT | TEAM | COMP | MATCH | CROSSLINE | AUTO SWITCH | AUTO SCALE | AUTO INTAKE | TELEOP SWITCH | TELEOP SCALE | TELEOP OTHER SWITCH | TELOP EXCHANGE | FIELD CONFIG | START POS | FOULS | DROPPED/FUMBLED CUBES | TELEOP INTAKE | CLIMB STATUS
	writeDataToCSV([scoutName, botID, compName, matchID, dfString, swString + "/" + swAttemptString, scString + "/" + scAttemptString, autoIntookCubesString, swTeleopString, scTeleopString, oswTeleopString, exTeleopString, fieldConfigString, startPosString, foulsString, droppedCubesString, intookCubesTeleopString, climbString])





def photoBooth(live=False, key=32):
	cap = cv2.VideoCapture(0)
	shades = ()
	bubbles = []
	while True:
		try:
			_, img = cap.read()
			keypress = cv2.waitKey(10)
			processed = []
			if (keypress == key) or live:
				processed = getPaper(*prepPhoto(img), img)
				columns = getColumns(processed[1])
				if columns:
					bubbles = getBubbles(*columns)
					# processMatchScout(bubbles)
			elif (keypress == 109):
				processMatchScout(bubbles)	
			cv2.imshow("Webcam", img)
		except Exception as e:
			print("ERROR:")
			print(e)

if __name__ == '__main__':
	photoBooth()
