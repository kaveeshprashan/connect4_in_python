import numpy as np
import pygame
import sys
import math
import random
import pygame

BLUE = (100,38,37)
BLACK = (184,143,111)
RED = (223,35,16)
YELLOW = (240,144,29)

ROW_COUNT = 6
COLUMN_COUNT = 7

Player = 0
AI=1

EMPTY = 0
WINDOW_LENGTH=4

Player_turn=1
AI_turn=2

imageRED = pygame.image.load('red.png') 
imageRED = pygame.transform.rotozoom(imageRED, 0,(6/8)*1.1)
imageSLIDE = pygame.image.load('slidebar.jpg') 
imageSLIDE = pygame.transform.rotozoom(imageSLIDE, 0,(6/8))
imageBLUE = pygame.image.load('blue.png') 
imageBLUE = pygame.transform.rotozoom(imageBLUE, 0,(6/8)*1.1)
imageGAME = pygame.image.load('Game.jpg') 
imageGAME = pygame.transform.rotozoom(imageGAME, 0,(6/8))
imageLOSE = pygame.image.load('lose.png') 
imageLOSE = pygame.transform.rotozoom(imageLOSE,0,0.9)
imageWIN = pygame.image.load('winner.png') 
imageWIN = pygame.transform.rotozoom(imageWIN,0,0.6)


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def board_fill():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board
	
def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def show_col(col,position):
	font = pygame.font.SysFont("comicsans", 30, True)	
	if col == None:
		text = font.render("Column : " + "_", 1, (0,0,0))
	else:
		col=col+1
		text = font.render("Column : " + str(col), 1, (0,0,0))
	screen.blit(text, position)

def print_board(board):
	print(np.flip(board, 0))
	
def coordinator(r,c):
	if c==0:
		x=55
	elif c==1:
		x=126
	elif c==2:
		x=197
	elif c==3:
		x=269
	elif c==4:
		x=341
	elif c==5:
		x=412
	else:
		x=484		
	if r==0:
		y= 507
	elif r==1:
		y=433
	elif r==2:
		y=362
	elif r==3:
		y=290
	elif r==4:
		y=219
	else:
		y=147		
	return (x,y)
		

def winning_move(board, turn):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == turn and board[r][c+1] == turn and board[r][c+2] == turn and board[r][c+3] == turn:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == turn and board[r+1][c] == turn and board[r+2][c] == turn and board[r+3][c] == turn:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == turn and board[r+1][c+1] == turn and board[r+2][c+2] == turn and board[r+3][c+3] == turn:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == turn and board[r-1][c+1] == turn and board[r-2][c+2] == turn and board[r-3][c+3] == turn:
				return True
def evaluate_window(window, piece):
	score = 0
	opp_piece = Player_turn
	if piece == Player_turn:
		opp_piece = AI_turn

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, Player_turn) or winning_move(board, AI_turn) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_turn):
				return (None, 100000000000000)
			elif winning_move(board, Player_turn):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_turn))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_turn)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, Player_turn)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col
def draw_board(board,Filled_board,coordinator):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pass

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				if Filled_board[r][c] == 1:
					pass
				else:
					coordinate = coordinator(r,c)
					screen.blit(imageRED, coordinate)
					Filled_board[r][c] = 1
			elif board[r][c] == 2: 
				if Filled_board[r][c] == 1:
					pass
				else:
					coordinate = coordinator(r,c)
					screen.blit(imageBLUE, coordinate)
					Filled_board[r][c] = 1		
	pygame.display.update()
	
	
def columnFinder(posx):
	if 48<=posx<120:
		col = 0
		return col
	elif 120<=posx<195:
		col = 1
		return col
	elif 195<=posx<260:
		col = 2
		return col
	elif 260<=posx<330:
		col = 3
		return col
	elif 330<=posx<400:
		col = 4
		return col
	elif 400<=posx<475:
		col = 5
		return col
	elif 475<=posx<=542:
		col = 6
		return col
	



board = create_board()
Filled_board = board_fill()
# print_board(board)
game_over = False
turn = 0
pygame.init()
SQUARESIZE = 95
width = 600
height = 600
size = (width, height)
# RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
screen.blit(imageGAME, (0, 0)) 

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.MOUSEMOTION:
			screen.blit(imageSLIDE, (0, 0)) 			
			posx = event.pos[0]
			col = columnFinder(posx)
			show_col(col,(420,40))
	
			if turn == 0:
				if 48<posx<542 :
					screen.blit(imageRED, (posx-26, (105*6)/8)) 
			else: 
				if 48<posx<542 :
					screen.blit(imageBLUE, (posx-26, (105*6)/8))
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if turn == Player:
				if 48<posx<542 :
					posx = event.pos[0]
					col = columnFinder(posx)
					
									
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, Player_turn)

					if winning_move(board, Player_turn):
						screen.blit(imageWIN, (140,0))	
						game_over = True
						
				turn += 1
				turn = turn % 2
				print_board(board)
				draw_board(board,Filled_board,coordinator)
					
					
	if turn == AI and not game_over:
# 		col = random.randint(0,COLUMN_COUNT-1)
		col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			pygame.time.wait(1500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_turn)

			if winning_move(board, AI_turn):
				screen.blit(imageLOSE, (110,0))	
				game_over = True


		print_board(board)

		turn += 1
		turn = turn % 2
		draw_board(board,Filled_board,coordinator)

	
pygame.time.wait(4000)
pygame.quit()
sys.exit(1)

			