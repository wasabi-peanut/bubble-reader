import thunder_grader
from tkinter import simpledialog
import tkinter as tk

# GRID SIZE CONSTANTS- GRID SIZE IS (rows, columns), DIMENSIONS IS (width, height).
# TWEAK DIMENSIONS TO ROUGHLY ASPECT RATIO OF BUBBLE AREA, BIGGER IS MORE ACCURATE AND SLOWER

matchString = "DEFAULT"

leftBoxDimensions = (203,260)
leftBoxGrid = (15, 8)
leftThresh = 0.95

rightBoxDimensions = (100,350)
rightBoxGrid = (15, 3)
rightThresh = 0.9

# THE REST ARE FOR PARSING THE BUBBLES.

validBubblesLeft = [
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[0,0,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[0,0,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[0,0,0,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,1,1,1,0,0,0,0],
				[0,0,0,0,0,1,1,1],
				[0,0,0,0,0,0,0,0],
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
					[0,1,0],
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
	matchString =	simpledialog.askstring("Input", "Enter Match String:", parent=main)
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
	else:
		print("team id: " + teamID)	
		
	
	#CAPABILITIES
	scaleString = "YES" if bubbles[0][4] else "NO"
	switchString = "YES" if bubbles[0][5] else "NO"
	intakeString = "YES" if bubbles[0][6] else "NO"
	climbString = "YES" if bubbles[0][7] else "NO"
	
	#MECHANISMS
	elevatorString = "YES" if bubbles[1][2] else "NO"
	armString = "YES" if bubbles[1][3] else "NO"
	shooterString = "YES" if bubbles[1][4] else "NO"
	partnerString = "YES" if bubbles[1][5] else "NO"
	intakeString = "ACTIVE" if bubbles[1][6] else ("PASSIVE" if bubbles[1][7] else "NONE")
	
	#DRIVEBASE
	drivebaseString = "NONE"
	if bubbles[0][2]:
		drivebaseString = "KIT"
	if bubbles[0][3]:
		drivebaseString = "H-DRIVE"
	if bubbles[0][4]:
		drivebaseString = "MECANUM"
	if bubbles[0][5]:
		drivebaseString = "SWERVE"
	if bubbles[0][6]:
		drivebaseString = "TRACTION"
	if bubbles[0][7]:
		drivebaseString = "OTHER"
	
	#CLIMBING
	climbPartnerString = thunder_grader.boolArrToRating(bubbles[0][10][6:])
	climbPos = "NONE"
	if bubbles[0][10][3]:
		climbPos = "TUBE"
	if bubbles[0][10][4]:
		climbPos = "TUBE"
	if bubbles[0][10][5]:
		climbPos = "BOX"
	
	#START POS
	startPos = ""
	if bubbles[0][12][1]:
		startPos = "LEFT "
	if bubbles[0][12][2]:
		startPos += "CENTER "
	if bubbles[0][12][3]:
		startPos += "RIGHT "
	if startPos[-1] == " ":
		startPos = startPos[:-1]
		
		
	#PREBUILT
	preBuilt = "NONE"
	if bubbles[0][13][5]:
		preBuilt = "EVERYBOT"
	if bubbles[0][13][6]:
		preBuilt = "GREYT"
	if bubbles[0][13][7]:
		preBuilt = "REV"
		
	#DRIVE FORWARD
	driveForwardString = "YES" if bubbles[1][13][1] else "NO"


	return [scoutName, teamName, compName, scaleString, switchString, intakeString,  climbString, elevatorString, armString, shooterString, climbPartnerString, drivebaseString, climbPos, startPos, preBuilt, driveForwardString]

