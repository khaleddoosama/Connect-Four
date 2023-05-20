import numpy as np
import random
import pygame
import sys
import math




roww = 6
coll = 7


def print_board(board):
    print(np.flip(board, 0))


# Check if a move is a winning move
def winning_move(board, piece):
    # Check horizontal locations for win
    for col in range(coll - 3):
        for row in range(roww):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and \
                    board[row][col + 3] == piece:
                return True

    # Check vertical locations for win
    for col in range(coll):
        for row in range(roww - 3):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and \
                    board[row + 3][col] == piece:
                return True

    # Check positively sloped diagonals
    for col in range(coll - 3):
        for row in range(roww - 3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and \
                    board[row + 3][col + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for col in range(coll - 3):
        for row in range(3, roww):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and \
                    board[row - 3][col + 3] == piece:
                return True

PLAYER_PIECE = 1
artif_intell_piece = 2

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == artif_intell_piece else artif_intell_piece

    piece_count = window.count(piece)
    empty_count = window.count(0)

    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2

    opponent_piece_count = window.count(opponent_piece)
    if opponent_piece_count == 3 and empty_count == 1:
        score -= 4

    return score

WINDOW_LENGTH = 4

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, coll // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3


            
      ## Score Horizontal
    for r in range(roww):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(coll - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
            
        ## Score egative sloped diagonal

    for r in range(roww - 3):
        for c in range(coll - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
            
            
        ## Score posiive sloped diagonal
    for r in range(roww - 3):
        for c in range(coll - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
                    

                
    ## Score Vertical
    for c in range(coll):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(roww - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
            
    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, artif_intell_piece) or len(get_valid_locations(board)) == 0


def drop_piece(board, row, col, piece):
    board[row][col] = piece





# Get the next open row for a move
def get_next_open_row(board, col):
    for row in range(roww):
        if board[row][col] == 0:
            return row



def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, artif_intell_piece):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, artif_intell_piece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, artif_intell_piece)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def is_valid_location(board, col):
    return board[roww - 1][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(coll):
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
        if best_score  <score :
            best_score = score
            best_col = col

    return best_col


color1 = (243, 156, 18)
color2 = (0, 0, 0)
color3 = (208, 211, 212)
color4 = (255, 255, 0)

def draw_board(board):
    for c in range(coll):
        for r in range(roww):
            pygame.draw.rect(screen, color1, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, color2, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(coll):
        for r in range(roww):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, color3, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == artif_intell_piece:
                pygame.draw.circle(screen, color4, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

PLAYER = 0
AI = 1

def create_board():
    return np.zeros((roww, coll))

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = coll * SQUARESIZE
height = (roww + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, color2, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, color3, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, color2, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            # Ask for Player 1 Input
        if turn == PLAYER:
            col = random.randint(0, coll - 1)
            pygame.time.wait(1000)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, color3)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2

        # # Ask for Player 2 Input
        if turn == AI and not game_over:

            pygame.time.wait(1000)
            col = pick_best_move(board, artif_intell_piece)

            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, artif_intell_piece)

                if winning_move(board, artif_intell_piece):
                    label = myfont.render("Player 2 wins!!", 1, color4)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

    if game_over:
        pygame.time.wait(300000)
        break

    if is_terminal_node(board):
        label = myfont.render("Game Over", 1, color3)
        screen.blit(label, (150, 10))
        game_over = True

        pygame.display.update()
        pygame.time.wait(3000)