# Import libraries
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

def special_jump(board, x, y, player):
    path = []
    if player == 'R':
        # Bottom right jump
        if x <= 5 and y <= 5 and (board[y+1][x+1] == 'b' or board[y+1][x+1] == 'B') and board[y+2][x+2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y+1][x+1] = '.'
            new_board[y+2][x+2] = 'R'
            double_jump = special_jump(new_board, x+2, y+2, player)
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
            double_jump = special_jump(new_board, x-2, y+2, player)
            tmp = numpy.array(double_jump).squeeze()
            tmp = tmp.tolist()
            if (len(tmp) >= 1):
                path.append(tmp)
            else:
                path.append(new_board)
        # Upper right jump
        if x <= 5 and y >= 2 and (board[y-1][x+1] == 'b' or board[y-1][x+1] == 'B') and board[y-2][x+2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y-1][x+1] = '.'
            new_board[y-2][x+2] = 'R'
            double_jump = special_jump(new_board, x+2, y-2, player)
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
            double_jump = special_jump(new_board, x-2, y-2, player)
            tmp = numpy.array(double_jump).squeeze()
            tmp = tmp.tolist()
            if (len(tmp) >= 1):
                path.append(tmp)
            else:
                path.append(new_board)

    elif player == 'B':
        # Bottom right jump
        if x <= 5 and y <= 5 and (board[y+1][x+1] == 'r' or board[y+1][x+1] == 'R') and board[y+2][x+2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y+1][x+1] = '.'
            new_board[y+2][x+2] = 'B'
            double_jump = special_jump(new_board, x+2, y+2, player)
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
            double_jump = special_jump(new_board, x-2, y+2, player)
            tmp = numpy.array(double_jump).squeeze()
            tmp = tmp.tolist()
            if (len(tmp) >= 1):
                path.append(tmp)
            else:
                path.append(new_board)
        # Upper right jump
        if x <= 5 and y >= 2 and (board[y-1][x+1] == 'r' or board[y-1][x+1] == 'R') and board[y-2][x+2] == '.':
            new_board = copy.deepcopy(board)
            new_board[y][x] = '.'
            new_board[y-1][x+1] = '.'
            new_board[y-2][x+2] = 'B'
            double_jump = special_jump(new_board, x+2, y-2, player)
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
            double_jump = special_jump(new_board, x-2, y-2, player)
            tmp = numpy.array(double_jump).squeeze()
            tmp = tmp.tolist()
            if (len(tmp) >= 1):
                path.append(tmp)
            else:
                path.append(new_board)

    return path

# Jump function
def jump(board, player):
    path = []
    player_piece = coordinates_locater(player, board)
    # Create successors for the player piece
    for i in player_piece:
        y, x = i[0], i[1]
        if player == 'r':
            # Upper right jump
            if x <= 5 and y >= 2 and (board[y-1][x+1] == 'b' or board[y-1][x+1] == 'B') and board[y-2][x+2] == '.':
                new_board = copy.deepcopy(board)
                new_board[y][x] = '.'
                new_board[y-1][x+1] = '.'
                if y == 2:
                    new_board[y-2][x+2] = 'R'
                    player = 'R'
                    double_jump = special_jump(new_board, x+2, y-2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)
                    break
                else:
                    new_board[y-2][x+2] = 'r'
                    double_jump = jump(new_board, player)
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
                    double_jump = special_jump(new_board, x-2, y-2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)
                else:
                    new_board[y-2][x-2] = 'r'
                    double_jump = jump(new_board, player)
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
                    double_jump = special_jump(new_board, x+2, y+2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)
                else:
                    new_board[y+2][x+2] = 'b'
                    double_jump = jump(new_board, player)
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
                    double_jump = special_jump(new_board, x-2, y+2, player)
                    tmp = numpy.array(double_jump).squeeze()
                    tmp = tmp.tolist()
                    if (len(tmp) >= 1):
                        path.append(tmp)
                    else:
                        path.append(new_board)
                else:
                    new_board[y+2][x-2] = 'b'
                    double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                double_jump = jump(new_board, player)
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
                    path = jump(board, board[i][j])
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
                    path = jump(board, board[i][j])
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
                    path = jump(board, board[i][j])
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
                    path = jump(board, board[i][j])
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

# Minimax implementation for the max player
def dfs_max(board, player):
    best_move = None

    if goal_state(board, player):
        return board

    if player == 'r':
        value = float('-inf')
    elif player == 'b':
        value = float('inf')

    if player == 'r':
        king = 'R'

    # Check for possible moves by r
    for move in successor(board, player):
        g_cost = cost(move, player)
        print(g_cost)
        if g_cost > value:
            value = g_cost
            best_move = move
        pass

    # Check for possible moves by R
    for move in successor(board, king):
        #print(move)
        g_cost = cost(move, player)
        print(g_cost)
        if g_cost > value:
            value = g_cost
            best_move = move
        pass

    return best_move, value

r_moves = successor(configuration, 'r')
R_moves = successor(configuration, 'R')
test3 = r_moves + R_moves

final_move, cost = dfs_max(configuration, 'r')
print(final_move, cost)

"""# Minimax with DFS
def dfs_minmax(board):
    best_move = []
    if terminal(pos):
        return best_move, utility(pos)
    if player(pos) == MAX: 
        value = float('-inf')
    if player(pos) == MIN: 
        value = infinity
    for move in actions(pos):
        nxt_pos = result(pos, move)
        nxt_val, nxt_move = DFMiniMax(nxt_pos)
    if player(pos) == MAX and value < nxt_val:
        value, best_move = nxt_val, move
    if player(pos) == MIN and value > nxt_value:
        value, best_move = nxt_val, move
    return best_move, value"""

# Output the file
output = open(output_file, "w")
for x in range(len(test3)):
    for i in range(rows):
        for j in range(columns):
            output.write(str(test3[x][i][j]))
        output.write("\n")
    output.write("\n")

"""output = open(output_file, "w")
for i in range(rows):
    for j in range(columns):
        output.write(str(final_move[i][j]))
    output.write("\n")"""
