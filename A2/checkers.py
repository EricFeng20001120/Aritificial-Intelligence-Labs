# Import libraries
from distutils.command.config import config
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

def jump(board, player):
    path = []
    player_piece = coordinates_locater(player, board)
    print("Red piece coordinates: " + str(player_piece))

    # Create successors for the player piece
    for i in player_piece:
        if player == 'r':
            # Jump left
            if i[0] <= 5 and i[1] >= 2 and board[i[0]+2][i[1]-2] == '.' and (board[i[0]+1][i[1]-1] == 'b' or board[i[0]+1][i[1]-1] == 'B'):
                new_board = copy.deepcopy(board)
                new_board[i[0]][i[1]] = '.'
                new_board[i[0]+1][i[1]-1] = '.'
                if i[0] == 5:
                    new_board[i[0]+2][i[1]-2] = 'R'
                else: 
                    new_board[i[0]+2][i[1]-2] = 'r'
                path.append(new_board)

            # Jump right
            if i[0] <= 5 and i[1] <= 5 and board[i[0]+2][i[1]+2] == '.' and (board[i[0]+1][i[1]+1] == 'b' or board[i[0]+1][i[1]+1] == 'B'):
                new_board = copy.deepcopy(board)
                new_board[i[0]][i[1]] = '.'
                new_board[i[0]+1][i[1]+1] = '.'
                if i[0] == 5:
                    new_board[i[0]+2][i[1]+2] = 'R'
                else: 
                    new_board[i[0]+2][i[1]+2] = 'r'
                path.append(new_board)

    return path

# Successor function
def successor(board, player):
    path = []
    if player == 'r':
        player_piece = coordinates_locater(player, board)
        print(player_piece)
        for i in player_piece:
            y, x = i[0], i[1]
            print(y,x)
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
        player_piece = coordinates_locater(player, board)
        print(player_piece)
        for i in player_piece:
            y, x = i[0], i[1]
            print(y,x)
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
        player_piece = coordinates_locater(player, board)
        print(player_piece)
        for i in player_piece:
            y, x = i[0], i[1]
            print(y,x)
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
        player_piece = coordinates_locater(player, board)
        print(player_piece)
        for i in player_piece:
            y, x = i[0], i[1]
            print(y,x)
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

print(len(successor(configuration, 'r')))
print(len(successor(configuration, 'R')))
print(len(successor(configuration, 'b')))
print(len(successor(configuration, 'B')))

# Output the file
output = open(output_file, "w")
for i in range(rows):
    for j in range(columns):
        output.write(str(configuration[i][j]))
    output.write("\n")
