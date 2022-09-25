import sys
import time
import copy

# Create global variables for the number of columns and rows of the board
cols = 5
rows = 4

start_time = time.time()

# Set the three parameters to pass in
filename = sys.argv[1]
dfs_filename = sys.argv[2]
astar_filename = sys.argv[3]

# Create a 5x4 array to store the digits of the puzzle
puzzle = [[] for x in range(cols)]

# Import the puzzle.txt file and use a nested for loop to store digits
with open(filename) as file:
    for i in range(cols):
        for j in range(rows):
            puzzle[i].append(file.read(1))
        file.read(1)

# Function that finds the coordinates of a specific digit given the configuration
def coordinates_locater(digit, config):
    index = []
    for i in range(cols):
        for j in range(rows):
            if config[i][j] == digit:
                index.append((i, j))
    return index

# Locate the empty squares as they are the only pieces which can move
def empty_space_locater(config):
    empty_squares = coordinates_locater('0', config)

    # Find individual x and y coordinates of the two empty spaces
    first_x, first_y = empty_squares[0][1], empty_squares[0][0]
    second_x, second_y = empty_squares[1][1], empty_squares[1][0]

    return first_x, first_y, second_x, second_y

# Function to find all the vertical pieces
# This is needed as there are 32 initial configurations
# and because the integers except 1 and 0 are randomized
def vertical_pieces(config):
    # Initialize a list that stores the vertical pieces
    digits_vertical = []
    # Initialize coordinates variables which find the index of numbers
    coordinates_2 = coordinates_locater('2', config)
    coordinates_3 = coordinates_locater('3', config)
    coordinates_4 = coordinates_locater('4', config)
    coordinates_5 = coordinates_locater('5', config)
    coordinates_6 = coordinates_locater('6', config)
    # Find if the y coordinate below the index is the same
    if coordinates_6[0][1] == coordinates_6[1][1]:
        digits_vertical.append('6')
    if coordinates_5[0][1] == coordinates_5[1][1]:
        digits_vertical.append('5')
    if coordinates_4[0][1] == coordinates_4[1][1]:
        digits_vertical.append('4')
    if coordinates_3[0][1] == coordinates_3[1][1]:
        digits_vertical.append('3') 
    if coordinates_2[0][1] == coordinates_2[1][1]:
        digits_vertical.append('2')  
    
    return digits_vertical

# Function that returns all horizontal pieces
# We know the 5 1x2 pieces are denoted by one of [2, 3, 4, 5, 6]
def horizontal_pieces(config, vertical_pieces_list):
    pieces = ['2', '3', '4', '5', '6'] 
    # Create list for all pieces that aren't in the vertical list
    digits_horizontal = [x for x in pieces if x not in vertical_pieces_list]
    return digits_horizontal

# Simple Manhattan distance function
def manhattan_distance(config):
    # Find indices of the Cao Cao piece
    index_of_ones = coordinates_locater('1', config)
    # Get the top and leftmost location from Cao Cao
    leftmost_x_pos, leftmost_y_pos = index_of_ones[0][1], index_of_ones[0][0]
    # Calculate the number of steps it would take for Cao Cao to get to the bottom centre of the puzzle
    manhattan_cost = abs(1-leftmost_x_pos) + (3-leftmost_y_pos)
    return manhattan_cost

# Successor function which examines every possibility
def successor_nodes(config):#, vertical, horizontal):
    path = []
    # Get coordinates for empty spaces
    first_x, first_y, second_x, second_y = empty_space_locater(config)

    return second_y

# Output the dfs file
with open(dfs_filename, "w" ) as dfs_f:
    print("Hey", file=dfs_f)
 
# Output the A* file
with open(astar_filename, "w") as astar_f:
    print("Hello", file=astar_f)

vertical_pieces_list = vertical_pieces(puzzle)
print(vertical_pieces_list)

horizontal_pieces_list = horizontal_pieces(puzzle, vertical_pieces_list)
print(horizontal_pieces_list)

print(manhattan_distance(puzzle))

print(successor_nodes(puzzle))

end_time = time.time()
final_time = end_time - start_time

print(final_time)