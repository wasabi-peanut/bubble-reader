import thunder_grader

# GRID SIZE CONSTANTS- GRID SIZE IS (rows, columns), DIMENSIONS IS (width, height).
# TWEAK DIMENSIONS TO ROUGHLY ASPECT RATIO OF BUBBLE AREA, BIGGER IS BETTER AND SLOWER

leftBoxDimensions = (203,260)
leftBoxGrid = (15, 8)
leftThresh = 0.7

rightBoxDimensions = (100,350)
rightBoxGrid = (15, 3)
rightThresh = 0.8

# THE REST ARE FOR PARSING THE BUBBLES.
# BY DEFAULT, WHAT YOU RETURN WILL BE WRITTEN TO "data.csv"
# RETURN None IF YOU WANT TO DOME SOMETHING ELSE

scoutTable = {
		0:		"NO NAME",
		1:		"Alex",
		10:		"Elaina",
		100:	"Taya",
		1000:	"Jazmyne",
		10000:	"Owen",
		100000:	"Ella",
		110000:	"Gabby",
		101000:	"Dani",
		111000:	"Julia"
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

def processMatchScout(bubbles):
	

	#METADATA
	scoutID = thunder_grader.boolArrToBinary(bubbles[1][1:3])
	scoutName = scoutTable[scoutID]
	compID = thunder_grader.boolArrToBinary(bubbles[1][6])
	compName = compTable[compID]
	teamID = thunder_grader.boolArrToBinary(bubbles[1][8:10])
	teamName = teamIDTable[teamID]
	matchID = thunder_grader.boolArrToBinary(bubbles[1][11:14])
	
		
	#AUTONOMOUS

	driveForward = [row[0] for row in bubbles[0][12:14]]
	dfString = "NO ATTEMPT"
	if driveForward[0]:
		dfString = "SUCCESS"
	elif driveForward[1]:
		dfString = "FAIL"

	switch = [row[2:4] for row in bubbles[0][12:14]]
	swString = str(thunder_grader.boolArrToSum(switch[0]))
	swAttemptString = str(thunder_grader.boolArrToSum(switch[0]) + thunder_grader.boolArrToSum(switch[1]))

	scale = [row[5:7] for row in bubbles[0][12:14]]
	scString = str(thunder_grader.boolArrToSum(scale[0]))
	scAttemptString = str(thunder_grader.boolArrToSum(scale[0]) + thunder_grader.boolArrToSum(scale[1]))

	autoIntookCubesString = str(thunder_grader.boolArrToSum(bubbles[0][10]))



	#TELEOP
	climb = thunder_grader.boolArrToBinary(bubbles[0][1][3:])
	print(bubbles[0][1][3:])
	climbTable = {
		1000: "LEVITATED",
		1001: "ASSISTED FROM OFF PLATFORM",
		1011: "ASSISTED FROM PLATFORM",
		1100: "FAILED CLIMB",
		1101: "FAILED ASSISTED CLIMB",
		  10: "PLATFORM, NO CLIMB",
		1010: "SUCCESSSSFUL CLIMB"
	}
	climbString = climbTable[climb]

	cubeCounts = bubbles[0][2:6]
	scTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[0][3:]))
	swTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[1][3:]))
	oswTeleopString = str(thunder_grader.boolArrToSum(cubeCounts[2][3:]))
	exTeleopString  = str(thunder_grader.boolArrToSum(cubeCounts[3]))

	fieldConfigString = str(thunder_grader.boolArrToBinary(bubbles[0][6][:3]))
	startPosString = str(thunder_grader.boolArrToBinary(bubbles[0][6][5:]))
	cubeRatingString = str(thunder_grader.boolArrToRating(bubbles[0][7][:4]))	
	foulsString = str(thunder_grader.boolArrToSum(bubbles[0][7][5:]))
	droppedCubesString = str(thunder_grader.boolArrToSum(bubbles[0][8]))
	intookCubesTeleopString = str(thunder_grader.boolArrToSum(bubbles[0][9]))



	# SCOUT | TEAM | COMP | MATCH | CROSSLINE | AUTO SWITCH | AUTO SCALE | AUTO INTAKE | TELEOP SWITCH | TELEOP SCALE | TELEOP OTHER SWITCH | TELOP EXCHANGE | FIELD CONFIG | START POS | FOULS | DROPPED/FUMBLED CUBES | TELEOP INTAKE | CLIMB STATUS
	return [scoutName, teamName, compName, matchID, dfString, swString + "/" + swAttemptString, scString + "/" + scAttemptString, autoIntookCubesString, swTeleopString, scTeleopString, oswTeleopString, exTeleopString, fieldConfigString, startPosString, foulsString, droppedCubesString, intookCubesTeleopString, climbString]
