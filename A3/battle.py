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

def existing_submarines(config, num_submarines):
    for i in range(n):
        for j in range(n):
            if config[i][j] == 'S':
                num_submarines = num_submarines - 1
    return num_submarines

num_submarines = existing_submarines(board, num_submarines)

# Variable declaration
ship_pieces = ['S', 'L', 'R', 'T', 'B', 'M']
total_pieces = ['S', 'L', 'R', 'T', 'B', 'M', 'W']
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

# Assign variables and domains
def assign_variable(config):
    # Create dictionary to store i, j indexes for cell-based assignments
    assignments = []
    domain = {}

    for i in range(n):
        for j in range(n):
            if config[i][j] not in total_pieces:
                assignments.append([i,j])
                domain[i, j] = [x for x in total_pieces]

    return assignments, domain

# Reduce top row constraints
def reduce_top_corners(config, domains):
    for i in domains:
        y, x = i[0], i[1]
        if y == 0 and x == 0:
            domains[i] = ['S', 'W', 'L', 'T', 'R']
            if config[y+1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'L']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T']
        elif y == 0 and x == n-1:
            domains[i] = ['S', 'W', 'L', 'T', 'R']
            if config[y][x-1] == 'W' and config[y+1][x] == 'W':
                domains[i] = ['S', 'W']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'T']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'R']
    return domains

# Reduce bottom row constraints
def reduce_bottom_corners(config, domains):
    for i in domains:
        y, x = i[0], i[1]
        if y == n-1 and x == n-1:
            domains[i] = ['S', 'W', 'L', 'B', 'R']
            if config[y-1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'R']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'B']
        elif y == n-1 and x == 0:
            domains[i] = ['S', 'W', 'L', 'B', 'R']
            if config[y-1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'B']
    return domains

# Reduce side constraints
def reduce_sides(config, domains):
    for i in domains:
        y, x = i[0], i[1]
        if x == 0 and y > 0 and y < n-1:
            domains[i] = ['S', 'W', 'L', 'T', 'B', 'M']
            if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L']
            elif config[y+1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'B']
            elif config[y-1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'B', 'L']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'T', 'L']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T', 'B', 'M']
        elif x == n-1 and y > 0 and y < n-1:
            domains[i] = ['S', 'W', 'R', 'T', 'B', 'M']
            if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'R']
            elif config[y+1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'B']
            elif config[y-1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'T']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'B', 'R']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'T', 'R']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'T', 'B', 'M']
        elif y == n-1 and x > 0 and x < n-1:
            domains[i] = ['S', 'W', 'R', 'L', 'B', 'M']
            if config[y][x-1] == 'W' and config[y][x+1] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W']
            elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'B']
            elif config[y][x-1] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L']
            elif config[y][x+1] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'R']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'B', 'L']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'B', 'R']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L', 'R', 'M']
        elif y == 0 and x > 0 and x < n-1:
            domains[i] = ['S', 'W', 'R', 'L', 'T', 'M']
            if config[y][x-1] == 'W' and config[y][x+1] == 'W' and config[y+1][x] == 'W':
                domains[i] = ['S', 'W']
            elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T']
            elif config[y][x-1] == 'W' and config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'L']
            elif config[y][x+1] == 'W' and config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'R']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'T', 'L']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T', 'R']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'L', 'R', 'M']
    return domains

# Reduce middle board constraints
def reduce_middle_board(config, domains):
    for i in domains:
        y, x = i[0], i[1]
        if x > 0 and x < n-1 and y > 0 and y < n-1:
            if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x-1] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W']
            elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L', 'R', 'M']
            elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T', 'B', 'M']
            elif config[y-1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'T', 'R']
            elif config[y+1][x] == 'W' and config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'B', 'R']
            elif config[y-1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'T', 'L']
            elif config[y+1][x] == 'W' and config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'B', 'L']
            elif config[y-1][x] == 'W':
                domains[i] = ['S', 'W', 'L', 'R', 'M', 'T']
            elif config[y+1][x] == 'W':
                domains[i] = ['S', 'W', 'L', 'R', 'M', 'B']
            elif config[y][x-1] == 'W':
                domains[i] = ['S', 'W', 'L', 'T', 'M', 'B']
            elif config[y][x+1] == 'W':
                domains[i] = ['S', 'W', 'R', 'T', 'M', 'B']
    return domains

# Check for solution
def is_solved(config):
    for i in range(n):
        for j in range(n):
            if config[i][j] == '0':
                return False
    return True

def MRV(domains):
    return dict(sorted(domains.items(), key=lambda i: -len(i[1]), reverse=True))

# FC 
def fc(config):
    updated_config = copy.deepcopy(config)

    return updated_config

board = autofill(board)
assignments, domains = assign_variable(board)

domains = reduce_top_corners(board, domains)
domains = reduce_bottom_corners(board, domains)
domains = reduce_sides(board, domains)
domains = reduce_middle_board(board, domains)
domains = MRV(domains)

print(num_submarines, num_destroyers, num_cruisers, num_battleships)

def ship_check(config, row_idx, col_idx, domain_value, row_line, col_line, num_submarines, num_destroyers, num_cruisers, num_battleships):

    return True

def row_col_constraint(config, row_idx, col_idx, domain_value, row_line, col_line, num_submarines, num_destroyers, num_cruisers, num_battleships):
    #config[row_idx][col_idx] 

    return True

def find_row_cells(domains, row_idx):
    keys_list = []
    keys_list = list(domains.keys())

    row_cells = []

    for i in keys_list:
        if i[0] == row_idx:
            row_cells.append(i)

    return row_cells

def find_col_cells(domains, col_idx):
    keys_list = []
    keys_list = list(domains.keys())

    col_cells = []

    for i in keys_list:
        if i[1] == col_idx:
            col_cells.append(i)

    return col_cells

def BT(config, domains, row_line, col_line, num_submarines, num_destroyers, num_cruisers, num_battleships):
    updated_config = copy.deepcopy(config)
    new_row_line = copy.deepcopy(row_line)
    new_col_line = copy.deepcopy(col_line)
    
    if is_solved == True:
        return updated_config

    for i in domains:
        y, x = i[0], i[1]
        row_cells = find_row_cells(domains, y)
        col_cells = find_col_cells(domains, x)
        for j in domains[i]:
            pass
            #print(ship_check(updated_config, i[0], i[1], j, new_row_line, new_col_line, num_submarines, num_destroyers, num_cruisers, num_battleships))
            #row_col_constraint(updated_config, y, x, j, new_row_line, new_col_line, num_submarines, num_destroyers, num_cruisers, num_battleships)

    print("Domains:")
    print(domains)
    return updated_config

board = BT(board, domains, row_line, col_line, num_submarines, num_destroyers, num_cruisers, num_battleships)
print(np.array(board))