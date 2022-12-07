from collections import defaultdict, deque
from copy import deepcopy
import sys
from tkinter import Variable

row_const = []
col_const = []
ship_const = {"S": 0, "D": 0, "C": 0, "B": 0}
dim = 0
variables = []


class State:
    """A state is a table of all the tiles with given initial locations.
    """

    def __init__(self, ships=None, assigned=None, data=None, parent=None):
        self.ships = ships
        self.assigned = assigned
        self.data = data
        self.parent = parent
        if self.parent:
            self.cost = parent.cost + 1
        else:
            self.cost = 0

    # for node ordering
    # def __gt__(self, state):
    #     return self.cost > state.cost

    # def __lt__(self, state):
    #     return self.cost < state.cost

    def get_domain(self):
        return self.domain

    def get_data(self):
        """ return curr data"""
        return self.data

    def get_parent(self):
        """ return the parent of curr state"""
        return self.parent


def preprocessing(state):  # checked
    """ filled the water to squares needed on board"""

    # surround my_ship with W
    update_data(state.data)
    # print("after update_data: \n", print_data(state))

    # add W based on row & col constraints
    update_const(state.data)
    # print("after update_const: \n", print_data(state))


def update_data(data):  # checked
    """
    update the grid by surround my_ship with W
    """
    for i in range(dim):
        for j in range(dim):

            # skip this square to boost efficiency
            if data[i][j] == '0':
                continue
            # if single submarine, surround it with water
            if data[i][j] == 'S':
                if i != 0:
                    data[i-1][j] = 'W'
                    if j != 0:
                        data[i-1][j-1] = 'W'
                    if j != dim-1:
                        data[i-1][j+1] = 'W'
                if j != 0:
                    data[i][j-1] = 'W'
                if j != dim-1:
                    data[i][j+1] = 'W'
                if i != dim-1:
                    data[i+1][j] = 'W'
                    if j != 0:
                        data[i+1][j-1] = 'W'
                    if j != dim-1:
                        data[i+1][j+1] = 'W'
            # if left end, add M to its right and filled needed squares with W
            elif data[i][j] == 'L':
                # add W's
                if i != 0:
                    data[i-1][j] = 'W'
                    if j != 0:
                        data[i-1][j-1] = 'W'
                    if j != dim-1:
                        data[i-1][j+1] = 'W'
                if j != 0:
                    data[i][j-1] = 'W'
                if i != dim-1:
                    data[i+1][j] = 'W'
                    if j != 0:
                        data[i+1][j-1] = 'W'
                    if j != dim-1:
                        data[i+1][j+1] = 'W'

            # if right end, add M to its left and filled needed squares with W
            elif data[i][j] == 'R':
                if i != 0:
                    data[i-1][j] = 'W'
                    if j != 0:
                        data[i-1][j-1] = 'W'
                    if j != dim-1:
                        data[i-1][j+1] = 'W'
                if j != dim-1:
                    data[i][j+1] = 'W'
                if i != dim-1:
                    data[i+1][j] = 'W'
                    if j != 0:
                        data[i+1][j-1] = 'W'
                    if j != dim-1:
                        data[i+1][j+1] = 'W'

            # if top end, add M to its bottom and filled needed squares with W
            elif data[i][j] == 'T':
                if i != 0:
                    data[i-1][j] = 'W'
                    if j != 0:
                        data[i-1][j-1] = 'W'
                    if j != dim-1:
                        data[i-1][j+1] = 'W'
                if j != 0:
                    data[i][j-1] = 'W'
                if j != dim-1:
                    data[i][j+1] = 'W'
                if i != dim-1:
                    if j != 0:
                        data[i+1][j-1] = 'W'
                    if j != dim-1:
                        data[i+1][j+1] = 'W'

            # if bottom end, add M to its top and filled needed squares with W
            elif data[i][j] == 'B':
                if i != 0:
                    if j != 0:
                        data[i-1][j-1] = 'W'
                    if j != dim-1:
                        data[i-1][j+1] = 'W'
                if j != 0:
                    data[i][j-1] = 'W'
                if j != dim-1:
                    data[i][j+1] = 'W'
                if i != dim-1:
                    data[i+1][j] = 'W'
                    if j != 0:
                        data[i+1][j-1] = 'W'
                    if j != dim-1:
                        data[i+1][j+1] = 'W'


def update_const(data):  # checked
    """
    update the board based on row, col, my_ship const
    """
    if match_ships(data):
        # my_ship number matched, filled the rest of the board with W
        # print("my_ship checked")
        for i in range(dim):
            for j in range(dim):
                if data[i][j] == '0':
                    data[i][j] = 'W'
        return

    for i in range(len(row_const)):
        if match_row_const(data, i):
            # row_num matches, need to filled out the rest squares on this row with W
            # print("row number " + str(i) + " is satisfied")
            for j in range(dim):
                if data[i][j] == '0':
                    data[i][j] = 'W'
        if match_col_const(data, i):
            # col_num matches, need to filled out the rest squares on this row with W
            # print("col number " + str(i) + " is satified")
            for j in range(dim):
                if data[j][i] == '0':
                    data[j][i] = 'W'


def match_row_const(data, row_num):  # checked
    """ check if assigning ship on board cause the num filled square match the row const number"""
    row = data[row_num]
    total = 0
    for i in range(len(row)):
        if row[i] != '0' and row[i] != 'W':
            total += 1
    if total == row_const[row_num]:
        return True
    else:
        return False


def check_row_const(data, row_num):  # checked
    """ check if assigning new ship will exceed the col number, data should be new_data"""
    row = data[row_num]
    total = 0
    for i in range(len(row)):
        if row[i] != '0' and row[i] != 'W':
            total += 1
    if total <= row_const[row_num]:
        return True
    else:
        return False


def match_col_const(data, col_num):  # checked
    """ 
    check if assigning ship on board cause the num filled square match the col const number
    should be called after assigned the ship
    """
    col = [data[i][col_num] for i in range(len(data))]
    total = 0
    for i in range(len(col)):
        if col[i] != '0' and col[i] != 'W':
            total += 1
    if total == col_const[col_num]:
        return True
    else:
        return False


def check_col_const(data, col_num):  # checked
    """ check if assigning new ship will exceed the col number, data should be new_data"""
    col = [data[i][col_num] for i in range(len(data))]
    total = 0
    for i in range(len(col)):
        if col[i] != '0' and col[i] != 'W':
            total += 1
    if total <= col_const[col_num]:
        return True
    else:
        return False


def count_ships(data):
    sub_num = 0
    des_num = 0
    crui_num = 0
    bat_num = 0
    length = len(data[0])
    for i in range(length):
        for j in range(length):
            if data[i][j] == '0' or data[i][j] == 'W':
                continue
            if data[i][j] == 'S':  # submarine 1x1
                sub_num += 1
            elif data[i][j] == 'T':  # vertical destroyer 1x2 or cruiser 1x3 or battleship 1x4
                if data[i+1][j] == 'M':  # cruiser 1x3 or battleship 1x4
                    if data[i+2][j] == 'M':  # battleship 1x4
                        bat_num += 1
                    elif data[i+2][j] == 'B':  # cruiser 1x3
                        crui_num += 1
                elif data[i+1][j] == 'B':  # destroyer 1x2
                    des_num += 1
            elif data[i][j] == 'L':  # horizontal destroyer 1x2 or cruiser 1x3 or battleship 1x4
                if data[i][j+1] == 'M':  # cruiser 1x3 or battleship 1x4
                    if data[i][j+2] == 'M':  # battleship 1x4
                        bat_num += 1
                    elif data[i][j+2] == 'R':  # cruiser 1x3
                        crui_num += 1
                elif data[i][j+1] == 'R':  # destroyer 1x2
                    des_num += 1
    return {"B": bat_num, "C": crui_num, "D": des_num, "S": sub_num}


def match_ships(data):  # checked
    """ check if the current board falsify the my_ship constraint"""
    ships = count_ships(data)
    if ships["S"] == ship_const["S"] and ship_const["D"] == ship_const["D"] and ships["C"] == ship_const["C"] and ships["B"] == ship_const["B"]:
        # the my_ship number match
        return True
    else:
        return False


# def check_ships(data):  # checked
#     """ check if the current board falsify the my_ship constraint"""
#     ships = count_ships(data)
#     if ships["S"] <= my_ship["S"] and ships["D"] <= my_ship["D"] and ships["C"] <= my_ship["C"] and ships["B"] <= my_ship["B"]:
#         # the my_ship number match
#         return True
#     else:
#         return False


def create_domain(data, var):
    """
    add all possible move (domain) for each ship & remove the assigned variables
    should have checked that there is bat ship num >= 1 before calling this function
    WARNING: cannot call it anywhere else except in read_file, will cause duplicate domain
    """
    domain = []
    for i in range(dim):
        for j in range(dim):
            if var == 4:
                if i+3 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0' and data[i+2][j] == '0' and data[i+3][j] == '0':
                    # there is space to place a vertical battleship
                    domain.append([[i, j], [i+1, j], [i+2, j], [i+3, j]])
                if j+3 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0' and data[i][j+2] == '0' and data[i][j+3] == '0':
                    # there is space to place a horizontal battleship
                    domain.append([[i, j], [i, j+1], [i, j+2], [i, j+3]])
            elif var == 3:
                if i+2 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0' and data[i+2][j] == '0':
                    # there is space to place a vertical cruiser
                    domain.append([[i, j], [i+1, j], [i+2, j]])
                if j+2 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0' and data[i][j+2] == '0':
                    # there is space to place a horizontal cruiser
                    domain.append([[i, j], [i, j+1], [i, j+2]])
            elif var == 2:
                if i+1 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0':
                    # there is space to place a vertical destroyer
                    domain.append([[i, j], [i+1, j]])
                if j+1 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0':
                    # there is space to place a horizontal destroyer
                    domain.append([[i, j], [i, j+1]])
            elif var == 1:
                if data[i][j] == '0':
                    # there is space to place a submarine
                    domain.append([[i, j]])
    return domain


def check_orientation(positions):  # checked
    """ determine the orientation of given positions """
    old_y, old_x = positions[0][0], positions[0][1]
    new_y, new_x = positions[1][0], positions[1][1]
    if new_y > old_y and new_x == old_x:  # vertical
        return 1
    elif new_y == old_y and new_x > old_x:  # horizontal
        return 0


def insert_into_board(data, ship_type, pos):  # checked
    """ set the given variable into given position """
    new_data = deepcopy(data)
    var = ship_type
    if len(pos) > 1:
        ori = check_orientation(pos)
    # pos = all of the squares need to be filled up with 'T', 'B', 'L', 'R', 'M' or 'S'
    if var == 4:  # a battleship, 1x4
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            new_data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            new_data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            new_data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            new_data[y][x] = 'B'
    elif var == 3:  # cruiser, 1x3
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            new_data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            new_data[y][x] = 'B'
    elif var == 2:  # destroyer, 1x2
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            new_data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            new_data[y][x] = 'B'
    elif var == 1:  # submarine, 1x1
        y, x = pos[0][0], pos[0][1]
        new_data[y][x] = 'S'

    # filled col or row with W where needed
    update_const(new_data)
    # surround this ship with W
    update_data(new_data)

    return new_data


def update_domain(state, var, pos):  # checked
    """ 
    remove the assigned pos from var 
    eliminate the positions of Y that is overlap or next to x after assign x to X 
    eliminate the positions of Y that violate the row or col constraints
    """
    domain = state.domain
    data = state.data

    # eliminate overlap or next to
    s = surround(pos)
    for x in domain:
        if x == var:
            # origin = deepcopy(domain[x])
            # domain[x].remove(pos)
            # if len(origin) == len(domain[x]):
            #    print("fail to remove from domain")
            continue
        else:  # for Y
            # print(x)
            y = 0
            while y < len(domain[x]):
                # print(y)
                for k in domain[x][y]:
                    if k in s:
                        # print(domain[x])
                        l = domain[x].pop(y)
                        # print(domain[x])
                        y -= 1
                        break
                y += 1

    # eliminate violate row or col constraint
    for x in domain:
        y = 0
        # print(x, domain[x])
        while y < len(domain[x]):
            for pos in domain[x][y]:
                i, j = pos[0], pos[1]
                if data[i][j] != '0':
                    l = domain[x].pop(y)
                    y -= 1
                    break
            y += 1


def find_surround(pos):
    """ find every square around the given square and return in a set """
    s = []
    y, x = pos[0], pos[1]
    if y != 0:
        s.append([y-1, x])
        if x != 0:
            s.append([y-1, x-1])
        if x != dim-1:
            s.append([y-1, x+1])
    s.append([y, x])
    if x != 0:
        s.append([y, x-1])
    if x != dim-1:
        s.append([y, x+1])
    if y != dim-1:
        s.append([y+1, x])
        if x != 0:
            s.append([y+1, x-1])
        if x != dim-1:
            s.append([y+1, x+1])
    return s


def surround(pos):
    """
    find every square around the given square and return
    """

    s = []
    for i in range(len(pos)):
        l = find_surround(pos[i])
        for j in range(len(l)):
            if l[j] not in s:
                s.append(l[j])
    return s


def check_overlapping(data, pos):  # checked
    """ check if there's ship overlap with or next to curr ship, """

    # # overlapping
    # for i in range(len(pos)):
    #     y, x = pos[i][0], pos[i][1]
    #     if data[y][x] != ship:          # TODO ?
    #         return False

    # next to
    s = []
    # unite all surrounding squares in a set
    # should cover every square in this solid area
    s = surround(pos)
    # remove the squares filled by this ship
    for i in range(len(pos)):
        if pos[i] in s:
            s.remove(pos[i])

    for x in s:
        y, x = x[0], x[1]
        if data[y][x] != 'W' and data[y][x] != '0':
            return False
    # does not overlap
    return True


##################################### BackTrack, FC, GAC algorithms ########################

def check_consistent(data, pos):  # checked
    """
    check if all constraints that is related to var are consistent
    return True if all constraints are satisfied
    return False if there's one constraints that is violated
    """
    res = []

    # sub
    if len(pos) == 1:  # S
        if match_row_const(data, pos[0][0]):
            # filled the rest of the col with W
            update_const(data)
        res.append(check_row_const(data, pos[0][1]))
        if match_col_const(data, pos[0][1]):
            # filled the rest of the col with W
            update_const(data)
        res.append(check_col_const(data, pos[0][0]))

    # for other ships with len > 1
    else:
        # check if this variable and its assigned position violate col constraints
        if check_orientation(pos) == 0:  # horizontal
            for i in range(len(pos)):  # need to check multi cols
                if match_col_const(data, pos[i][1]):
                    # filled the rest of the col with W
                    update_const(data)
                res.append(check_col_const(data, pos[i][1]))
        else:  # vertical
            if match_col_const(data, pos[0][1]):
                update_const(data)
            res.append(check_col_const(data, pos[0][1]))

        # check if violate row constraints
        if check_orientation(pos) == 0:  # horizontal
            res.append(check_row_const(data, pos[0][0]))  # only check 1 row
        else:  # vertical
            for i in range(len(pos)):
                if match_row_const(data, pos[i][0]):
                    # filled the rest of the col with W
                    update_const(data)
                res.append(check_row_const(data, pos[i][0]))

    # check if overlap or next to
    res.append(check_overlapping(data, pos))
    print(res)
    return all(res)


def all_assigned(state):  # checked
    """ return True if every my_ship is assigned with a position """
    if match_ships(state.data):
        return True
    return False


# def clear_domain(state, var):
#     """ clear the domain of the variable """
#     for pos in state.domain[var]:
#         state.domain[var].remove(pos)


def check_r_const(data, row_num, num_squares):
    row = data[row_num]
    total = 0
    for i in range(len(row)):
        if row[i] != '0' and row[i] != 'W':
            total += 1
    total += num_squares
    if total <= row_const[row_num]:
        return True
    else:
        return False


def make_r_const(data, new_var_index, pos):  # ?
    """ 
    row constraint
    input should be a domain of all possible positions
    return only the domain consistent
    """
    if not pos:  # pos is None
        return None
    res = []
    var = variables[new_var_index]
    if var == 1:  # S
        for i in range(len(pos)):
            if check_r_const(data, pos[i][0][0], 1):
                res.append(pos[i])
    elif var == 2:  # D
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 0:  # horizontal
                if check_r_const(data, pos[i][0][0], 2):  # only check 1 row
                    res.append(pos[i])
            else:  # vertical
                if all([check_r_const(data, pos[i][j][0], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])
    elif var == 3:  # C
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 0:  # horizontal
                if check_r_const(data, pos[i][0][0], 3):  # only check 1 row
                    res.append(pos[i])
            else:  # vertical
                if all([check_r_const(data, pos[i][j][0], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])
    elif var == 4:  # D
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 0:  # horizontal
                if check_r_const(data, pos[i][0][0], 4):  # only check 1 row
                    res.append(pos[i])
            else:  # vertical
                if all([check_r_const(data, pos[i][j][0], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])

    if len(res) == 0:
        return None
    return res


def check_c_const(data, col_num, num_squares):
    col = [data[i][col_num] for i in range(len(data))]
    total = 0
    for i in range(len(col)):
        if col[i] != '0' and col[i] != 'W':
            total += 1
    total += num_squares
    if total <= col_const[col_num]:
        return True
    else:
        return False


def make_c_const(data, new_var_index, pos):  # checked
    """ 
    col constraint
    input should be a domain of all possible positions
    return only the domain consistent
    """
    if not pos:  # pos is None
        return None

    res = []
    var = variables[new_var_index]
    if var == 1:  # S
        for i in range(len(pos)):
            if check_c_const(data, pos[i][0][1], 1):
                res.append(pos[i])
    elif var == 2:  # D
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 1:  # vertical
                if check_c_const(data, pos[i][0][1], 2):  # only check 1 row
                    res.append(pos[i])
            else:  # horizontal
                if all([check_c_const(data, pos[i][j][1], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])
    elif var == 3:  # C
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 1:  # vertical
                if check_c_const(data, pos[i][0][1], 3):  # only check 1 row
                    res.append(pos[i])
            else:  # horizontal
                if all([check_c_const(data, pos[i][j][1], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])
    elif var == 4:  # D
        for i in range(len(pos)):
            # for one possible position set
            if check_orientation(pos[i]) == 1:  # vertical
                if check_c_const(data, pos[i][0][1], 4):  # only check 1 row
                    res.append(pos[i])
            else:  # horizontal
                if all([check_c_const(data, pos[i][j][1], 1) for j in range(len(pos[i]))]):
                    res.append(pos[i])

    if len(res) == 0:
        return None
    return res


def make_non_overlapping_const(state, assign_index, pos):  # checked
    """ """
    if not pos:  # pos is None
        return None

    res = []
    data = state.data
    assign_pos = state.assigned[assign_index]
    for i in range(len(pos)):
        # for each position set
        if check_overlapping(data, pos[i]) and not is_subset(assign_pos, pos[i]):
            res.append(pos[i])
    if len(res) == 0:
        return None
    return res


def is_subset(assign_pos, pos):
    """ """
    s = surround(assign_pos)
    for i in range(len(pos)):
        # for each square
        if pos[i] in s:
            # overlap or next to
            return True
    # does not overlap
    return False


def MRV(ships):  # checked
    """" return the name of the unassigned variable with the least CurDom"""
    if len(ships) > 0:
        return ships.pop()
    else:
        print("nothing to pop")
        return None


def FC(state, ships, arrangements, current_board):
    """ Forward checking"""

    if all_assigned(state):
        return (True, current_board)
    if (len(ships)) > len(arrangements):
        return (False, current_board)
    if len(ships) == 0:
        print(print_data(state))

    for row in current_board:
        print(row)
        print("\n")

    var = ships[len(ships)-1]
    next_arrangements = create_domain(state.data, var)

    next_arrangements = make_r_const(
        state.data, len(ships)-1, next_arrangements)
    print(next_arrangements)
    next_arrangements = make_c_const(
        state.data, len(ships)-1, next_arrangements)
    print(next_arrangements)
    next_arrangements = make_non_overlapping_const(
        state, len(ships), next_arrangements)
    print(next_arrangements)

    if not next_arrangements:
        return (False, current_board)

    for arrangement in next_arrangements:
        current_board = insert_into_board(state.data, ships, arrangement)
        assigned = deepcopy(state.assigned)
        assigned[len(ships)-1] = arrangement
        next_state = State(data=current_board, assigned=assigned, parent=state)
        next_state.assigned[len(ships)-1] = arrangement
        preprocessing(init)
        result, board = FC(next_state, ships[0: len(
            ships)-1], next_arrangements, current_board)

        if result:
            return (True, board)

    return (False, board)


# def FC1(state, ship_type, index, domain):

#     if all_assigned(state):
#         return state

#     # ships = state.ships
#     # var = MRV(ships)
#     # the index of this newly pop var is the last index on original ships (= len)
#     # index = len(ships)

#     preprocessing(state)
#     print(print_data(state))
#     # domain = create_domain(state, var)
#     print(domain)
#     assigned = state.assigned

#     for pos in domain:

#         # assign var to pos
#         assigned[index] = pos

#         # place var on pos
#         new_data = deepcopy(state.data)
#         insert_into_board(new_data, ship_type, pos)
#         new_ships = deepcopy(state.ships)
#         new_assigned = deepcopy(assigned)

#         # child state
#         child = State(ships=new_ships, assigned=new_assigned,
#                       data=new_data, parent=state)
#         preprocessing(child)
#         print(print_data(child))

#         DWO = False
#         # check if any other variable result in DWO if var -> pos
#         i = index-1  # there are index-1 num of other var need to be assigned
#         while i >= 0:
#             next_arrangements = create_domain(child, variables[i])
#             print(next_arrangements)
#             next_arrangements = make_r_const(child, i, next_arrangements)
#             print(next_arrangements)
#             next_arrangements = make_c_const(child, i, next_arrangements)
#             print(next_arrangements)
#             next_arrangements = make_non_overlapping_const(
#                 child, index, next_arrangements)
#             print(next_arrangements)
#             if not next_arrangements:
#                 DWO = True
#                 break
#             i -= 1

#         if not DWO:
#             return FC(child, variables[index-1], index-1, next_arrangements)
#         else:
#             continue


def is_empty(domain):
    for positions in domain:
        for pos in positions:
            if len(pos) != 0:
                return False
    return True
######################################## read, output file ###############################


def print_data(state):  # check
    result = ""
    data = state.data
    length = len(data[0])
    for i in range(length):
        for j in range(length):
            result += str(data[i][j])
        result += "\n"
    return result


# def print_domain(state):  # check
#     result = ""
#     domain = state.domain
#     for x in state.domain:
#         result += x
#         result += ": "
#         for j in range(len(domain[x])):
#             result += str(domain[x][j])
#         result += "\n"
#     return result


def to_list(string):
    res = [int(string[i]) for i in range(len(string)-1)]
    return res


def read_file(filename):
    """ read the state from input file"""
    file = open(filename, "r")

    row_line = file.readline()
    global row_const
    row_const = to_list(row_line)
    # print(row_const)

    col_line = file.readline()
    global col_const
    col_const = to_list(col_line)
    # print(col_const)

    ships_line = file.readline()
    ships_const = to_list(ships_line)

    my_ship = []
    if len(ships_const) == 1:
        ship_const["S"] = ships_const[0]
        for i in range(ships_const[0]):
            my_ship.append(1)
    if len(ships_const) == 2:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
        for i in range(ships_const[1]):
            my_ship.append(1)
        for i in range(ships_const[0]):
            my_ship.append(2)
    if len(ships_const) == 3:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
        ship_const["C"] = ships_const[2]
        for i in range(ships_const[0]):
            my_ship.append(1)
        for i in range(ships_const[1]):
            my_ship.append(2)
        for i in range(ships_const[2]):
            my_ship.append(3)
    if len(ships_const) == 4:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
        ship_const["C"] = ships_const[2]
        ship_const["B"] = ships_const[3]
        for i in range(ships_const[0]):
            my_ship.append(1)
        for i in range(ships_const[1]):
            my_ship.append(2)
        for i in range(ships_const[2]):
            my_ship.append(3)
        for i in range(ships_const[3]):
            my_ship.append(4)
    print(my_ship)

    global dim
    dim = len(row_line)-1

    length = dim
    # print(length)

    new_data = [["0" for _ in range(length)] for _ in range(length)]
    for i in range(length):
        row = file.readline()
        for j in range(length):
            new_data[i][j] = str(row[j])

    # ships dict to count the num of each ship
    # ships = count_ships(new_data)
    for i in range(dim):
        for j in range(dim):
            if new_data[i][j] == 'S':
                # exists a sub on board
                my_ship.remove(1)
            elif new_data[i][j] == 'D':
                my_ship.remove(2)
            elif new_data[i][j] == 'C':
                my_ship.remove(3)
            elif new_data[i][j] == 'B':
                my_ship.remove(4)
    # print(my_ship)
    # domain (list of possible locations) of each ship
    assigned = [[] for _ in range(len(my_ship))]

    global variables
    variables = deepcopy(my_ship)

    res = State(ships=my_ship, assigned=assigned, data=new_data)

    # preprocessing(res)

    # create domains for each variable based on data
    # domains(res)
    # print("after eliminate domain: \n", print_domain(res))

    file.close()
    return res


def output_file(filename, state):
    """ print FC output into file """

    file = open(filename, "w")

    final = FC(state)
    file.write(print_data(final))
    file.close()


if __name__ == '__main__':

    # init = read_file(sys.argv[1])
    # output_file(sys.argv[2], init)

    init = read_file("input1.txt")
    print(print_data(init))
    # print(MRV(init.ships))
    preprocessing(init)
    ship_type = MRV(init.ships)
    arrangements = create_domain(init.data, ship_type)
    # board = insert_into_board(init.data, ship_type, arrangements[0])
    result, final = FC(init, init.ships, arrangements, init.data)
    # preprocessing(init)
    print("final: \n", print_data(final))

    # FC(init)
    # print(print_data(init))