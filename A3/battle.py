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

print(np.array(board))

# Function that finds the coordinates of a specific digit given the configuration
def coordinates_locater(config, digit):
    index = []
    for i in range(n):
        for j in range(n):
            if config[i][j] == digit:
                index.append((i, j))
    return index

def zero_check(config):
    for i in range(len(col_line)):
        if col_line[i] == '0':
            return i

print(num_submarines, num_destroyers, num_cruisers, num_battleships)
print(row_line, col_line)

pieces = ['S', 'L', 'R', 'T', 'B', 'M']

# Variable declaration
water_surrounding = {
    'S':
        """
        WWW
        WSW
        WWW
        """
}

def remaining_row_col_count(config):
    for row_index, row in enumerate(config):
        for col_index, cell_char in enumerate(row):
            if cell_char in pieces:
                row_line[row_index] -= 1
                col_line[col_index] -= 1
    return row_line, col_line

def autofill_water_in_full_rows_cols(config):
    """
    Add water cells if all the ship bits for that column/row are populated already.
    :return:
    """
    ships_to_add_to_row, ships_to_add_to_col = remaining_row_col_count(board)
    for row_index, row in enumerate(config):
        for col_index, cell_char in enumerate(row):
            if ships_to_add_to_row[row_index] == 0 or ships_to_add_to_col[col_index] == 0:
                if config[row_index][col_index] == '0':
                    config[row_index][col_index] = 'W'
    
    return np.array(config)

print(remaining_row_col_count(board))
print(autofill_water_in_full_rows_cols(board))