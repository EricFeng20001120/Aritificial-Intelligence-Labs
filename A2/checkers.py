# Import libraries
import sys
import copy

# Get arguments from terminal
input_file = sys.argv[1]
output_file = sys.argv[2]

# Create global variables for the num of rows and columns
rows = 8
columns = 8

# Create a list of list for the board
board = [[] for x in range(rows)]

# Import the input.txt file and use a nested for loop to store characters
with open(input_file) as file:
    for i in range(rows):
        for j in range(columns):
            board[i].append(file.read(1))
        file.read(1)

# Function that finds the coordinates of a specific character given the configuration
def coordinates_locater(piece, config):
    index = []
    for i in range(rows):
        for j in range(columns):
            if config[i][j] == piece:
                index.append((i, j))
    return index

# Successor function
def successor(config):

    red_kings = coordinates_locater('R', config)
    red_pieces = coordinates_locater('r', config)
    print("Red piece coordinates: " + str(red_pieces))
    
    # Create successors for the single red piece
    for i in red_pieces:
        # Left Diagonal jump when not becoming King
        if i[0] > 2 and i[0] < 8 and i[1] > 1 and i[1] <= 7:
            if (config[i[0]-1][i[1]-1] == 'b' or config[i[0]-1][i[1]-1] == 'B'):
                config[i[0]-1][i[1]-1] = '.'
                config[i[0]][i[1]] = '.'
                config[i[0]-2][i[1]-2] = 'r'
                break
            
            # Left diagonal
            elif (config[i[0]-1][i[1]-1] == '.'):
                config[i[0]-1][i[1]-1] = 'r'
                config[i[0]][i[1]] = '.'
                break
        
        # Right Diagonal jump when not becoming King
        elif i[0] > 2 and i[0] < 8 and i[1] >= 0 and i[1] < 6: 
            if (config[i[0]-1][i[1]+1] == 'b' or config[i[0]-1][i[1]+1] == 'B'):
                config[i[0]-1][i[1]+1] = '.'
                config[i[0]][i[1]] = '.'
                config[i[0]-2][i[1]+2] = 'r'
                break
            
            elif(config[i[0]-1][i[1]+1] == '.'):
                config[i[0]-1][i[1]+1] = 'r'
                config[i[0]][i[1]] = '.'
                break

        # Left Diagonal jump when becoming King
        elif i[0] == 2 and i[1] > 1 and i[1] <= 7:
            if (config[i[0]-1][i[1]-1] == 'b' or config[i[0]-1][i[1]-1] == 'B'):
                config[i[0]-1][i[1]-1] = '.'
                config[i[0]][i[1]] = '.'
                config[i[0]-2][i[1]-2] = 'R'
                break

        # Right Diagonal jump when becoming King
        elif i[0] == 2 and i[1] >= 0 and i[1] < 6:
            if (config[i[0]-1][i[1]+1] == 'b' or config[i[0]-1][i[1]+1] == 'B'):
                config[i[0]-1][i[1]+1] = '.'
                config[i[0]][i[1]] = '.'
                config[i[0]-2][i[1]+2] = 'R'
                break
    
    return config

successor_nodes = successor(board)
new_board = [['.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', 'b', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', 'R'], ['.', '.', 'b', '.', 'b', '.', 'r', '.'], ['.', '.', '.', 'b', '.', '.', '.', '.'], ['.', '.', 'r', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', 'B', '.', '.', '.']]
print(successor_nodes)
print(successor(new_board))

# Output the file
output = open(output_file, "w")
for i in range(rows):
    for j in range(columns):
        output.write(str(board[i][j]))
    output.write("\n")
