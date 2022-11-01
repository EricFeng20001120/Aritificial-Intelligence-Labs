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
        num_submarines = ship_line[i]
    if i == 1:
        num_destroyers = ship_line[i]
    if i == 2:
        num_cruisers = ship_line[i]
    if i == 3:
        num_battleships = ship_line[i]

# Get the n for the nxn board configuration
n = len(board_lines)

# Store the board into a list of list while stripping white spaces
board = [list(i.strip()) for i in board_lines]

# Function that finds the coordinates of a specific digit given the configuration
def coordinates_locater(config, digit):
    index = []
    for i in range(n):
        for j in range(n):
            if config[i][j] == digit:
                index.append((i, j))
    return index

# Variable declaration
pieces = ['S', 'L', 'R', 'T', 'B', 'M']
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
            if cell_char in pieces:
                row_line[row_index] -= 1
                col_line[col_index] -= 1

    for row_index, row in enumerate(updated_config):
        for col_index, cell in enumerate(row):
            if cell in pieces:
                superimpose_grids(updated_config, water_surrounding[cell], row_index, col_index)
    
    for row_index in range(n):
        for col_index in range(n):
            if row_line[row_index] == 0 or col_line[col_index] == 0:
                if updated_config[row_index][col_index] == '0':
                    updated_config[row_index][col_index] = 'W'

    return updated_config

'''# Assign variables
def assign_variable(config):
    assignments = {}
    for i in range(n):
        for j in range(n):
            assignments += ((i, j), config[i][j])

    return assignments'''

def fill_x(config):
    updated_config = copy.deepcopy(config)
    for i in range(n):
        for j in range(n):
            if updated_config[i][j] == '0' and row_line[i] == 1 and col_line[j] == 1:
                updated_config[i][j] == 'S'
                row_line[i] -= 1
                col_line[j] -= 1

    return np.array(updated_config)

# Check for solution
def is_solved(config):
    for i in range(n):
        for j in range(n):
            if config[i][j] == '0':
                return False
    return True

# FC 
def fc(config):
    updated_config = copy.deepcopy(config)

    return updated_config

print(np.array(autofill(board)))