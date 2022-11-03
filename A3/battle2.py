# Import necessary libraries
import sys
import copy
import numpy as np

# Set the two parameters to pass in
input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the input file
with open(input_file, 'r') as f:
    list_of_lines = f.readlines()

# Get the first three lines for the row, column and ship information
# The last n lines are for the board configuration
row_line = list(list_of_lines[0])
col_line = list(list_of_lines[1])
ship_line = list(list_of_lines[2])
board_lines = list_of_lines[3:]

# Remove the whitespace at the end of the first three lines
del row_line[-1], col_line[-1], ship_line[-1]

# Convert characters in row and col line into integers
row_line = [int(n) for n in row_line]
col_line = [int(n) for n in col_line]

# Get the number of ships per the ship line
num_submarines, num_destroyers, num_cruisers, num_battleships = 0, 0, 0, 0
for i in range(len(ship_line)):
    if i == 0:
        num_submarines = int(ship_line[i])
    if i == 1:
        num_destroyers = int(ship_line[i])
    if i == 2:
        num_cruisers = int(ship_line[i])
    if i == 3:
        num_battleships = int(ship_line[i])

# Get the n for the nxn board configuration
n = len(board_lines)

# Store the board into a list of list while stripping white spaces
board = [list(i.strip()) for i in board_lines]

'''def existing_submarines(config, num_submarines):
    for i in range(n):
        for j in range(n):
            if config[i][j] == 'S':
                num_submarines = num_submarines - 1
    return num_submarines

num_submarines = existing_submarines(board, num_submarines)'''

ships = {"S": num_submarines, "D": num_destroyers, "C": num_cruisers, "B": num_battleships}

ship_pieces = ['S', 'L', 'R', 'T', 'B', 'M']
water_surrounding = {
    'S': [['W', 'W', 'W'], ['W', 'S', 'W'], ['W', 'W', 'W']],
    'T': [['W', 'W', 'W'], ['W', 'T', 'W'], ['W', '0', 'W']],
    'M': [['W', '0', 'W'], ['0', 'M', '0'], ['W', '0', 'W']],
    'L': [['W', 'W', 'W'], ['W', 'L', 'X'], ['W', 'W', 'W']],
    'R': [['W', 'W', 'W'], ['0', 'R', 'W'], ['W', 'W', 'W']],
    'B': [['W', 'X', 'W'], ['W', 'B', 'W'], ['W', 'W', 'W']]
}

def superimpose_grids(config, grid_pattern, row_in_middle, col_in_middleumn):
    # If cell is in top row and not to sides
    if row_in_middle == 0 and (col_in_middleumn != 0 and col_in_middleumn != (n-1)):
        top_row = row_in_middle
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn - 1

    # If cell is in bottom row and not to sides
    elif row_in_middle == (n-1) and (col_in_middleumn != 0 and col_in_middleumn != (n-1)):
        top_row = row_in_middle - 1
        bottom_row = row_in_middle
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn - 1 
    
    # If cell is in right column and not at top or bottom
    elif col_in_middleumn == (n-1) and row_in_middle != 0 and row_in_middle != (n-1):
        top_row = row_in_middle - 1
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn
        left_col = col_in_middleumn - 1
    
    # If cell is in left column and not at top or bottom
    elif col_in_middleumn == 0 and row_in_middle != 0 and row_in_middle != (n-1):
        top_row = row_in_middle - 1
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn
    
    # If cell is in right row and top
    elif row_in_middle == 0 and col_in_middleumn == (n-1):
        top_row = row_in_middle
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn
        left_col = col_in_middleumn - 1

    # If cell is in right row and bottom
    elif col_in_middleumn == (n-1) and row_in_middle == n-1:
        top_row = row_in_middle - 1
        bottom_row = row_in_middle
        right_col = col_in_middleumn
        left_col = col_in_middleumn - 1
    
    # If cell is in bottom row and left
    elif row_in_middle == (n-1) and col_in_middleumn == 0:
        top_row = row_in_middle - 1
        bottom_row = row_in_middle
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn 
    
    # If cell is in top row and left
    elif row_in_middle == 0 and col_in_middleumn == 0:
        top_row = row_in_middle
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn 

    # If the cell is anywhere else on the board
    else:
        top_row = row_in_middle - 1
        bottom_row = row_in_middle + 1
        right_col = col_in_middleumn + 1
        left_col = col_in_middleumn - 1
        
    # Go through the cell surroundings and assign Water near it
    for row_idx in range(top_row, bottom_row + 1):
        for col_idx in range(left_col, right_col + 1):
            subgrid_row = row_idx - row_in_middle + 1
            subgrid_col = col_idx - col_in_middleumn + 1
            subcell = grid_pattern[subgrid_row][subgrid_col]
            if subcell == 'W':
                config[row_idx][col_idx] = subcell  

    return config

# Proprocessing function which autofills water near given ships and rows and columns with 0 ships
def autofill(config):
    updated_config = copy.deepcopy(config)
    for row_index in range(n):
        for col_index in range(n):
            if row_line[row_index] == 0 or col_line[col_index] == 0:
                updated_config[row_index][col_index] = 'W'

    for row_index, row in enumerate(updated_config):
        for col_index, cell_char in enumerate(row):
            if cell_char in ship_pieces:
                row_line[row_index] -= 1
                col_line[col_index] -= 1

    for row_index, row in enumerate(updated_config):
        for col_index, cell in enumerate(row):
            if cell in ship_pieces:
                superimpose_grids(updated_config, water_surrounding[cell], row_index, col_index)
    
    for row_index in range(n):
        for col_index in range(n):
            if row_line[row_index] == 0 or col_line[col_index] == 0:
                if updated_config[row_index][col_index] == '0':
                    updated_config[row_index][col_index] = 'W'

    return updated_config

def check_ships(config):
    """ check if the current board falsify the ships constraint"""
    sub_num = 0
    des_num = 0
    crui_num = 0
    bat_num = 0
    for i in range(n):
        for j in range(n):
            if config[i][j] == '0' or config[i][j] == 'W':
                continue
            if config[i][j] == 'S':  # submarine 1x1
                sub_num += 1
            elif config[i][j] == 'T':  # vertical destroyer 1x2 or cruiser 1x3 or battleship 1x4
                if config[i+1][j] == 'M':  # cruiser 1x3 or battleship 1x4
                    if config[i+2][j] == 'M':  # battleship 1x4
                        bat_num += 1
                    elif config[i+2][j] == 'B':  # cruiser 1x3
                        crui_num += 1
                elif config[i+1][j] == 'B':  # destroyer 1x2
                    des_num += 1
            elif config[i][j] == 'L':  # horizontal destroyer 1x2 or cruiser 1x3 or battleship 1x4
                if config[i][j+1] == 'M':  # cruiser 1x3 or battleship 1x4
                    if config[i][j+2] == 'M':  # battleship 1x4
                        bat_num += 1
                    elif config[i][j+2] == 'R':  # cruiser 1x3
                        crui_num += 1
                elif config[i][j+1] == 'R':  # destroyer 1x2
                    des_num += 1

    if sub_num == ships["S"] and des_num == ships["D"] and crui_num == ships["C"] and bat_num == ships["B"]:
        # the ships number match
        return True
    else:
        return False

def check_row_const(config, row_num):
    """ check if the current board falsify the row constraint"""
    row = config[row_num]
    total = len(row)
    for i in range(len(row)):
        if row[i] == '0' or row[i] == 'W':
            total -= 1
    if total == row_line[row_num]:
        return True
    else:
        return False


def check_col_const(config, col_num):
    """ check if the current board falsify the col constraint"""
    col = [config[i][col_num] for i in range(len(config))]
    total = len(col)
    for i in range(len(col)):
        if col[i] == '0' or col[i] == 'W':
            total -= 1
    if total == col_line[col_num]:
        return True
    else:
        return False

def match_row_const(data, row_num):  # checked
    """ check if assigning ship on board cause the num filled square match the row const number"""
    row = data[row_num]
    total = 0
    for i in range(len(row)):
        if row[i] != '0' and row[i] != 'W':
            total += 1
    if total == row_line[row_num]:
        return True
    else:
        return False

def match_col_const(data, col_num):  # checked
    """ check if assigning new ship will exceed the col number, data should be new_data"""
    col = [data[i][col_num] for i in range(len(data))]
    total = 0
    for i in range(len(col)):
        if col[i] != '0' and col[i] != 'W':
            total += 1
    if total <= col_line[col_num]:
        return True
    else:
        return False

def update_const(config):  # checked
    """
    update the board based on row, col, ships const 
    """
    updated_config = copy.deepcopy(config)
    if check_ships(updated_config):
        # ships number matched, filled the rest of the board with W
        # print("ships checked")
        for i in range(n):
            for j in range(n):
                if updated_config[i][j] == '0':
                    updated_config[i][j] = 'W'
        return

    for i in range(n):
        if check_row_const(updated_config, i):
            # row_num matches, need to filled out the rest squares on this row with W
            # print("row number " + str(i) + " is satisfied")
            for j in range(n):
                if updated_config[i][j] == '0':
                    updated_config[i][j] = 'W'
        if check_col_const(updated_config, i):
            # col_num matches, need to filled out the rest squares on this row with W
            # print("col number " + str(i) + " is satified")
            for j in range(n):
                if updated_config[j][i] == '0':
                    updated_config[j][i] = 'W'
    return updated_config

board = autofill(board)
board = update_const(board)
print(np.array(board))

def domains(config, domain):  # checked
    """
    add all possible move (domain) for each ship & remove the assigned variables
    should have checked that there is bat ship num >= 1 before calling this function
    WARNING: cannot call it anywhere else except in read_file, will cause duplicate domain
    """
    for i in range(n):
        for j in range(n):
            if i+3 <= n-1 and config[i][j] == '0' and config[i+1][j] == '0' and config[i+2][j] == '0' and config[i+3][j] == '0':
                # there is space to place a vertical battleship
                domain["B"].append([[i, j], [i+1, j], [i+2, j], [i+3, j]])
            if j+3 <= n-1 and config[i][j] == '0' and config[i][j+1] == '0' and config[i][j+2] == '0' and config[i][j+3] == '0':
                # there is space to place a horizontal battleship
                domain["B"].append([[i, j], [i, j+1], [i, j+2], [i, j+3]])
            if i+2 <= n-1 and config[i][j] == '0' and config[i+1][j] == '0' and config[i+2][j] == '0':
                # there is space to place a vertical cruiser
                domain["C"].append([[i, j], [i+1, j], [i+2, j]])
            if j+2 <= n-1 and config[i][j] == '0' and config[i][j+1] == '0' and config[i][j+2] == '0':
                # there is space to place a horizontal cruiser
                domain["C"].append([[i, j], [i, j+1], [i, j+2]])
            if i+1 <= n-1 and config[i][j] == '0' and config[i+1][j] == '0':
                # there is space to place a vertical destroyer
                domain["D"].append([[i, j], [i+1, j]])
            if j+1 <= n-1 and config[i][j] == '0' and config[i][j+1] == '0':
                # there is space to place a horizontal destroyer
                domain["D"].append([[i, j], [i, j+1]])
            if config[i][j] == '0':
                # there is space to place a submarine
                domain["S"].append([[i, j]])
    return domain

# domain (list of possible locations) of each ship
domain = {}
domain["S"] = []
domain["D"] = []
domain["C"] = []
domain["B"] = []

domain = domains(board, domain)

def check_orientation(positions):  # checked
    """ determine the orientation of given positions """
    old_y, old_x = positions[0][0], positions[0][1]
    new_y, new_x = positions[1][0], positions[1][1]
    if new_y > old_y and new_x == old_x:  # vertical
        return 1
    elif new_y == old_y and new_x > old_x:  # horizontal
        return 0


def insert_into_board(data, var, pos):  # checked
    """ set the given variable into given position """
    if len(pos) > 1:
        ori = check_orientation(pos)
    # pos = all of the squares need to be filled up with 'T', 'B', 'L', 'R', 'M' or 'S'
    if var == 'B':  # a battleship, 1x4
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            data[y][x] = 'B'
    elif var == 'C':  # cruiser, 1x3
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'B'
    elif var == 'D':  # destroyer, 1x2
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'B'
    elif var == 'S':  # submarine, 1x1
        y, x = pos[0][0], pos[0][1]
        data[y][x] = 'S'
    update_const(data)
    update_data(data)

# Output the file
output = open(output_file, "w")
for i in range(n):
    for j in range(n):
        output.write((str(board[i][j])))
    output.write("\n")