# Import necessary libraries
from re import X
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

'''print(num_submarines, num_destroyers, num_cruisers, num_battleships)
print(row_line, col_line)'''

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

def superimpose_grids(config, grid_pattern, centre_row, centre_column):
    # If cell is in top row and not to sides
    if centre_row == 0 and (centre_column != 0 and centre_column != (n-1)):
        top_row = centre_row
        bottom_row = centre_row + 1
        right_col = centre_column + 1
        left_col = centre_column - 1
        print(left_col)
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell  

    # If cell is in bottom row and not to sides
    elif centre_row == (n-1) and (centre_column != 0 and centre_column != (n-1)):
        top_row = centre_row - 1
        bottom_row = centre_row
        right_col = centre_column + 1
        left_col = centre_column - 1
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell 
    
    # If cell is in right column and not at top or bottom
    elif centre_column == (n-1) and centre_row != 0 and centre_row != (n-1):
        top_row = centre_row - 1
        bottom_row = centre_row + 1
        right_col = centre_column
        left_col = centre_column - 1
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell 
    
    # If cell is in left column and not at top or bottom
    elif centre_column == 0 and centre_row != 0 and centre_row != (n-1):
        top_row = centre_row - 1
        bottom_row = centre_row + 1
        right_col = centre_column + 1
        left_col = centre_column
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell 
    
    # If cell is in right row and top
    elif centre_row == 0 and centre_column == (n-1):
        top_row = centre_row
        bottom_row = centre_row + 1
        right_col = centre_column
        left_col = centre_column - 1
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell 

    # If cell is in right row and bottom
    elif centre_column == (n-1) and centre_row == n-1:
        top_row = centre_row - 1
        bottom_row = centre_row
        right_col = centre_column
        left_col = centre_column - 1
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell
    
    # If cell is in bottom row and left
    elif centre_row == (n-1) and centre_column == 0:
        top_row = centre_row - 1
        bottom_row = centre_row
        right_col = centre_column + 1
        left_col = centre_column 
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell
    
    # If cell is in top row and left
    elif centre_row == 0 and centre_column == 0:
        top_row = centre_row
        bottom_row = centre_row + 1
        right_col = centre_column + 1
        left_col = centre_column 
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell

    else:
        top_row = centre_row - 1
        bottom_row = centre_row + 1
        right_col = centre_column + 1
        left_col = centre_column - 1
        
        for row_idx in range(top_row, bottom_row + 1):
            for col_idx in range(left_col, right_col + 1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = grid_pattern[subgrid_row][subgrid_col]
                if subcell == 'W':
                    config[row_idx][col_idx] = subcell  

    return config

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
    
    return np.array(updated_config)

print(autofill(board))
