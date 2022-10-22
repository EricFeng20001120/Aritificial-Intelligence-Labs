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

print(list_of_lines)

# Get the first three lines for the row, column and ship information
# The last n lines are for the board configuration
row_line = list(list_of_lines[0])
col_line = list(list_of_lines[1])
ship_line = list(list_of_lines[2])
board_lines = list_of_lines[3:]

# Remove the whitespace at the end of the first three lines
del row_line[-1], col_line[-1], ship_line[-1]
print(row_line, col_line, ship_line)

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

print(num_submarines, num_destroyers, num_cruisers, num_battleships)

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

print(coordinates_locater(board, 'S'))
