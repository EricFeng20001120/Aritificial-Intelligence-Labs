import sys
import time

start_time = time.time()

# Set the three parameters to pass in
filename = sys.argv[1]
dfs_filename = sys.argv[2]
astar_filename = sys.argv[3]

# Create a 4x5 array to store the digits of the puzzle
puzzle = [[] for x in range(5)]

# Import the puzzle.txt file and use a nested for loop to store digits
with open(filename) as file:
    for i in range(5):
        for j in range(4):
            puzzle[i].append(file.read(1))
        file.read(1)

print(puzzle)

# Function that finds the coordinates of state and value of a specific digit
def coordinates_locater(state, value):
    index = []
    for i in range(5):
        for j in range(4):
            if state[i][j] == value:
                index.append((i, j))
    return index

with open(dfs_filename, "w" ) as dfs_f:
    print("Hey", file=dfs_f)
 
with open(astar_filename, "w") as astar_f:
    print("Hello", file=astar_f)

end_time = time.time()
final_time = end_time - start_time

print(final_time)

print(coordinates_locater(puzzle, '1'))