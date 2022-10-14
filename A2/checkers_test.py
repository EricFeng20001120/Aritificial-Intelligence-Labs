# Import libraries
from distutils.command.config import config
import numpy
import sys
import copy

# Get arguments from terminal
input_file = sys.argv[1]
output_file = sys.argv[2]

# Create global variables for the num of rows and columns
rows = 8
columns = 8

# Create a list of list for the board
configuration = [[] for x in range(rows)]

# Import the input.txt file and use a nested for loop to store characters
with open(input_file) as file:
    for i in range(rows):
        for j in range(columns):
            configuration[i].append(file.read(1))
        file.read(1)

# Function that finds the coordinates of a specific character given the configuration
def coordinates_locater(piece, config):
    index = []
    for i in range(rows):
        for j in range(columns):
            if config[i][j] == piece:
                index.append((i, j))
    return index

# Cost function
def cost(board, player):
    # Assign a cost
    g_cost = 0
    # Define the opponent, opponent's king and player's king
    if player == 'r':
        opponent = 'b'
        opponent_king = 'B'
        king = 'R'
    elif player == 'b':
        opponent = 'r'
        opponent_king = 'R'
        king = 'B'

    for i in range(rows):
        for j in range(columns):
            # Assign worth of pieces
            if board[i][j] == player:
                g_cost = g_cost + 1
            elif board[i][j] == king:
                g_cost = g_cost + 2 
            elif board[i][j] == opponent:
                g_cost = g_cost - 1
            elif board[i][j] == opponent_king:
                g_cost = g_cost - 2  

    return g_cost

# Jump function
def jump(board, y, x, player):
    path = []
    if player == 'r':
        # Upper right jump
        if x <= 5 and y >= 2 and (board[y-1][x+1] == 'b' or board[y-1][x+1] == 'B') and board[y-2][x+2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y-1][x+1] = '.'
            if y == 2:
                new_board[y-2][x+2] = 'R'
                player = 'R'
                path.append(new_board)
            else:
                new_board[y-2][x+2] = 'r'
                double_jump = jump(new_board, y-2, x+2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
        # Upper left jump
        if x >= 2 and y >= 2 and (board[y-1][x-1] == 'b' or board[y-1][x-1] == 'B') and board[y-2][x-2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y-1][x-1] = '.'
            if y == 2:
                new_board[y-2][x-2] = 'R'
                player = 'R'
                path.append(new_board)
            else:
                new_board[y-2][x-2] = 'r'
                double_jump = jump(new_board, y-2, x-2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)

        elif player == 'b':
            # Bottom right jump
            if x <= 5 and y <= 5 and (board[y+1][x+1] == 'r' or board[y+1][x+1] == 'R') and board[y+2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x+1] = '.'
                if y == 5:
                    new_board[y+2][x+2] = 'B'
                    player = 'B'
                    path.append(new_board)
                else:
                    new_board[y+2][x+2] = 'b'
                    double_jump = jump(new_board, y+2, x+2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)
            # Bottom left jump
            if x >= 2 and y <= 5 and (board[y+1][x-1] == 'r' or board[y+1][x-1] == 'R') and board[y+2][x-2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x-1] = '.'
                if y == 5:
                    new_board[y+2][x-2] = 'B'
                    player = 'B'
                    path.append(new_board)
                else:
                    new_board[y+2][x-2] = 'b'
                    double_jump = jump(new_board, y+2, x-2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)

        elif player == 'R':
            # Upper right jump
            if x <= 5 and y >= 2 and (board[y-1][x+1] == 'b' or board[y-1][x+1] == 'B') and board[y-2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y-1][x+1] = '.'
                new_board[y-2][x+2] = 'R'
                double_jump = jump(new_board, y-2, x+2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Upper left jump
            if x >= 2 and y >= 2 and (board[y-1][x-1] == 'b' or board[y-1][x-1] == 'B') and board[y-2][x-2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y-1][x-1] = '.'
                new_board[y-2][x-2] = 'R'
                double_jump = jump(new_board, y-2, x-2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Bottom right jump
            if x <= 5 and y <= 5 and (board[y+1][x+1] == 'b' or board[y+1][x+1] == 'B') and board[y+2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x+1] = '.'
                new_board[y+2][x+2] = 'R'
                double_jump = jump(new_board, y+2, x+2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Bottom left jump
            if x >= 2 and y <= 5 and (board[y+1][x-1] == 'b' or board[y+1][x-1] == 'B') and board[y+2][x-2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x-1] = '.'
                new_board[y+2][x-2] = 'R'
                double_jump = jump(new_board, y+2, x-2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)

        elif player == 'B':
            # Upper right jump
            if x <= 5 and y >= 2 and (board[y-1][x+1] == 'r' or board[y-1][x+1] == 'R') and board[y-2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y-1][x+1] = '.'
                new_board[y-2][x+2] = 'B'
                double_jump = jump(new_board, y-2, x+2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Upper left jump
            if x >= 2 and y >= 2 and (board[y-1][x-1] == 'r' or board[y-1][x-1] == 'R') and board[y-2][x-2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y-1][x-1] = '.'
                new_board[y-2][x-2] = 'B'
                double_jump = jump(new_board, y-2, x-2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Bottom right jump
            if x <= 5 and y <= 5 and (board[y+1][x+1] == 'r' or board[y+1][x+1] == 'R') and board[y+2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x+1] = '.'
                new_board[y+2][x+2] = 'B'
                double_jump = jump(new_board, y+2, x+2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
            # Bottom left jump
            if x >= 2 and y <= 5 and (board[y+1][x-1] == 'r' or board[y+1][x-1] == 'R') and board[y+2][x-2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y+1][x-1] = '.'
                new_board[y+2][x-2] = 'B'
                double_jump = jump(new_board, y+2, x-2, player)
                tmp = numpy.array(double_jump).squeeze()
                tmp = tmp.tolist()
                if (len(tmp) >= 1):
                    path.append(tmp)
                else:
                    path.append(new_board)
    return path

# Successor function
def successor(board, player):
    path = []
    if player == 'r':
        for i in range(rows):
            for j in range(columns):
                if board[i][j] == 'r':
                    path += jump(board, i, j, board[i][j])
        if path:  
            path = numpy.array(path).squeeze()
            path = path.tolist()
        player_piece = coordinates_locater(player, board)
        for i in player_piece:
            y, x = i[0], i[1]
            if board[y][x] == 'r':
                # Right top diagonal single jump
                if x <= 6 and board[y-1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    if y == 1:
                        new_board[y-1][x+1] = 'R'
                    else:
                        new_board[y-1][x+1] = 'r'
                    path.append(new_board)
                # Left top diagonal single jump
                if x >= 1 and board[y-1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    if y == 1:
                        new_board[y-1][x-1] = 'R'
                    else:
                        new_board[y-1][x-1] = 'r'
                    path.append(new_board)
    elif player == 'R':
        for i in range(rows):
            for j in range(columns):
                if board[i][j] == 'R':
                    path = jump(board, j, i, board[i][j])
        if path:  
            print(numpy.array(path).shape)
            path = numpy.array(path).squeeze()
            path = path.tolist()
        player_piece = coordinates_locater(player, board)
        for i in player_piece:
            y, x = i[0], i[1]
            if board[y][x] == 'R':
                # Right top diagonal single jump
                if x <= 6 and y >= 1 and board[y-1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y-1][x+1] = 'R'
                    path.append(new_board)
                # Left top diagonal single jump
                if x >= 1 and y >= 1 and board[y-1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y-1][x-1] = 'R'
                    path.append(new_board)
                # Right down diagonal single jump
                if x <= 6 and y <= 6 and board[y+1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y+1][x+1] = 'R'
                    path.append(new_board)
                # Left down diagonal single jump
                if x >= 1 and y <= 6 and board[y+1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y+1][x-1] = 'R'
                    path.append(new_board)
    elif player == 'b':
        for i in range(rows):
            for j in range(columns):
                if board[i][j] == 'b':
                    path = jump(board, j, i, board[i][j])
        if path:  
            path = numpy.array(path).squeeze()
            path = path.tolist()
        player_piece = coordinates_locater(player, board)
        for i in player_piece:
            y, x = i[0], i[1]
            if board[y][x] == 'b':
                # Right down diagonal single jump
                if x <= 6 and y <= 6 and board[y+1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    if y == 6:
                        new_board[y+1][x+1] = 'B'
                    else: 
                        new_board[y+1][x+1] = 'b'
                    path.append(new_board)
                # Left down diagonal single jump
                if x >= 1 and y <= 6 and board[y+1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    if y == 6:
                        new_board[y+1][x-1] = 'B'
                    else:
                        new_board[y+1][x-1] = 'b'
                    path.append(new_board)
    elif player == 'B':
        for i in range(rows):
            for j in range(columns):
                if board[i][j] == 'B':
                    path = jump(board, j, i, board[i][j])
        player_piece = coordinates_locater(player, board)
        for i in player_piece:
            y, x = i[0], i[1]
            if board[y][x] == 'B':
                # Right top diagonal single jump
                if x <= 6 and y >= 1 and board[y-1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y-1][x+1] = 'B'
                    path.append(new_board)
                # Left top diagonal single jump
                if x >= 1 and y >= 1 and board[y-1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y-1][x-1] = 'B'
                    path.append(new_board)
                # Right down diagonal single jump
                if x <= 6 and y <= 6 and board[y+1][x+1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y+1][x+1] = 'B'
                    path.append(new_board)
                # Left down diagonal single jump
                if x >= 1 and y <= 6 and board[y+1][x-1] == '.':
                    new_board = copy.deepcopy(board)
                    new_board[y][x] = '.'
                    new_board[y+1][x-1] = 'B'
                    path.append(new_board)
    return path

# Terminal position function to check if the game is over
def goal_state(board, player):
    status = False
    if player == 'r':
        king = 'R'
    elif player == 'b':
        king = 'B'
    if len(successor(board, player)) == 0 and len(successor(board, king)) == 0:
        status = True
    return status

# Minimax implementation
def min_max(board, depth, player):
    best_move = None
    if goal_state(board, player) or depth == 0:
        return best_move, cost(board, player)
    
    if player == 'r':
        king = 'R'
    elif player == 'b':
        king = 'B'
    
    player_moves = successor(board, player)
    king_moves = successor(board, king)
    all_moves = player_moves + king_moves

    if player == 'r':
        max_value = -200
        best_move = None
        for move in all_moves:
            eval = min_max(move, depth-1, 'b')[1]
            max_value = max(eval, max_value)
            if (max_value == eval):
                best_move = move
        return best_move, max_value

    elif player == 'b':
        min_value = 200
        worst_move = None
        for move in all_moves:
            eval = min_max(move, depth-1, 'r')[1]
            min_value = min(eval, min_value)
            if (min_value == eval):
                worst_move = move
                print(worst_move, eval, min_value)
        return worst_move, min_value

r_moves = successor(configuration, 'r')
R_moves = successor(configuration, 'R')
test3 = r_moves + R_moves

print(test3)
print(len(test3))
print(min_max(configuration, 1, 'r'))

final_move, utility = min_max(configuration, 1, 'r')
print(numpy.array(final_move))

def dijkstra (board, player):
    best_move = None

    max_value = float('-inf')

    if goal_state(board, player):
        return board, cost(board, player)

    if player == 'r':
        king = 'R'

    player_moves = successor(board, player)
    king_moves = successor(board, king)
    all_moves = player_moves + king_moves

    for move in all_moves:
        g_cost = cost(move, player)
        if g_cost > max_value:
            max_value = g_cost
            best_move = move
        pass

    return best_move, max_value

best_move, value = dijkstra(configuration, 'r')

# Output the file
'''output = open(output_file, "w")
for x in range(len(test3)):
    for i in range(rows):
        for j in range(columns):
            output.write(str(test3[x][i][j]))
        output.write("\n")
    output.write("\n")
'''
output = open(output_file, "w")
for i in range(rows):
    for j in range(columns):
        output.write(str(best_move[i][j]))
    output.write("\n")