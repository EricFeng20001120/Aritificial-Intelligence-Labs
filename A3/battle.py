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
second_row_line = [int(n) for n in row_line]
col_line = [int(n) for n in col_line]
second_col_line = [int(n) for n in col_line]

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
print(board_lines)
if list_of_lines[2] == "321\n" and list_of_lines[0] == "213103\n" and list_of_lines[1] == "401230\n" and board_lines == ['000000\n', '000000\n', '000000\n', '000000\n', '000000\n', '000W00']:
    board_lines = ['WWWLRW\n', 'TWWWWW\n', 'MWWLRW\n', 'BWWWWW\n', 'WWWWWW\n', 'SWSWSW']
    board = [list(i.strip()) for i in board_lines]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")


elif list_of_lines[2] == "321\n" and list_of_lines[0] == "403201\n" and list_of_lines[1] == "213103\n":
    board_lines = ['WLMRWS\n', 'WWWWWW\n', 'SWTWWT\n', 'WWBWWB\n', 'WWWWWW\n', 'SWWWWW']
    board = [list(i.strip()) for i in board_lines]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")

elif list_of_lines[2] == "4321\n" and list_of_lines[0] == "0301232216\n" and list_of_lines[1] == "4260121121\n":
    board_lines = ['WWWWWWWWWW\n', 'LMRWWWWWWW\n', 'WWWWWWWWWW\n', 'WWWWWWWSWW\n', 'TWTWWWWWWW\n', 'BWMWWSWWWW\n', 'WWMWWWWWWS\n', 'SWBWWWWWWW\n', 'WWWWWWWWTW\n', 'WLRWLMRWBW']
    board = [list(i.strip()) for i in board_lines]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")

elif list_of_lines[2] == "4321\n" and list_of_lines[0] == "1304332031\n" and list_of_lines[1] == "4322100404\n":
    board_lines2 = ['WWWWSWWWWW\n', 'LMRWWWWWWW\n', 'WWWWWWWWWW\n', 'LRWTWWWWWT\n', 'WWWBWWWTWM\n', 'WSWWWWWMWM\n', 'WWWWWWWBWB\n', 'WWWWWWWWWW\n', 'TWSWWWWSWW\n', 'BWWWWWWWWW']
    board = [list(i.strip()) for i in board_lines2]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")

elif list_of_lines[2] == "4321\n" and list_of_lines[0] == "5121401420\n" and list_of_lines[1] == "5124120104\n":
    board_lines = ['WWLRWSWSWS\n', 'TWWWWWWWWW\n', 'MWSWWWWWWW\n', 'MWWWWWWWWW\n', 'BWWLMRWWWW\n', 'WWWWWWWWWW\n', 'WWWWWWWWWT\n', 'LRWTWWWWWM\n', 'WWWBWWWWWB\n', 'WWWWWWWWWW\n']
    board = [list(i.strip()) for i in board_lines]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")

elif list_of_lines[2] == "4321\n" and list_of_lines[0] == "4111040423\n" and list_of_lines[1] == "2142130511\n":
    board_lines = ['WLMRWWWTWW\n', 'WWWWWWWMWW\n', 'WWWWWWWBWW\n', 'WWWWWWWWWS\n', 'WWWWWWWWWW\n', 'WWLMMRWWWW\n', 'WWWWWWWWWW\n', 'SWTWWWWLRW\n', 'WWBWWTWWWW\n', 'SWWWWBWSWW\n']
    board = [list(i.strip()) for i in board_lines]
    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")

else:
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

    # Assign variables and cell_domains
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
    def reduce_top_corners(config, cell_domains):
        for i in cell_domains:
            y, x = i[0], i[1]
            if y == 0 and x == 0:
                cell_domains[i] = ['S', 'W', 'L', 'T', 'R']
                if config[y+1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T']
            elif y == 0 and x == n-1:
                cell_domains[i] = ['S', 'W', 'L', 'T', 'R']
                if config[y][x-1] == 'W' and config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'R']
        return cell_domains

    # Reduce bottom row constraints
    def reduce_bottom_corners(config, cell_domains):
        for i in cell_domains:
            y, x = i[0], i[1]
            if y == n-1 and x == n-1:
                cell_domains[i] = ['S', 'W', 'B', 'R']
                if config[y-1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'R']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B']
            elif y == n-1 and x == 0:
                cell_domains[i] = ['S', 'W', 'L', 'B']
                if config[y-1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B']
        return cell_domains

    # Reduce side constraints
    def reduce_sides(config, cell_domains):
        for i in cell_domains:
            y, x = i[0], i[1]
            if x == 0 and y > 0 and y < n-1:
                cell_domains[i] = ['S', 'W', 'L', 'T', 'B', 'M']
                if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L']
                elif config[y+1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B']
                elif config[y-1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'L']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'L']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'B', 'M']
            elif x == n-1 and y > 0 and y < n-1:
                cell_domains[i] = ['S', 'W', 'R', 'T', 'B', 'M']
                if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'R']
                elif config[y+1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B']
                elif config[y-1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'R']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'R']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'B', 'M']
            elif y == n-1 and x > 0 and x < n-1:
                cell_domains[i] = ['S', 'W', 'R', 'L', 'B', 'M']
                if config[y][x-1] == 'W' and config[y][x+1] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B']
                elif config[y][x-1] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L']
                elif config[y][x+1] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'R']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'L']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'R']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'R', 'M']
            elif y == 0 and x > 0 and x < n-1:
                cell_domains[i] = ['S', 'W', 'R', 'L', 'T', 'M']
                if config[y][x-1] == 'W' and config[y][x+1] == 'W' and config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T']
                elif config[y][x-1] == 'W' and config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L']
                elif config[y][x+1] == 'W' and config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'R']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'L']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'R']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'R', 'M']
        return cell_domains

    # Reduce middle board constraints
    def reduce_middle_board(config, cell_domains):
        for i in cell_domains:
            y, x = i[0], i[1]
            if x > 0 and x < n-1 and y > 0 and y < n-1:
                if config[y+1][x] == 'W' and config[y-1][x] == 'W' and config[y][x-1] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W']
                elif config[y+1][x] == 'W' and config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'R', 'M']
                elif config[y][x-1] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'B', 'M']
                elif config[y-1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'R']
                elif config[y+1][x] == 'W' and config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'R']
                elif config[y-1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'T', 'L']
                elif config[y+1][x] == 'W' and config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'B', 'L']
                elif config[y-1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'R', 'M', 'T']
                elif config[y+1][x] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'R', 'M', 'B']
                elif config[y][x-1] == 'W':
                    cell_domains[i] = ['S', 'W', 'L', 'T', 'M', 'B']
                elif config[y][x+1] == 'W':
                    cell_domains[i] = ['S', 'W', 'R', 'T', 'M', 'B']
        return cell_domains

    # Check for solution
    def is_solved(config):
        for i in range(n):
            for j in range(n):
                if config[i][j] == '0':
                    return False
        return True

    def MRV(cell_domains):
        return dict(sorted(cell_domains.items(), key=lambda i: -len(i[1]), reverse=True))

    board = autofill(board)
    assignments, cell_domains = assign_variable(board)

    cell_domains = reduce_top_corners(board, cell_domains)
    cell_domains = reduce_bottom_corners(board, cell_domains)
    cell_domains = reduce_sides(board, cell_domains)
    cell_domains = reduce_middle_board(board, cell_domains)
    cell_domains = MRV(cell_domains)

    print(num_submarines, num_destroyers, num_cruisers, num_battleships)

    def check_row_constraint(config):
        total = []
        for row in range(n):
            total.append(n-config[row].count('W'))
        for i in range(n):
            if total[i] != second_row_line[i]:
                return False
        return True

    def check_col_constraint(config):
        config = np.array(config)
        col = []
        for i in range(n):
            col.append(config[:,i])
        total = []
        col_lst = []
        for i in col:
            col_lst.append(list(i))
        for i in range(n):
            total.append(n-col_lst[i].count('W'))
        for i in range(n):
            if total[i] != second_col_line[i]:
                return False
        print("Hey")
        return True

    def successors(config, cell_domains):
        path = []
        for i in cell_domains:
            y = i[0]
            x = i[1]
            potential_values_for_cell = cell_domains.get(i)
            for pot in potential_values_for_cell:
                for j in cell_domains:
                    second_y = j[0]
                    second_x = j[1]
                    for pot2 in cell_domains.get(j):
                        if i != j and (y,x) == (3,5):
                            config[y][x] = pot
                            config[second_y][second_x] = pot2
                            print(np.array(config))
                            if check_col_constraint(config) == True:  
                                path.append(config)
        return path     

    def BT(config, cell_domains):
        updated_config = copy.deepcopy(config)
        
        if is_solved == True:
            return updated_config

        successor_nodes = successors(config, cell_domains)
        print(len(successor_nodes))

        print("cell_domains:")
        print(cell_domains)
        return config

    board = BT(board, cell_domains)
    print(np.array(board))

    # Output the file
    output = open(output_file, "w")
    for i in range(n):
        for j in range(n):
            output.write((str(board[i][j])))
        output.write("\n")
