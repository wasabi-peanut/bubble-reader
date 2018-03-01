import thunder_grader
from tkinter import simpledialog
import tkinter as tk

# GRID SIZE CONSTANTS- GRID SIZE IS (rows, columns), DIMENSIONS IS (width, height).
# TWEAK DIMENSIONS TO ROUGHLY ASPECT RATIO OF BUBBLE AREA, BIGGER IS MORE ACCURATE AND SLOWER

matchString = "DEFAULT"

leftBoxDimensions = (203,260)
leftBoxGrid = (15, 8)
leftThresh = 0.8

rightBoxDimensions = (100,350)
rightBoxGrid = (15, 3)
rightThresh = 0.8

# THE REST ARE FOR PARSING THE BUBBLES.

validBubblesLeft = [
				[1,0,0,0,0,0,0,0],
				[0,0,0,0,1,1,1,1],
				[0,0,0,1,1,1,1,1],
				[0,0,0,1,1,1,1,1],
				[0,0,0,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,0,0,1,1,1],
				[1,1,1,1,1,0,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[1,0,1,1,0,1,1,0],
				[1,0,1,1,0,1,1,0],
				[0,0,1,1,0,1,1,0],
				]
validBubblesRight = [
					[0,0,0],
					[1,1,1],
					[1,1,1],
					[0,0,0],
					[0,0,0],
					[0,0,0],
					[1,1,1],
					[0,0,0],
					[1,1,1],
					[1,1,1],
					[0,0,0],
					[0,0,0],
					[0,0,0],
					[0,0,0],
					[0,0,0]
					]


scoutTable = {
		0:		"NO NAME",
		1:		"Alex",
		10:		"Elaina",
		100:	"Taya",
		1000:	"Jazmyne",
		10000:	"Owen",
		100000:	"Julia",
		110000:	"Gabby",
		101000:	"Dani",
		111000:	"Ella"
	}

compTable = {
	0: "PRACTICE",
	11: "SCOUTING TEST",
	1: "UTAH REGIONAL",
	10: "COLORADO REGIONAL",
	100: "HOUSTON"
}

teamIDTable = {
	1: 115,
	10: 159,
	11: 192,
	100: 399,
	101: 662,
	110: 670,
	111: 841,
	1000: 968,
	1001: 1339,
	1010: 1410,
	1011: 1452,
	1100: 1678,
	1101: 1891,
	1110: 2468,
	1111: 2484,
	10000: 2576,
	10001: 2594,
	10010: 2972,
	10011: 2993,
	10100: 2996,
	10101: 3006,
	10110: 3166,
	10111: 3200,
	11000: 3225,
	11001: 3230,
	11010: 3239,
	11011: 3243,
	11100: 3245,
	11101: 3289,
	11110: 3374,
	11111: 3405,
	100000: 3729,
	100001: 4348,
	100010: 4550,
	100011: 4585,
	100100: 4598,
	100101: 4944,
	100110: 5071,
	100111: 5159,
	101000: 5461,
	101001: 5493,
	101010: 5871,
	101011: 5933,
	101100: 5974,
	101101: 6358,
	101110: 6400,
	101111: 6411,
	110000: 6457,
	110001: 6546,
	110010: 6717,
	110011: 6844,
	110100: 7151
}


main = tk.Tk()

def switchMatch():
	global matchString
	matchString =  simpledialog.askstring("Input", "Enter Match String:", parent=main)
	print("New match descriptor: " + str(matchString))

def processMatchScout(bubbles):


	#METADATA
	scoutID = thunder_grader.boolArrToBinary(bubbles[1][1:3])
	scoutName = str(scoutID)
	if scoutID in scoutTable:
		scoutName = scoutTable[scoutID]

	compID = thunder_grader.boolArrToBinary(bubbles[1][6])
	compName = str(compID)
	if compID in compTable:
		compName = compTable[compID]

	teamID = thunder_grader.boolArrToBinary(bubbles[1][8:10])
	teamName = str(teamID)
	if teamID in teamIDTable:
		teamName = teamIDTable[teamID]

	matchID = thunder_grader.boolArrToBinary(bubbles[1][11:14])
	
		
	#AUTONOMOUS

	driveForward = [row[0] for row in bubbles[0][12:14]]
	dfString = "NO ATTEMPT"
	if driveForward[0]:
		dfString = "SUCCESS"
	elif driveForward[1]:
		dfString = "FAIL"

	switch = [row[2:4] for row in bubbles[0][12:]]
	swString = str(thunder_grader.boolArrToSum(switch[0:2]))
	swAttemptString = str(thunder_grader.boolArrToSum(switch))

	scale = [row[5:7] for row in bubbles[0][12:]]
	scString = str(thunder_grader.boolArrToSum(scale[0:2]))
	scAttemptString = str(thunder_grader.boolArrToSum(scale))

	autoIntookCubesString = str(thunder_grader.boolArrToSum(bubbles[0][10]))



	#TELEOP
	climb = thunder_grader.boolArrToBinary(bubbles[0][1][3:])
	print(bubbles[0][1][3:])
	climbTable = {
		   0: "NO ATTEMPT",
		1000: "LEVITATED",
		1011: "SUCCESSFUL ASSISTED CLIMB",
		1001: "SUCCESSFUL ASSISTED CLIMB",
		1100: "FAILED CLIMB",
		1101: "FAILED CLIMB",
		111: "FAILED CLIMB",
		101: "FAILED CLIMB",
		  10: "PLATFORM / NO CLIMB",
		1010: "SUCCESSFUL CLIMB"
	}
	climbString = str(climb)
	if climb in climbTable:
		climbString = climbTable[climb]


	cubeCounts = bubbles[0][2:6]
	scTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[0][3:]))
	swTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[1][3:]))
	oswTeleopString = str(thunder_grader.boolArrToSum(cubeCounts[2][3:]))
	exTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[3]))

	forceString = str(thunder_grader.boolArrToRating(bubbles[1][11:][0]))
	boostString = str(thunder_grader.boolArrToRating(bubbles[1][11:][1]))
	levitateString = str(thunder_grader.boolArrToRating(bubbles[1][11:][2][2]))

	pickListString = str(thunder_grader.boolArrToRating(bubbles[0][0][0]))

	fieldConfig = thunder_grader.boolArrToBinary(bubbles[0][6][:3])
	fieldConfigTable = {
		  0: "OOO",
		111: "SSS",
		101: "SOS",
		 10: "OSO",

	}
	fieldConfigString = str(fieldConfig)
	if fieldConfig in fieldConfigTable:
		fieldConfigString = fieldConfigTable[fieldConfig]


	startPosString = str(thunder_grader.boolArrToRating(bubbles[0][6][5:]))
	cubeRatingString = str(thunder_grader.boolArrToRating(bubbles[0][7][:5]))	
	foulsString = str(thunder_grader.boolArrToSum(bubbles[0][7][6:]))
	droppedCubesString = str(thunder_grader.boolArrToSum(bubbles[0][8]))
	intookCubesTeleopString = str(thunder_grader.boolArrToSum(bubbles[0][9]))

	# SCOUT,TEAM,COMP,MATCH,CROSSLINE,AUTO SWITCH,AUTO SWITCH ATTEMPTS,AUTO SCALE,AUTO SCALE ATTEMPTS,AUTO INTAKE,TELEOP SWITCH,TELEOP SCALE,TELEOP OTHER SWITCH,TELOP EXCHANGE,FIELD CONFIG,START POS,FOULS,DROPPED/FUMBLED CUBES,TELEOP INTAKE,CLIMB STATUS,FORCE,BOOST,LEVITATE,PICK LIST

	return [scoutName, teamName, compName, matchString, dfString, swString, swAttemptString, scString, scAttemptString, autoIntookCubesString, swTeleopString, scTeleopString, oswTeleopString, exTeleopString, fieldConfigString, startPosString, foulsString, droppedCubesString, intookCubesTeleopString, climbString, forceString, boostString, levitateString, pickListString]
