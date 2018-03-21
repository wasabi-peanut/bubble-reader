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
		0:	"NO NAME",
		1:	"Alex",
		10:	"Elaina",
		100:	"Taya",
		1000:	"Jaymin",
		1001:	"Sophia",
		10000:	"Owen",
		100000:	"Julia",
		110000:	"Gabby",
		101000:	"Dani",
		101010: "Zane",
		111000:	"Clowie",
		100001:	"Hans",
		100100:	"Sam S",		
	}

compTable = {
	0: "PRACTICE",
	11: "SCOUTING TEST",
	1: "UTAH REGIONAL",
	10: "COLORADO REGIONAL",
	100: "HOUSTON"
}

teamIDTable = {
	118: 1,
	10: 148,
	11: 159,
	100: 662,
	101: 698,
	110: 1011,
	111: 1157,
	1000: 1245,
	1001: 1303,
	1010: 1332,
	1011: 1339,
	1100: 1410,
	1101: 1583,
	1110: 1584,
	1111: 1619,
	10000: 1730,
	10001: 1799,
	10010: 1977,
	10011: 2036,
	10100: 2083,
	10101: 2240,
	10110: 2259,
	10111: 2261,
	11000: 2848,
	11001: 2945,
	11010: 2996,
	11011: 3005,
	11100: 3200,
	11101: 3288,
	11110: 3374,
	11111: 3648,
	100000: 3729,
	100001: 3807,
	100010: 4068,
	100011: 4153,
	100100: 4293,
	100101: 4386,
	100110: 4388,
	100111: 4418,
	101000: 4499,
	101001: 4550,
	101010: 4593,
	101011: 4641,
	101100: 4944,
	101101: 5126,
	101110: 5414,
	101111: 5493,
	110000: 5657,
	110001: 5763,
	110010: 5899,
	110011: 6459,
	110100: 7243,
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
		0111: "FAILED CLIMB",
		0101: "FAILED CLIMB",
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
