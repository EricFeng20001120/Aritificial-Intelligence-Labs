import sys
import time
import copy
import heapq
from turtle import pu

start_time = time.time()

# Create global variables for the number of columns and rows of the board
cols = 5
rows = 4

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
# We know the 5 1second_x pieces are denoted by one of [2, 3, 4, 5, 6]
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
    cost = abs(1-leftmost_x_pos) + (3-leftmost_y_pos)
    '''# find displaced blocks for following Manhattan
    for y in range(leftmost_y_pos, 3):
        if config[y+2][leftmost_x_pos] != '0':
            cost += 1
        if config[y+2][leftmost_x_pos+1] != '0':
            cost += 1
            
    if leftmost_x_pos == 0:
        if config[3][2] != '0':
            cost += 1
        if config[4][2] != '0':
            cost += 1
    if leftmost_x_pos == 2:
        if config[3][1] != '0':
            cost += 1
        if config[4][1] != '0':
            cost += 1'''
    return cost

def get_successor(config, vertical, horizontal):

    path = []
    
    first_x, first_y, second_x, second_y = empty_space_locater(config)
    
    # Find successors for the first empty square
    # Left
    if first_x > 0:
        # Horizontal piece check
        if config[first_y][first_x - 1] in horizontal:
            new_state = copy.deepcopy(config)
            new_state[first_y][first_x - 2] = '0'
            new_state[first_y][first_x] = config[first_y][first_x - 1]
            path.append(new_state)
        # Single square check
        elif config[first_y][first_x - 1] == '7':
            new_state = copy.deepcopy(config)
            new_state[first_y][first_x - 1] = '0'
            new_state[first_y][first_x] = '7'
            path.append(new_state)
    
    # Right
    if first_x < 3:
        # Horizontal piece check
        if config[first_y][first_x + 1] in horizontal:
            new_state = copy.deepcopy(config)
            new_state[first_y][first_x + 2] = '0'
            new_state[first_y][first_x] = config[first_y][first_x + 1]
            path.append(new_state)
        # Single square check
        elif config[first_y][first_x + 1] == '7':
            new_state = copy.deepcopy(config)
            new_state[first_y][first_x + 1] = '0'
            new_state[first_y][first_x] = '7'
            path.append(new_state)
    
    # Top
    if first_y > 0:
        # Vertical piece check
        if config[first_y - 1][first_x] in vertical:
            new_state = copy.deepcopy(config)
            new_state[first_y - 2][first_x] = '0'
            new_state[first_y][first_x] = config[first_y - 1][first_x]
            path.append(new_state)
        # Single square check
        elif config[first_y - 1][first_x] == '7':
            new_state = copy.deepcopy(config)
            new_state[first_y - 1][first_x] = '0'
            new_state[first_y][first_x] = '7'
            path.append(new_state)
    
    # Bottom
    if first_y < 4:
        # Vertical piece check
        if config[first_y + 1][first_x] in vertical:
            new_state = copy.deepcopy(config)
            new_state[first_y + 2][first_x] = '0'
            new_state[first_y][first_x] = config[first_y + 1][first_x]
            path.append(new_state)
        # Single square check
        elif config[first_y + 1][first_x] == '7':
            new_state = copy.deepcopy(config)
            new_state[first_y + 1][first_x] = '0'
            new_state[first_y][first_x] = '7'
            path.append(new_state)
    
    # Find successors for the second empty square
    # Left
    if second_x > 0:
        # Horizontal piece check
        if config[second_y][second_x - 1] in horizontal:
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x] = config[second_y][second_x - 1]
            new_state[second_y][second_x - 2] = '0'
            path.append(new_state)
        # Single square check
        elif config[second_y][second_x - 1] == '7':
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x - 1] = '0'
            new_state[second_y][second_x] = '7'
            path.append(new_state)
        # First empty square check
        elif config[second_y][second_x - 1] == '0':
            if second_y < 4:
                if config[second_y + 1][second_x] in horizontal:
                    if config[second_y + 1][second_x] == config[second_y + 1][second_x - 1]:
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = config[second_y + 1][second_x]
                        new_state[second_y][second_x-1] = config[second_y + 1][second_x]
                        new_state[second_y + 1][second_x] = '0'
                        new_state[second_y + 1][second_x - 1] = '0'
                        path.append(new_state)
                elif config[second_y + 1][second_x] == '1':
                    if config[second_y + 1][second_x - 1] == '1':
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = '1'
                        new_state[second_y][second_x - 1] = '1'
                        new_state[second_y+2][second_x] = '0'
                        new_state[second_y+2][second_x - 1] = '0'
                        path.append(new_state)

            if second_y > 0:
                if config[second_y - 1][second_x] == '1':
                    if config[second_y - 1][second_x - 1] == '1':
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = '1'
                        new_state[second_y][second_x - 1] = '1'
                        new_state[second_y - 2][second_x - 1] = '0'
                        new_state[second_y - 2][second_x] = '0'
                        path.append(new_state)
                elif config[second_y - 1][second_x] in horizontal:
                    if config[second_y - 1][second_x - 1] == config[second_y - 1][second_x]:
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = config[second_y - 1][second_x]
                        new_state[second_y][second_x - 1] = config[second_y - 1][second_x]
                        new_state[second_y - 1][second_x - 1] = '0'
                        new_state[second_y - 1][second_x] = '0'
                        path.append(new_state)

    # Right
    if second_x < 3:
        # Single square check
        if config[second_y][second_x + 1] == '7':
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x + 1] = '0'
            new_state[second_y][second_x] = '7'
            path.append(new_state)
        # Horizontal piece check
        elif config[second_y][second_x + 1] in horizontal:
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x] = config[second_y][second_x + 1]
            new_state[second_y][second_x + 2] = '0'
            path.append(new_state)

    # Top
    if second_y > 0:
        # Vertical piece check
        if config[second_y - 1][second_x] in vertical:
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x] = config[second_y - 1][second_x]
            new_state[second_y - 2][second_x] = '0'
            path.append(new_state)
        # Single square check
        elif config[second_y - 1][second_x] == '7':
            new_state = copy.deepcopy(config)
            new_state[second_y - 1][second_x] = '0'
            new_state[second_y][second_x] = '7'
            path.append(new_state)
        # First empty square check
        elif config[second_y - 1][second_x] == '0':
            if second_x < 3:
                if config[second_y][second_x + 1] == '1':
                    if config[second_y - 1][second_x + 1] == '1':
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = '1'
                        new_state[second_y - 1][second_x] = '1'
                        new_state[second_y - 1][second_x + 2] = '0'
                        new_state[second_y][second_x + 2] = '0'
                        path.append(new_state)
                elif config[second_y][second_x + 1] in vertical:
                    if config[second_y - 1][second_x + 1] == config[second_y][second_x + 1]:
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = config[second_y][second_x + 1]
                        new_state[second_y - 1][second_x] = config[second_y][second_x + 1]
                        new_state[second_y - 1][second_x + 1] = '0'
                        new_state[second_y][second_x + 1] = '0'
                        path.append(new_state)
            if second_x > 0:
                if config[second_y][second_x - 1] == '1':
                    if config[second_y - 1][second_x - 1] == '1':
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = '1'
                        new_state[second_y - 1][second_x] = '1'
                        new_state[second_y - 1][second_x - 2] = '0'
                        new_state[second_y][second_x - 2] = '0'
                        path.append(new_state)
                elif config[second_y][second_x - 1] in vertical:
                    if config[second_y - 1][second_x - 1] == config[second_y][second_x - 1]:
                        new_state = copy.deepcopy(config)
                        new_state[second_y][second_x] = config[second_y][second_x - 1]
                        new_state[second_y-1][second_x] = config[second_y][second_x - 1]
                        new_state[second_y-1][second_x - 1] = '0'
                        new_state[second_y][second_x - 1] = '0'
                        path.append(new_state)

    # Bottom
    if second_y < 4:
        # Vertical piece check
        if config[second_y + 1][second_x] in vertical:
            new_state = copy.deepcopy(config)
            new_state[second_y][second_x] = config[second_y + 1][second_x]
            new_state[second_y + 2][second_x] = '0'
            path.append(new_state)
        # Single square check
        elif config[second_y + 1][second_x] == '7':
            new_state = copy.deepcopy(config)
            new_state[second_y + 1][second_x] = '0'
            new_state[second_y][second_x] = '7'
            path.append(new_state)
                        
    return path

vertical_pieces_list = vertical_pieces(puzzle)

horizontal_pieces_list = horizontal_pieces(puzzle, vertical_pieces_list)

def reflection(config):
    updated_config = copy.deepcopy(config)
    for i in range(cols):
        for j in range(rows):
            updated_config[i][j] = config[i][3-j]
    return updated_config

def hash_state(config, vertical, horizontal):
    # Replace all vertical squares by 'v' and all horizontal squares by 'h'
    updated_config = copy.deepcopy(config)
    for i in range(5):
        for j in range(4):
            if updated_config[i][j] in vertical:
                updated_config[i][j] = 'v'
            elif updated_config[i][j] in horizontal:
                updated_config[i][j] = 'h'
    
    return updated_config

# checks whether state is a goal state
def is_goal(state):
    return state[4][1] == '1' and state[4][2] == '1'

# A* Algorithm
def astar(config, vertical_pieces_list, horizontal_pieces_list):
    
    # Integer to track how many nodes have been explored
    nodes_num = 1

    # Initialize frontier, a set of frontier nodes, and a set of explored nodes
    frontier = []
    frontier_set = set()
    explore_set = set()

    # Path to actual solution
    solution = []
    solution.append(config)

    # Get the costs
    heuristic = manhattan_distance(config)
    cost = len(solution) - 1

    heapq.heappush(frontier, (cost + heuristic, solution))
    frontier_set.add(str(hash_state(config, vertical_pieces_list, horizontal_pieces_list)))

    # Enter a while loop until frontier isn't empty
    while frontier:
        # Select and remove state curr from Frontier
        curr = heapq.heappop(frontier)
        n_k = curr[-1][-1]
        nodes_num += 1

        hashed_n_k = str(hash_state(n_k, vertical_pieces_list, horizontal_pieces_list))
        print(hashed_n_k)

        if hashed_n_k not in explore_set:
            # Add the state to the explore set
            explore_set.add(hashed_n_k)
            # If curr is the goal state, return curr
            if n_k[4][1] == '1' and n_k[4][2] == '1':
                return solution, nodes_num
            # check all neighbour states
            for i in get_successor(n_k, vertical_pieces_list, horizontal_pieces_list):
                hashed_i = hash_state(i, vertical_pieces_list, horizontal_pieces_list)
    
                if str(hashed_i) not in frontier_set:
                    frontier_set.add(str(hashed_i))
                    frontier_set.add(str(reflection(hashed_i)))
                    solution = copy.copy(curr[-1])
                    solution.append(i)
                    heuristic = manhattan_distance(i)
                    cost = len(solution)-1
                    heapq.heappush(frontier, (heuristic + cost, solution))
    print (nodes_num)
    # Return no solution in the case that no path was found
    return 'No Solution'

# Output the dfs file
with open(dfs_filename, "w" ) as dfs_f:
    print("Hey", file=dfs_f)
 
# Output the A* file
with open(astar_filename, "w") as astar_f:
    print("Hello", file=astar_f)

end_time = time.time()
final_time = end_time - start_time

print(final_time)
print(astar(puzzle, vertical_pieces_list, horizontal_pieces_list))