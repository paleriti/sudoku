"""9x9 Sudoku, by Yasar Murat, yasarmurat@msn.com

A logic-based, combinatorial number-placement puzzle."""

import random, copy, sys

# Constants used for displaying the board:
EMPTY_SPACE = " " 
BOARD_ROW_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')
BOARD_COLOMN_LABELS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
BOARD_WIDTH = 9
BOARD_HEIGHT = 9
assert BOARD_HEIGHT == 9 and BOARD_WIDTH == 9 # A classic Sudoku board is 9x9 grids

# The string for displaying the board:
BOARD_TEMPLATE = """
    1 2 3 | 4 5 6 | 7 8 9
   _______________________
  |       |       |       |
A | {} {} {} | {} {} {} | {} {} {} |
B | {} {} {} | {} {} {} | {} {} {} |
C | {} {} {} | {} {} {} | {} {} {} |
_ |_______|_______|_______|
  |       |       |       |
D | {} {} {} | {} {} {} | {} {} {} |
E | {} {} {} | {} {} {} | {} {} {} |
F | {} {} {} | {} {} {} | {} {} {} |
_ |_______|_______|_______|
  |       |       |       |
G | {} {} {} | {} {} {} | {} {} {} |
H | {} {} {} | {} {} {} | {} {} {} |
I | {} {} {} | {} {} {} | {} {} {} |
  |_______|_______|_______|
"""

def main():
	"""Runs a single game of Sudoku."""
	 
	print(
        """9x9 Sudoku, by Yasar Murat, yasarmurat@msn.com

Fill a 9x9 grid with digits so that each column, each row, and each of the nine 3x3 subgrids that compose the grid contain all of the digits from 1 to 9 once.
"""
    )
	# Set up the game:
	print("Do you want to load your last board? (Y/N)")
	response = input("> ").upper().strip()
	
	if response == 'Y':
		try:
			oldBoard, remainingSpace = loadOldBoard()
			if remainingSpace == 0:
				print('You completed your last board. Getting you a new one.')
				gameBoard = getNewBoard()
			else:
				gameBoard = oldBoard
		except FileNotFoundError:
			print('There is no saved board. Getting you a new one.')
			gameBoard = getNewBoard()
	else:
		gameBoard = getNewBoard()

	# Save the board to a file for later use.
	saveToFile(gameBoard)
	
	while True:  # Run a player's turn.
        # Display the board:
		displayBoard(gameBoard)
		
		# Get player move
		playerMove = getPlayerMove(gameBoard)

		# Make the move and update the game board accordingly
		colomnIndex = playerMove[0][0]
		rowIndex = playerMove[0][1]
		move = playerMove[1]
		gameBoard[(colomnIndex, rowIndex)] = move
		
		# Save the board to a file for later use after a move.
		saveToFile(gameBoard)
		
		# Check for a complete board
		if isComplete(gameBoard):
			displayBoard(gameBoard) # Display the board one last time.
			print("WELL DONE! You have completed the board.")
			sys.exit()

def loadOldBoard():
	""" Reads a certain file and returns a dictionary that represents the last played Sudoku board. """
	
	with open('Sudoku.sdb', 'r') as fileObj:
		valueStr = fileObj.read()
		
	board = {}
	i = 0
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			try:
				board[(x, y)] = int(valueStr[i])
			except ValueError:
				board[(x, y)] = valueStr[i]
			i += 1
	
	remainingSpaces = int(valueStr[-2] + valueStr[-1])
	
	return board, remainingSpaces

def getNewBoard():
	"""Returns a dictionary that represents a new Sudoku board.
    The keys are (columnIndex, rowIndex) tuples of two integers and the values are integers from 1 to 9 and (empty space) strings."""
    
	# Let player decide the number of empty spaces by offering difficulty levels. """
	while True:
		print('Please select difficulty : (E)asy, (N)ormal, (H)ard')
		response = input("> ").upper().strip()
		
		if response == 'E':
			emptySpace = 20
			break
		elif response == 'N':
			emptySpace = 30
			break
		elif response == 'H':
			emptySpace = 40
			break
		else:
			continue
			
	# First generate a full board with no space, then place empty spaces randomly based on the number of empty spaces.
	fullBoard = getCompleteBoard()
	emptiedBoard = getEmptyCells(fullBoard, emptySpace)
	#emptiedBoard = getEmptyCells(copy.copy(fullBoard), emptySpace)
	
	return emptiedBoard
	
def getCompleteBoard():
	"""Returns a dictionary that represents a new complete Sudoku board.
    The keys are (columnIndex, rowIndex) tuples of two integers and the values are the digits from 1 to 9"""

	# Fill the board with zeros for starting point to work with on.
	fullBoard = {}
	for row in range(BOARD_HEIGHT):
		for colomn in range(BOARD_WIDTH):
			fullBoard[(colomn, row)] = 0
	
	rowIndex = 0
	while True:
		colomnIndex = 0
		while True:
			digit = random.randint(1,BOARD_WIDTH)
			possibleDigits = getPossibleNumbers(fullBoard, colomnIndex, rowIndex)
			if len(possibleDigits) > 0:
				if digit in possibleDigits:
					fullBoard[(colomnIndex, rowIndex)] = digit
					colomnIndex += 1
					if colomnIndex == BOARD_WIDTH :
						break
				else:
					continue
			else:
				for x in range(BOARD_WIDTH): 
					fullBoard[(x, rowIndex)] = 0 # whole row is set to zero to start over
				colomnIndex = 0
				continue
		rowIndex += 1
		if rowIndex == BOARD_HEIGHT:
			break
	
	return fullBoard

def getEmptyCells(board, difficulty):
	""" Takes the current board, places random empty cells and returns the board with empty cells for game play. """
	
	NUM_OF_EMPTY_SPACE = difficulty
	spaces = 0
	emptyCells = []
	
	while True:
		cell = (random.randint(0, 8), random.randint(0, 8))
		
		# Makes sure the number of empty cells that are placed is matched with the level of difficulty.
		if cell in emptyCells: 		
			continue
		else:
			emptyCells.append(cell)
			board[cell] = EMPTY_SPACE
			spaces += 1
			if spaces == NUM_OF_EMPTY_SPACE:
				break

	return board

def displayBoard(board):
	"""Display the board and its cells on the screen.
	
	Prepare a list to pass to the format() string method for the board template. 
	The list holds all of the board's digits (and empty spaces) going left to right, top to bottom:
"""

	gridChars = []
	for rowIndex in range(BOARD_HEIGHT):
		for colomnIndex in range(BOARD_WIDTH):
			gridChars.append(board[(colomnIndex, rowIndex)])

	# Display the board.
	print(BOARD_TEMPLATE.format(*gridChars))

def saveToFile(board):
	""" Takes the board as parameter and converts its values into one string value and then writes this string value to a file for later use. """
	
	valueList = list(board.values())
	valueStr = ''
	for i in range(len(valueList)):
		valueStr += str(valueList[i])
		
	# Count the remaining empty spaces on the board and add to valueStr.
	remainingSpaces = 0
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			if board[(x, y)] == EMPTY_SPACE:
				remainingSpaces += 1
	valueStr += '{:02}'.format(remainingSpaces)
		
	with open('Sudoku.sdb', 'w') as fileObj:
		fileObj.write(valueStr)

def isValid(board, colNum, rowNum, num):
	"""Returns True if the generated number is valid for the board, else returns False """
	
	rows= []
	for x in range(BOARD_WIDTH):
		rows.append(board[(x, rowNum)])
	
	colomns = []
	for y in range(BOARD_HEIGHT):
		colomns.append(board[(colNum, y)])
	
	subgrids = []
	x = (colNum // 3) * 3
	y = (rowNum // 3) * 3
	for yy in range(y, y + 3):
		for xx in range(x, x + 3):
			subgrids.append(board[(xx, yy)])
	
	if num in rows: # In Sudoku rules, no number should appear more than once in a row.
		return False
	if num in colomns: # In Sudoku rules, no number should appear more than once in a colomn.
		return False
	if num in subgrids: # In Sudoku rules, no number should appear more than once in a 3x3 subgrid
		return False
	else: 
		return True
	
def getPossibleNumbers(board, colNum, rowNum):
	""" Calculates the possible numbers that can be placed on the cell that user selects based on the current board. """
	
	possibleNumbers = []
	
	for i in range(1, BOARD_WIDTH + 1):
		if isValid(board, colNum, rowNum, i):
			possibleNumbers.append(i)
			
	return possibleNumbers

def getPlayerCell(board):
	"""Let a player select a cell on the board.

    Returns a tuple which contains (column, row) that the player selected to make a guess. """

	print("Please select the cell you want to make a guess or Q for QUIT:")
	while True:  # Keep asking player until they enter a valid move.
		response = input("> ").upper().strip()

		if response.startswith('Q'):
			print("Thanks for playing!")
			input('Press ENTER to exit.')
			sys.exit()

		# Rename colomn and row for easy use.
		selectedColomn = int(response[1]) - 1
		selectedRow = BOARD_ROW_LABELS.index(response[0])
		selectedCell = (selectedColomn, selectedRow)
		
		if len(response) != 2:
			print('Please use this format when you select your cell : A1 or c3')
			continue # Ask player again for their move.
			
		if not response[0] in BOARD_ROW_LABELS:
			print('Your selected cell must start with a valid letter (ie. from A to I)')
			continue  # Ask player again for their move.
			
		if not int(response[1]) in BOARD_COLOMN_LABELS:
			print('Your selected cell must end with a valid number (ie. from 1 to 9)')
			continue # Ask player again for their move.
		
		if board[selectedCell] != EMPTY_SPACE:
			print('Please select an empty cell')
			continue # Ask player again for their move.
		
		return selectedCell

def getPlayerGuess(board, cell):
	"""Let player make a guess for their selected cell on the board."""

	while True:  # Keep asking player until they enter a valid move.
	
		# Rename the colomn and row index in selected cell for easy use.
		colomn = cell[0]
		row = cell[1]
		
		cellName = str(BOARD_ROW_LABELS[row]) + str(colomn + 1) # Used in comments that are showed to player.
		
		possibleNumbers = getPossibleNumbers(board, colomn, row)
		
		print(f'Please choose: Enter a single digit for [ {cellName} ], show (H)int, change (C)ell or (Q)uit')
			
		response = input("> ").upper().strip()
	
		if len(response) != 1:
			print('Please choose: Enter a single digit, show (H)int, change (C)ell or (Q)uit ')
			continue # Ask player again for their move.

		if response.startswith('Q'):
			print("Thanks for playing!")
			input('Press ENTER to exit.')
			sys.exit()
			
		if response.startswith('H'):
			print(f'Possible numbers for [ {cellName} ] : {possibleNumbers}')
			continue # Ask player again for their move.
		
		if response.startswith('C'):
			cell = getPlayerCell(board)
			continue # Ask player again for their move.
			
		if not int(response) in possibleNumbers:
			print(f'Your guess [ {response} ] is not valid: it is used either in the colomn, row or subgrid.')
			continue # Ask player again for their move.
		
		if response.isdigit(): # A valid response is given
			return cell, int(response)
		
		else:
			continue # Ask player again for their move.
		
def getPlayerMove(board):
	"""Let a player select a cell on the board and make a guess for that cell.

    Returns a list that contain a tuple for (column, row) and the digit that the player selected to make the move. """

	playerMove = []
	
	firstCell = getPlayerCell(board) # Player selects a cell
	print()
	lastCell, guess = getPlayerGuess(board, firstCell) # Player makes a guess for their first cell or changes the cell and makes a guess for their new cell.
	# If player doesn't change the cell, firstCell and lastCell is the same.'
	playerMove.append(lastCell)
	playerMove.append(guess)
	
	return playerMove

def isComplete(board):
	""" Checks whether the board is complete.
	
	Returns True if the board is complete without any empty space, returns False if there is still room for play. """
	
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			if board[(x, y)] == EMPTY_SPACE:
				pn = getPossibleNumbers(board, x, y)
				if len(pn) == 0: # There is no valid move
					print("GAME OVER! You don't have any more valid move")
					displayBoard(board) # Display the board one last time.
					input('Press ENTER to exit!')
					sys.exit()
				else:
					return False
	return True

#  If this program was run (instead of imported), run the game:
if __name__ == "__main__":
    main()