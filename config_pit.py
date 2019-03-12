import thunder_grader
from tkinter import simpledialog
import tkinter as tk

# GRID SIZE CONSTANTS- GRID SIZE IS (rows, columns), DIMENSIONS IS (width, height).
# TWEAK DIMENSIONS TO ROUGHLY ASPECT RATIO OF BUBBLE AREA, BIGGER IS MORE ACCURATE AND SLOWER

notesString = "NONE"

leftBoxDimensions = (203,260)
leftBoxGrid = (15, 8)
leftThresh = 0.7

rightBoxDimensions = (100,350)
rightBoxGrid = (15, 3)
rightThresh = 0.7

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
		1001:	"Sophia",
		10000:	"Owen",
		10101:	"Zane",
		100000:	"Julia",
		110000:	"Gabby",
		101000:	"Dani",
		101010:	"Kacey",
		111000:	"Clowie",
		100100:	"Sam S",
		100010:	"Judah",
		100101:	"Ryan",
		110010: "Anai",
		101101: "Theo",
		111010: "Devon"
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

def setNotes():
	global notesString
	notesString =	simpledialog.askstring("Input", "Notes:", parent=main)
	print(str(notesString))



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
		
	print(bubbles[0])

	#CAPABILITIES
	scaleString = "YES" if bubbles[0][1][4] else "NO"
	switchString = "YES" if bubbles[0][1][5] else "NO"
	exchangeString = "YES" if bubbles[0][1][6] else "NO"
	climbString = "YES" if bubbles[0][1][7] else "NO"
	
	#MECHANISMS
	elevatorString = "YES" if bubbles[0][4][2] else "NO"
	armString = "YES" if bubbles[0][4][3] else "NO"
	shooterString = "YES" if bubbles[0][4][4] else "NO"
	partnerString = "YES" if bubbles[0][4][5] else "NO"
	intakeString = "ACTIVE" if bubbles[0][4][6] else ("PASSIVE" if bubbles[1][7] else "NONE")
	
	#DRIVEBASE
	drivebaseString = "NONE"
	if bubbles[0][7][2]:
		drivebaseString = "KIT"
	if bubbles[0][7][3]:
		drivebaseString = "H-DRIVE"
	if bubbles[0][7][4]:
		drivebaseString = "MECANUM"
	if bubbles[0][7][5]:
		drivebaseString = "SWERVE"
	if bubbles[0][7][6]:
		drivebaseString = "TRACTION"
	if bubbles[0][7][7]:
		drivebaseString = "OTHER"
	
	#CLIMBING
	climbPartnerString = thunder_grader.boolArrToRating(bubbles[0][10][6:])
	climbPos = "NONE"
	if bubbles[0][10][3]:
		climbPos = "TUBE"
	if bubbles[0][10][4]:
		climbPos = "BOX"
	if bubbles[0][10][3] and bubbles[0][10][4]:
		climbPos = "TUBE BOX"
	if bubbles[0][10][5]:
		climbPos = "WHOLE"
	
	#START POS
	startPos = ""
	if bubbles[0][12][1]:
		startPos = "LEFT "
	if bubbles[0][12][2]:
		startPos += "CENTER "
	if bubbles[0][12][3]:
		startPos += "RIGHT "
	if len(startPos) and startPos[-1] == " ":
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

	global notesString
	print(notesString)
	return [scoutName, teamName, compName, scaleString, switchString, exchangeString,  climbString, elevatorString, armString, shooterString, intakeString, climbPartnerString, drivebaseString, climbPos, startPos, preBuilt, driveForwardString, notesString]
	notesString = "NONE"

