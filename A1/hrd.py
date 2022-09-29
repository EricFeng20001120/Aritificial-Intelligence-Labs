# Import necessary libraries
import sys
import copy
import heapq

# Create global variables for the number of columns and columns of the board
rows = 5
columns = 4

# Set the three parameters to pass in
filename = sys.argv[1]
dfs_filename = sys.argv[2]
astar_filename = sys.argv[3]

# Create a 5x4 array to store the digits of the puzzle
puzzle = [[] for x in range(rows)]

# Import the puzzle.txt file and use a nested for loop to store digits
with open(filename) as file:
    for i in range(rows):
        for j in range(columns):
            puzzle[i].append(file.read(1))
        file.read(1)

# Function that finds the coordinates of a specific digit given the configuration
def coordinates_locater(digit, config):
    index = []
    for i in range(rows):
        for j in range(columns):
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
    # Get the top and rightmost location from Cao Cao
    bottom_left_x_pos, bottom_left_y_pos = index_of_ones[2][1], index_of_ones[2][0]
    # Calculate the number of steps it would take for Cao Cao to get to the bottom centre of the puzzle
    manhattan_cost = abs(1-bottom_left_x_pos) + (4-bottom_left_y_pos)
    return manhattan_cost

# Original heuristic function implementation
def original_heuristic(config):
    # Find indices of the Cao Cao piece
    index_of_ones = coordinates_locater('1', config)
    # Get the top and rightmost location from Cao Cao
    bottom_left_x_pos, bottom_left_y_pos = index_of_ones[2][1], index_of_ones[2][0]
    # Find Manhattan cost
    total_cost = manhattan_distance(config)

    # Check if the 2x2 is at the left edge and if the 0s are where they need to be for the 2x2 to go to the finish
    if bottom_left_x_pos == 0:
        if config[3][2] != '0':
            total_cost += 1
        if config[4][2] != '0':
            total_cost += 1

    # Check if the 2x2 is at the right edge and if the 0s are where they need to be for the 2x2 to go to the finish
    if bottom_left_x_pos == 2:
        if config[3][1] != '0':
            total_cost += 1
        if config[4][1] != '0':
            total_cost += 1
    
    # Check in a for loop of the horizontal adjacency of empty spaces to the 2x2 piece and add a cost if empty space isn't there
    for y in range(bottom_left_y_pos, 4):
        if config[y + 1][bottom_left_x_pos + 1] != '0':
            total_cost += 1
        if config[y + 1][bottom_left_x_pos] != '0':
            total_cost += 1
    
    return total_cost

# Successor function which examines all possibilities
def successor_nodes(config, vertical, horizontal):
    path = []
    
    # Find coordinates of empty squares
    first_x, first_y, second_x, second_y = empty_space_locater(config)
    
    # Find successors for the first empty square
    # Left
    if first_x > 0:
        # Horizontal piece check
        if config[first_y][first_x - 1] in horizontal:
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x - 2] = '0'
            updated_config[first_y][first_x] = config[first_y][first_x - 1]
            path.append(updated_config)
        # Single square check
        elif config[first_y][first_x - 1] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x - 1] = '0'
            updated_config[first_y][first_x] = '7'
            path.append(updated_config)
    
    # Right
    if first_x < 3:
        # Horizontal piece check
        if config[first_y][first_x + 1] in horizontal:
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x + 2] = '0'
            updated_config[first_y][first_x] = config[first_y][first_x + 1]
            path.append(updated_config)
        # Single square check
        elif config[first_y][first_x + 1] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x + 1] = '0'
            updated_config[first_y][first_x] = '7'
            path.append(updated_config)
    
    # Top
    if first_y > 0:
        # Vertical piece check
        if config[first_y - 1][first_x] in vertical:
            updated_config = copy.deepcopy(config)
            updated_config[first_y - 2][first_x] = '0'
            updated_config[first_y][first_x] = config[first_y - 1][first_x]
            path.append(updated_config)
        # Single square check
        elif config[first_y - 1][first_x] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[first_y - 1][first_x] = '0'
            updated_config[first_y][first_x] = '7'
            path.append(updated_config)
    
    # Bottom
    if first_y < 4:
        # Vertical piece check
        if config[first_y + 1][first_x] in vertical:
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x] = config[first_y + 1][first_x]
            updated_config[first_y + 2][first_x] = '0'
            path.append(updated_config)
        # Single square check
        elif config[first_y + 1][first_x] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[first_y][first_x] = '7'
            updated_config[first_y + 1][first_x] = '0'
            path.append(updated_config)
    
    # Find successors for the second empty square
    # Left
    if second_x > 0:
        # Horizontal piece check
        if config[second_y][second_x - 1] in horizontal:
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x - 2] = '0'
            updated_config[second_y][second_x] = config[second_y][second_x - 1]
            path.append(updated_config)
        # Single square check
        elif config[second_y][second_x - 1] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x] = '7'
            updated_config[second_y][second_x - 1] = '0'
            path.append(updated_config)
        # First empty square check
        elif config[second_y][second_x - 1] == '0':
            if second_y < 4:
                if config[second_y + 1][second_x] in horizontal:
                    if config[second_y + 1][second_x] == config[second_y + 1][second_x - 1]:
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y][second_x-1] = config[second_y + 1][second_x]
                        updated_config[second_y][second_x] = config[second_y + 1][second_x]                      
                        updated_config[second_y + 1][second_x - 1] = '0'
                        updated_config[second_y + 1][second_x] = '0'                       
                        path.append(updated_config)
                elif config[second_y + 1][second_x] == '1':
                    if config[second_y + 1][second_x - 1] == '1':
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y][second_x - 1] = '1'
                        updated_config[second_y][second_x] = '1'
                        updated_config[second_y+2][second_x - 1] = '0'
                        updated_config[second_y+2][second_x] = '0'
                        path.append(updated_config)

            if second_y > 0:
                if config[second_y - 1][second_x] == '1':
                    if config[second_y - 1][second_x - 1] == '1':
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y - 2][second_x - 1] = '0'
                        updated_config[second_y - 2][second_x] = '0'
                        updated_config[second_y][second_x] = '1'
                        updated_config[second_y][second_x - 1] = '1'
                        path.append(updated_config)
                elif config[second_y - 1][second_x] in horizontal:
                    if config[second_y - 1][second_x - 1] == config[second_y - 1][second_x]:
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y][second_x] = config[second_y - 1][second_x]
                        updated_config[second_y][second_x - 1] = config[second_y - 1][second_x]
                        updated_config[second_y - 1][second_x - 1] = '0'
                        updated_config[second_y - 1][second_x] = '0'
                        path.append(updated_config)

    # Right
    if second_x < 3:
        # Single square check
        if config[second_y][second_x + 1] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x] = '7'
            updated_config[second_y][second_x + 1] = '0'
            path.append(updated_config)
        # Horizontal piece check
        elif config[second_y][second_x + 1] in horizontal:
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x + 2] = '0'
            updated_config[second_y][second_x] = config[second_y][second_x + 1]
            path.append(updated_config)

    # Top
    if second_y > 0:
        # Vertical piece check
        if config[second_y - 1][second_x] in vertical:
            updated_config = copy.deepcopy(config)
            updated_config[second_y - 2][second_x] = '0'
            updated_config[second_y][second_x] = config[second_y - 1][second_x]
            path.append(updated_config)
        # Single square check
        elif config[second_y - 1][second_x] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x] = '7'
            updated_config[second_y - 1][second_x] = '0'
            path.append(updated_config)
        # First empty square check
        elif config[second_y - 1][second_x] == '0':
            if second_x < 3:
                if config[second_y][second_x + 1] == '1':
                    if config[second_y - 1][second_x + 1] == '1':
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y - 1][second_x + 2] = '0'
                        updated_config[second_y][second_x + 2] = '0'
                        updated_config[second_y][second_x] = '1'
                        updated_config[second_y - 1][second_x] = '1'
                        path.append(updated_config)
                elif config[second_y][second_x + 1] in vertical:
                    if config[second_y - 1][second_x + 1] == config[second_y][second_x + 1]:
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y - 1][second_x + 1] = '0'
                        updated_config[second_y][second_x + 1] = '0'
                        updated_config[second_y][second_x] = config[second_y][second_x + 1]
                        updated_config[second_y - 1][second_x] = config[second_y][second_x + 1]
                        path.append(updated_config)
            if second_x > 0:
                if config[second_y][second_x - 1] == '1':
                    if config[second_y - 1][second_x - 1] == '1':
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y - 1][second_x - 2] = '0'
                        updated_config[second_y][second_x - 2] = '0'
                        updated_config[second_y][second_x] = '1'
                        updated_config[second_y - 1][second_x] = '1'
                        path.append(updated_config)
                elif config[second_y][second_x - 1] in vertical:
                    if config[second_y - 1][second_x - 1] == config[second_y][second_x - 1]:
                        updated_config = copy.deepcopy(config)
                        updated_config[second_y-1][second_x - 1] = '0'
                        updated_config[second_y][second_x - 1] = '0'
                        updated_config[second_y][second_x] = config[second_y][second_x - 1]
                        updated_config[second_y-1][second_x] = config[second_y][second_x - 1]
                        path.append(updated_config)

    # Bottom
    if second_y < 4:
        # Vertical piece check
        if config[second_y + 1][second_x] in vertical:
            updated_config = copy.deepcopy(config)
            updated_config[second_y + 2][second_x] = '0'
            updated_config[second_y][second_x] = config[second_y + 1][second_x]
            path.append(updated_config)
        # Single square check
        elif config[second_y + 1][second_x] == '7':
            updated_config = copy.deepcopy(config)
            updated_config[second_y][second_x] = '7'
            updated_config[second_y + 1][second_x] = '0'
            path.append(updated_config)
                        
    return path

# Reflects the board over the vertical axis
def reflection(config):
    updated_config = copy.deepcopy(config)
    for i in range(rows):
        for j in range(columns):
            updated_config[i][j] = config[i][3-j]
    return updated_config

# Hashing
def updated_puzzle(config, vertical, horizontal):
    updated_config = copy.deepcopy(config)
    for i in range(5):
        for j in range(4):
            if updated_config[i][j] in vertical:
                updated_config[i][j] = 'vertical'
            elif updated_config[i][j] in horizontal:
                updated_config[i][j] = 'horizontal'
    
    return updated_config

# Depth first search algorithm
def dfs(config, vertical_pieces_list, horizontal_pieces_list):
    # Integer to track how many nodes have been explored
    nodes_num = 1

    # Initialize frontier, a set of frontier nodes, and a set of explored nodes
    frontier = []
    frontier_set = set()
    explore_set = set()

    # Path to actual solution
    solution = []
    solution.append(config)

    frontier.append(solution)
    frontier_set.add(str(updated_puzzle(config, vertical_pieces_list, horizontal_pieces_list)))

    # Enter a while loop until frontier isn't empty
    while frontier:
        # Select and remove state curr from Frontier
        nodes_num += 1
        curr = frontier.pop()
        nodes = curr[-1]
        nodes_h = str(updated_puzzle(nodes, vertical_pieces_list, horizontal_pieces_list))

        if nodes_h not in explore_set:
            # Add the state to the explore set
            explore_set.add(nodes_h)
            
            # If curr is the goal state, return curr
            if nodes[4][1] == '1' and nodes[4][2] == '1':
                return curr
            
            # Successor possibilities
            for i in successor_nodes(nodes, vertical_pieces_list, horizontal_pieces_list):
                hashed_i = updated_puzzle(i, vertical_pieces_list, horizontal_pieces_list)
                if str(hashed_i) not in frontier_set:
                    frontier_set.add(str(hashed_i))
                    frontier_set.add(str(reflection(hashed_i)))
                    solution = copy.copy(curr)
                    solution.append(i)

                    frontier.append(solution)

    # Return no solution in the case that no path was found
    return 'No Solution'

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
    frontier_set.add(str(updated_puzzle(config, vertical_pieces_list, horizontal_pieces_list)))

    # Enter a while loop until frontier isn't empty
    while frontier:
        # Select and remove state curr from Frontier
        nodes_num += 1
        curr = heapq.heappop(frontier)
        nodes = curr[-1][-1]
        nodes_h = str(updated_puzzle(nodes, vertical_pieces_list, horizontal_pieces_list))

        if nodes_h not in explore_set:
            # Add the state to the explore set
            explore_set.add(nodes_h)
            
            # If curr is the goal state, return curr
            if nodes[4][1] == '1' and nodes[4][2] == '1':
                return curr
            
            # Successor possibilities
            for i in successor_nodes(nodes, vertical_pieces_list, horizontal_pieces_list):
                hashed_i = updated_puzzle(i, vertical_pieces_list, horizontal_pieces_list)
                if str(hashed_i) not in frontier_set:
                    frontier_set.add(str(hashed_i))
                    frontier_set.add(str(reflection(hashed_i)))
                    solution = copy.copy(curr[-1])
                    solution.append(i)
                    heuristic = manhattan_distance(i)
                    cost = len(solution)-1
                    heapq.heappush(frontier, (heuristic + cost, solution))

    # Return no solution in the case that no path was found
    return 'No Solution'

# Get lists of the vertical and horizontal pieces
vertical_pieces_list = vertical_pieces(puzzle)
horizontal_pieces_list = horizontal_pieces(puzzle, vertical_pieces_list)

# Get dfs solution and cost
dfs_solution = dfs(puzzle, vertical_pieces_list, horizontal_pieces_list)
dfs_cost = len(dfs_solution)-1

# Get A* soplution and cost
astar_solution = astar(puzzle, vertical_pieces_list, horizontal_pieces_list)
astar_cost = len(astar_solution[1])-1

# Output the A* file
astar_f = open(astar_filename, "w")
astar_f.write("Cost of solution: " + str(astar_cost))
for x in range(len(astar_solution[1])):
    astar_f.write("\n")
    for i in range(rows):
        for j in range(columns):
            # Update to 2 if it is a horizontal piece 
            if str(astar_solution[1][x][i][j]) in horizontal_pieces_list:
                astar_solution[1][x][i][j] = '2'
            # Update to 3 if it is a vertical piece
            elif str(astar_solution[1][x][i][j]) in vertical_pieces_list:
                astar_solution[1][x][i][j] = '3'
            # Update to 4 if it is a singular piece
            elif str(astar_solution[1][x][i][j]) == '7':
                astar_solution[1][x][i][j] = '4'
            astar_f.write((str(astar_solution[1][x][i][j])))
        astar_f.write("\n")
        
# Output the dfs file
dfs_f = open(dfs_filename, "w")
dfs_f.write("Cost of solution: " + str(dfs_cost))
for x in range (len(dfs_solution)):
    dfs_f.write("\n")
    for i in range(rows):
        for j in range(columns):
            # Addressing a weird edge case where the first entry isn't what's expected
            if x == 0:
                dfs_f.write((str(dfs_solution[x][i][j])))
            else:
                # Update to 2 if it is a horizontal piece
                if str(dfs_solution[x][i][j]) in horizontal_pieces_list:
                    dfs_solution[x][i][j] = '2'
                # Update to 3 if it is a vertical piece
                elif str(dfs_solution[x][i][j]) in vertical_pieces_list:
                    dfs_solution[x][i][j] = '3'
                # Update to 4 if it is a singular piece
                elif str(dfs_solution[x][i][j]) == '7':
                    dfs_solution[x][i][j] = '4'
                dfs_f.write((str(dfs_solution[x][i][j])))
        dfs_f.write("\n")