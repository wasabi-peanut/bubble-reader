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
rightThresh = 0.9

# THE REST ARE FOR PARSING THE BUBBLES.

validBubblesLeft = [
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,1,1,1,1],
				[0,1,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,1,1,1,1,0,0,0],
				[0,1,1,1,0,0,1,1],
				[0,1,1,1,0,0,1,1],
				[0,1,1,1,0,0,0,1],
				[0,1,1,1,0,0,0,1],
				[0,1,1,1,1,0,0,1],
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
					[0,0,1],
					[0,0,1],
					[0,0,1],
					[0,0,0]
					]


scoutIDTable = {
	1: "Julia S",
	10: "Nick",
	11: "Jonah",
	100: "Noah",
	101: "Jazmyne",
	110: "Devon",
	111: "Aidan",
	1000: "Parker",
	1001: "Gavyn",
	1010: "Isaac",
	1011: "Hagan",
	1100: "Gabby",
	1101: "Owen",
	1110: "Julia D",
	1111: "Vanessa",
	10000: "Sam",
	10001: "Helen",
	10010: "Wes",
	10011: "Andrew",
	10100: "Simon",
	10101: "Cameron",
	10110: "Gabe",
	10111: "Alex",
	11000: "Emma",
	11001: "Thomas",
	11010: "Grady",
}


teamIDTable = {
	1: 60,
	10: 118,
	11: 498,
	100: 670,
	101: 687,
	110: 842,
	111: 991,
	1000: 996,
	1001: 1011,
	1010: 1138,
	1011: 1165,
	1100: 1339,
	1101: 1622,
	1110: 1726,
	1111: 1828,
	10000: 1891,
	10001: 2240,
	10010: 2403,
	10011: 2478,
	10100: 2486,
	10101: 2840,
	10110: 3009,
	10111: 3019,
	11000: 3133,
	11001: 3187,
	11010: 3230,
	11011: 3577,
	11100: 3853,
	11101: 4063,
	11110: 4146,
	11111: 4183,
	100000: 4565,
	100001: 5059,
	100010: 5133,
	100011: 5429,
	100100: 5493,
	100101: 5496,
	100110: 5539,
	100111: 5678,
	101000: 6127,
	101001: 6413,
	101010: 6474,
	101011: 6546,
	101100: 6656,
	101101: 6674,
	101110: 6821,
	101111: 6824,
	110000: 6871,
	110001: 6922,
	110010: 7214,
	110011: 7424,
	110100: 7426,
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
	if scoutID in scoutIDTable:
		scoutName = scoutIDTable[scoutID]

	teamID = thunder_grader.boolArrToBinary(bubbles[1][8:10])
	teamName = str(teamID)
	if teamID in teamIDTable:
		teamName = teamIDTable[teamID]

	#START
	startingPos = ("3" if bubbles[0][12][7] else "") + ("2" if bubbles[0][13][7] else "") + ("1" if bubbles[0][14][7] else "")
	print(bubbles[0][12][7:8])

	botConfig = ("CARGO" if bubbles[0][10][6] else "") + ("HATCH" if bubbles[0][11][6] else "")
	fieldConfig = ("CARGO" if bubbles[0][10][7] else "") + ("HATCH" if bubbles[0][11][7] else "")


	#AUTONOMOUS
	autoRocketCargo = bubbles[0][10][1:4]
	autoRocketHatch = bubbles[0][11][1:4]
	autoCBCargo = bubbles[0][12][1:4]
	autoCBHatch = bubbles[0][13][1:4]
	
	#TELEOP
	teleopRRocketL3 = bubbles[0][0][1:5]
	tRRL3C = sum(teleopRRocketL3[1:3])
	tRRL3H = teleopRRocketL3[0] + teleopRRocketL3[3]

	teleopRRocketL2 = bubbles[0][1][1:5]
	tRRL2C = sum(teleopRRocketL2[1:3])
	tRRL2H = teleopRRocketL2[0] + teleopRRocketL2[3]

	teleopRRocketL1 = bubbles[0][2][1:5]
	tRRL1C = sum(teleopRRocketL1[1:3])
	tRRL1H = teleopRRocketL1[0] + teleopRRocketL1[3]

	teleopLRocketL3 = bubbles[0][3][1:5]
	tLRL3C = sum(teleopLRocketL3[1:3])
	tLRL3H = teleopLRocketL3[0] + teleopLRocketL3[3]

	teleopLRocketL2 = bubbles[0][4][1:5]
	tLRL2C = sum(teleopLRocketL2[1:3])
	tLRL2H = teleopLRocketL2[0] + teleopLRocketL2[3]
	
	teleopLRocketL1 = bubbles[0][5][1:5]
	tLRL1C = sum(teleopLRocketL1[1:3])
	tLRL1H = teleopLRocketL1[0] + teleopLRocketL1[3]
	

	fouls = bubbles[0][14][1:5]


	# SCOUT,TEAM,MATCH,STARTING POS,BOT CONFIG,FIELD CONFIG,STORM ROCKET CARGO,STORM ROCKET HATCH,STORM CB CARGO,STORM CB HATCH,RIGHT ROCKET L3 C,RIGHT ROCKET L3 H,RIGHT ROCKET L2 C,RIGHT ROCKET L2 H,RIGHT ROCKET L1 C,RIGHT ROCKET L2 H,RIGHT ROCKET L1 C,RIGHT ROCKET L1 H,LEFT ROCKET L3 C,LEFT ROCKET L3 H,LEFT ROCKET L2 C,LEFT ROCKET L2 H,LEFT ROCKET L1 C,LEFT ROCKET L2 H,LEFT ROCKET L1 C,LEFT ROCKET L1 H,FOULS

	return [scoutName, teamName, matchString, startingPos, botConfig, fieldConfig, autoRocketCargo, autoRocketHatch, autoCBCargo, autoCBHatch, tRRL3C, tRRL3H, tRRL2C, tRRL2H, tRRL1C, tRRL1H, tLRL3C, tLRL3H, tLRL2C, tLRL2H, tLRL1C, tLRL1H, fouls]
