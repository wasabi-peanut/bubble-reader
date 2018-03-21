import thunder_grader
from tkinter import simpledialog
import tkinter as tk

# GRID SIZE CONSTANTS- GRID SIZE IS (rows, columns), DIMENSIONS IS (width, height).
# TWEAK DIMENSIONS TO ROUGHLY ASPECT RATIO OF BUBBLE AREA, BIGGER IS MORE ACCURATE AND SLOWER

matchString = "DEFAULT"

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
				[0,0,1,1,1,1,1,1],
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
	drivebase = "NONE"
	if bubbles[0][2]:
		drivebase = "KIT"
	if bubbles[0][3]:
		drivebase = "H-DRIVE"
	if bubbles[0][4]:
		drivebase = "MECANUM"
	if bubbles[0][5]:
		drivebase = "SWERVE"
	if bubbles[0][6]:
		drivebase = "TRACTION"
	if bubbles[0][7]:
		drivebase = "OTHER"
	
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
	startPos = "NONE"
	if bubbles[0][12][1]:
		startPos = "LEFT"
	if bubbles[0][12][2]:
		startPos = "CENTER"
	if bubbles[0][12][3]:
		startPos = "RIGHT"
		
		
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
