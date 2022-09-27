import heapq
import copy
debug = False
import sys
filename = sys.argv[1]
# read in the initial state for puzzle(id)
def read_puzzle(id):
    
    puzzle = [[] for x in range(5)]
    
    with open(filename) as f:
        for i in range(5):
            for j in range(4):
                puzzle[i].append(f.read(1))
            f.read(1)
    
    return puzzle

# helper to locate indices of value
def find_indices(state, value):
    space_indices = []
    for i in range(5):
        for j in range(4):
            if state[i][j] == value:
                space_indices.append((i, j))
    
    return space_indices

orientation = []

# returns a list of all vertical 1 x 2 blocks
def find_vertical(state):
    
    vertical_list = []
    # figure out orientation of each type of block
    
    # 2
    indices = find_indices(state, '2')
    if indices[0][1] == indices[1][1]:
        vertical_list.append('2')
    # 3
    indices = find_indices(state, '3')
    if indices[0][1] == indices[1][1]:
        vertical_list.append('3')   
    # 4
    indices = find_indices(state, '4')
    if indices[0][1] == indices[1][1]:
        vertical_list.append('4')
    # 5
    indices = find_indices(state, '5')
    if indices[0][1] == indices[1][1]:
        vertical_list.append('5')
    # 6
    indices = find_indices(state, '6')
    if indices[0][1] == indices[1][1]:
        vertical_list.append('6')
    
    return vertical_list

if debug:
    test_puzzle = [['2', '1', '1', '3'], 
                   ['2', '1', '1', '3'], 
                   ['4', '6', '6', '5'], 
                   ['4', '7', '7', '5'], 
                   ['7', '0', '7', '0']]
    puzzle1=read_puzzle(1)
    print(puzzle1)
    print(find_indices(test_puzzle, '0'))
    vertical_blocks = find_vertical(puzzle1)
    print(vertical_blocks)

# checks whether state is a goal state
def is_goal(state):
    return state[4][1] == '1' and state[4][2] == '1'

if debug:
    print(is_goal(puzzle1))

def get_successor(state, vertical_blocks):
    
    all_blocks = ['2', '3', '4', '5', '6'] 
    horizontal_blocks = [i for i in all_blocks if i not in vertical_blocks]

    successor_list = []
    space_indices = find_indices(state, '0')
    
    y1 = space_indices[0][0]
    x1 = space_indices[0][1]
    y2 = space_indices[1][0]
    x2 = space_indices[1][1]
    
    # check first space
    
    # check top direction
    if y1 > 0:
        # add new state if the grid above the empty space is a 1 x 2 block
        if state[y1-1][x1] in vertical_blocks:
            new_state = copy.deepcopy(state)
            new_state[y1-2][x1] = '0'
            new_state[y1][x1] = state[y1-1][x1]
            successor_list.append(new_state)
        # add new state if the grid above the empty space is a single block
        elif state[y1-1][x1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y1-1][x1] = '0'
            new_state[y1][x1] = '7'
            successor_list.append(new_state)
    
    # check bottom direction
    if y1 < 4:
        
        # add new state if the grid below the empty space is a single block
        if state[y1+1][x1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y1+1][x1] = '0'
            new_state[y1][x1] = '7'
            successor_list.append(new_state)
        # add new state if the grid below the empty space is a 1 x 2 block
        elif state[y1+1][x1] in vertical_blocks:
            new_state = copy.deepcopy(state)
            new_state[y1+2][x1] = '0'
            new_state[y1][x1] = state[y1+1][x1]
            successor_list.append(new_state)
    
    # check left direction
    if x1 > 0:
        
        # add new state if the grid to the left of the empty space is a single block
        if state[y1][x1-1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y1][x1-1] = '0'
            new_state[y1][x1] = '7'
            successor_list.append(new_state)
        # add new state if the grid to the left of the empty space is a 2 x 1 block
        elif state[y1][x1-1] in horizontal_blocks:
            new_state = copy.deepcopy(state)
            new_state[y1][x1-2] = '0'
            new_state[y1][x1] = state[y1][x1-1]
            successor_list.append(new_state)
    
    # check right direction
    if x1 < 3:
        
        # add new state if the grid to the right of the empty space is a single block
        if state[y1][x1+1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y1][x1+1] = '0'
            new_state[y1][x1] = '7'
            successor_list.append(new_state)
        # add new state if the grid to the right of the empty space is a 2 x 1 block
        elif state[y1][x1+1] in horizontal_blocks:
            new_state = copy.deepcopy(state)
            new_state[y1][x1+2] = '0'
            new_state[y1][x1] = state[y1][x1+1]
            successor_list.append(new_state)
    
    # check second space
    
    # check top direction
    if y2 > 0:
        
        # add new state if the grid above the empty space is a single block
        if state[y2-1][x2] == '7':
            new_state = copy.deepcopy(state)
            new_state[y2-1][x2] = '0'
            new_state[y2][x2] = '7'
            successor_list.append(new_state)
        # add new state if the grid above the empty space is a 1 x 2 block
        elif state[y2-1][x2] in vertical_blocks:
            new_state = copy.deepcopy(state)
            new_state[y2][x2] = state[y2-1][x2]
            new_state[y2-2][x2] = '0'
            successor_list.append(new_state)
        # if block above is also empty
        elif state[y2-1][x2] == '0':
            # check the two grids to the left of the two empty grids
            if x2 > 0:
                if state[y2][x2-1] in vertical_blocks:
                    if state[y2-1][x2-1] == state[y2][x2-1]:
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = state[y2][x2-1]
                        new_state[y2-1][x2] = state[y2][x2-1]
                        new_state[y2-1][x2-1] = '0'
                        new_state[y2][x2-1] = '0'
                        successor_list.append(new_state)
                elif state[y2][x2-1] == '1':
                    if state[y2-1][x2-1] == '1':
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = '1'
                        new_state[y2-1][x2] = '1'
                        new_state[y2-1][x2-2] = '0'
                        new_state[y2][x2-2] = '0'
                        successor_list.append(new_state)
            # check the two grids to the right of the two empty grids
            if x2 < 3:
                if state[y2][x2+1] in vertical_blocks:
                    if state[y2-1][x2+1] == state[y2][x2+1]:
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = state[y2][x2+1]
                        new_state[y2-1][x2] = state[y2][x2+1]
                        new_state[y2-1][x2+1] = '0'
                        new_state[y2][x2+1] = '0'
                        successor_list.append(new_state)
                elif state[y2][x2+1] == '1':
                    if state[y2-1][x2+1] == '1':
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = '1'
                        new_state[y2-1][x2] = '1'
                        new_state[y2-1][x2+2] = '0'
                        new_state[y2][x2+2] = '0'
                        successor_list.append(new_state)

    # check bottom direction
    if y2 < 4:

        # add new state if the grid below the empty space is a single block
        if state[y2+1][x2] == '7':
            new_state = copy.deepcopy(state)
            new_state[y2+1][x2] = '0'
            new_state[y2][x2] = '7'
            successor_list.append(new_state)
        # add new state if the grid below the empty space is a 1 x 2 block
        elif state[y2+1][x2] in vertical_blocks:
            new_state = copy.deepcopy(state)
            new_state[y2][x2] = state[y2+1][x2]
            new_state[y2+2][x2] = '0'
            successor_list.append(new_state)
        

    # check left direction
    if x2 > 0:

        # add new state if the grid to the left of the empty space is a single block
        if state[y2][x2-1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y2][x2-1] = '0'
            new_state[y2][x2] = '7'
            successor_list.append(new_state)
        # add new state if the grid to the left of the empty space is a 2 x 1 block
        elif state[y2][x2-1] in horizontal_blocks:
            new_state = copy.deepcopy(state)
            new_state[y2][x2] = state[y2][x2-1]
            new_state[y2][x2-2] = '0'
            successor_list.append(new_state)
        # if block to the left is also empty
        elif state[y2][x2-1] == '0':
            # check the two grids to the top of the two empty grids
            if y2 > 0:
                if state[y2-1][x2] in horizontal_blocks:
                    if state[y2-1][x2-1] == state[y2-1][x2]:
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = state[y2-1][x2]
                        new_state[y2][x2-1] = state[y2-1][x2]
                        new_state[y2-1][x2-1] = '0'
                        new_state[y2-1][x2] = '0'
                        successor_list.append(new_state)
                elif state[y2-1][x2] == '1':
                    if state[y2-1][x2-1] == '1':
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = '1'
                        new_state[y2][x2-1] = '1'
                        new_state[y2-2][x2-1] = '0'
                        new_state[y2-2][x2] = '0'
                        successor_list.append(new_state)

            # check the two grids to the bottom of the two empty grids
            if y2 < 4:
                if state[y2+1][x2] in horizontal_blocks:
                    if state[y2+1][x2] == state[y2+1][x2-1]:
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = state[y2+1][x2]
                        new_state[y2][x2-1] = state[y2+1][x2]
                        new_state[y2+1][x2] = '0'
                        new_state[y2+1][x2-1] = '0'
                        successor_list.append(new_state)
                elif state[y2+1][x2] == '1':
                    if state[y2+1][x2-1] == '1':
                        new_state = copy.deepcopy(state)
                        new_state[y2][x2] = '1'
                        new_state[y2][x2-1] = '1'
                        new_state[y2+2][x2] = '0'
                        new_state[y2+2][x2-1] = '0'
                        successor_list.append(new_state)

    # check right direction
    if x2 < 3:
        # add new state if the grid to the right of the empty space is a single block
        if state[y2][x2+1] == '7':
            new_state = copy.deepcopy(state)
            new_state[y2][x2+1] = '0'
            new_state[y2][x2] = '7'
            successor_list.append(new_state)
        # add new state if the grid to the right of the empty space is a 2 x 1 block
        elif state[y2][x2+1] in horizontal_blocks:
            new_state = copy.deepcopy(state)
            new_state[y2][x2] = state[y2][x2+1]
            new_state[y2][x2+2] = '0'
            successor_list.append(new_state)
        
                        
    return successor_list
flag = True
if flag:
    test_state1 = [['2', '1', '1', '3'], 
                   ['2', '1', '1', '3'], 
                   ['4', '6', '6', '5'], 
                   ['4', '7', '7', '5'], 
                   ['7', '0', '0', '7']]
    
    test_state2 = [['2', '1', '1', '5'], 
                   ['2', '1', '1', '5'], 
                   ['7', '4', '0', '3'], 
                   ['7', '4', '0', '3'], 
                   ['6', '6', '7', '7']]
    
    test_state3 = [['2', '1', '1', '3'], 
                   ['2', '1', '1', '3'], 
                   ['7', '4', '0', '0'], 
                   ['7', '4', '7', '5'], 
                   ['6', '6', '7', '5']]
    
    test_state4 = [['2', '1', '1', '0'], 
                   ['2', '1', '1', '3'], 
                   ['6', '6', '5', '3'], 
                   ['0', '0', '5', '0'], 
                   ['6', '6', '7', '7']]
    
    test_state5 = [['2', '1', '1', '0'], 
                   ['2', '1', '1', '3'], 
                   ['6', '6', '0', '3'], 
                   ['x', 'x', '5', 'x'], 
                   ['6', '6', '7', '7']]
    
    test_state6 = [['2', '1', '1', 'x'], 
                   ['1', '1', '0', '3'], 
                   ['1', '1', '0', '3'], 
                   ['x', 'x', '5', 'x'], 
                   ['6', '6', '7', '7']]
    
    test_state7 = [['2', '1', '1', 'x'], 
                   ['1', '1', 'x', '3'], 
                   ['1', '1', 'x', '3'], 
                   ['x', '0', '1', '1'], 
                   ['x', '0', '1', '1']]
    
    test_state8 = [['2', '1', '1', 'x'], 
                   ['1', '1', 'x', '3'], 
                   ['1', '1', 'x', '3'], 
                   ['0', '0', '1', '1'], 
                   ['x', '1', '1', '1']]
    
    test_state9 = [['0', '0', '1', 'x'], 
                   ['1', '1', 'x', '3'], 
                   ['1', '1', 'x', '3'], 
                   ['0', '0', '1', '1'], 
                   ['x', '1', '1', '1']]
    
    test_state10 = [['2', '1', '1', '3'], 
                   ['2', '1', '1', '3'], 
                   ['4', '6', '6', '5'], 
                   ['4', '0', '0', '5'], 
                   ['7', '7', '7', '7']]
    
    succ = get_successor(test_state10, find_vertical(test_state10))
    print(succ)
# helper to get cost of path
def get_cost(path):
    return len(path) - 1

# helper to find improved Manhattan distance of a state
def get_heuristic(state):
    
    # find Manhattan distance
    indices = find_indices(state, '1')
    top_left_y = indices[0][0]
    top_left_x = indices[0][1]
    cost = (3 - top_left_y) + abs(1 - top_left_x)
    
    '''# find displaced blocks for following Manhattan
    for y in range(top_left_y, 3):
        if state[y+2][top_left_x] != '0':
            cost += 1
        if state[y+2][top_left_x+1] != '0':
            cost += 1
            
    if top_left_x == 0:
        if state[3][2] != '0':
            cost += 1
        if state[4][2] != '0':
            cost += 1
    if top_left_x == 2:
        if state[3][1] != '0':
            cost += 1
        if state[4][1] != '0':
            cost += 1'''
    return cost
if debug:
    test_state = [['2', '1', '1', '0'], 
                  ['2', '1', '1', '3'], 
                  ['7', '4', '5', '3'], 
                  ['7', '4', '5', '0'], 
                  ['6', '6', '7', '7']]
    print(get_heuristic(test_state))

# abstract away 1x2 blocks
def hash_state(state, vertical_blocks):
    
    # find horizontal blocks
    all_blocks = ['2', '3', '4', '5', '6'] 
    horizontal_blocks = [i for i in all_blocks if i not in vertical_blocks]
    
    # replace all vertical squares by 'v' and all horizontal squares by 'h'
    new_state = copy.deepcopy(state)
    for i in range(5):
        for j in range(4):
            if new_state[i][j] in vertical_blocks:
                new_state[i][j] = 'v'
            elif new_state[i][j] in horizontal_blocks:
                new_state[i][j] = 'h'
    
    return new_state

if debug:
    hashed = hash_state(puzzle1, vertical_blocks)

# flip state over y-axis
def flip_state(state):
    new_state = copy.deepcopy(state)
    for i in range(5):
        for j in range(4):
            new_state[i][j] = state[i][3-j]
    return new_state

# A* search algorithm
def a_star(initial_state):

    # keep track of the number of nodes expanded
    num_expanded = 1
    
    # start with a path consisting of only the initial_state
    path = []
    path.append(initial_state)
    
    # use a set in_frontier to keep track of all paths in frontier
    frontier = []
    in_frontier = set()

    # add initial path to heap
    heuristic = get_heuristic(initial_state)
    cost = get_cost(path)
    heapq.heappush(frontier, (heuristic + cost, path))
    in_frontier.add(str(hash_state(initial_state, vertical_blocks)))
    
    # explored set starts empty
    explored = set()
    
    while frontier:
        # retrieve the current path
        curpath = heapq.heappop(frontier)
        n_k = curpath[-1][-1]
        num_expanded = num_expanded + 1
        
        # check if the abstracted state has been explored
        hashed_n_k = str(hash_state(n_k, vertical_blocks))

        if hashed_n_k not in explored:
            explored.add(hashed_n_k)
            # we have found the path
            if (is_goal(n_k)):
                return curpath, num_expanded
            # check all neighbour states
            for i in get_successor(n_k, vertical_blocks):
                hashed_i = hash_state(i, vertical_blocks)
    
                if str(hashed_i) not in in_frontier:
                    in_frontier.add(str(hashed_i))
                    in_frontier.add(str(flip_state(hashed_i)))
                    path = copy.copy(curpath[-1])
                    path.append(i)
                    heuristic = get_heuristic(i)
                    cost = len(path)-1
                    heapq.heappush(frontier, (heuristic + cost, path))
                    
    return 'no soln'

if debug:
    soln, num_expanded = a_star(test_state)

# dfs algorithm
def dfs(initial_state):
    
    # keep track of the number of nodes expanded
    num_expanded = 1
    
    # start with a path consisting of only the initial_state
    path = []
    path.append(initial_state)
    
    # use a set in_frontier to keep track of all paths in frontier
    frontier = []
    in_frontier = set()
    
    # add initial path to stack
    frontier.append(path)
    in_frontier.add(str(hash_state(initial_state, vertical_blocks)))
    
    # explored set starts empty
    explored = set()
    
    while frontier:
        
        curpath = frontier.pop()
        n_k = curpath[-1]
        num_expanded = num_expanded + 1
        
        hashed_n_k = str(hash_state(n_k, vertical_blocks))
        if hashed_n_k not in explored:
            explored.add(hashed_n_k)
            if (is_goal(n_k)):
                return curpath, num_expanded
            for i in get_successor(n_k, vertical_blocks):
                hashed_i = hash_state(i, vertical_blocks)
                if str(hashed_i) not in in_frontier:
                    in_frontier.add(str(hashed_i))
                    in_frontier.add(str(flip_state(hashed_i)))
                    path = copy.copy(curpath)
                    path.append(i)
                    
                    
                    frontier.append(path)
                    
    return 'no soln', 'no soln'

if debug:
    soln, num_expanded = dfs(test_state)

# solve puzzles
# take in first puzzle
puzzle1=read_puzzle(1)

# find all vertical 1 x 2 blocks
vertical_blocks = find_vertical(puzzle1)

# run A* on the first puzzle
soln1_astar, num_expanded1_astar = a_star(puzzle1)
print(num_expanded1_astar)

# run dfs on the first puzzle
soln1_dfs, num_expanded1_dfs = dfs(puzzle1)

print(num_expanded1_dfs)
