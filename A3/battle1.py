from collections import defaultdict, deque
from copy import deepcopy
import sys

row_const = []
col_const = []
ship_const = {"S": 0, "D": 0, "C": 0, "B": 0}
dim = 0


class State:
    """A state is a table of all the tiles with given initial locations.
    """

    def __init__(self, ships=None, domain=None, data=None, parent=None):
        self.ships = ships
        self.domain = domain
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

    # surround ship_const with W
    update_data(state.data)
    # print("after update_data: \n", print_data(state))

    # add W based on row & col constraints
    update_const(state.data)
    # print("after update_const: \n", print_data(state))


def update_data(data):  # checked
    """
    update the grid by surround ship_const with W
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
    update the board based on row, col, ship_const const
    """
    if match_ships(data):
        # ship_const number matched, filled the rest of the board with W
        # print("ship_const checked")
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
    """ check if the current board falsify the ship_const constraint"""
    ships = count_ships(data)
    if ships["S"] == ship_const["S"] and ships["D"] == ship_const["D"] and ships["C"] == ship_const["C"] and ships["B"] == ship_const["B"]:
        # the ship_const number match
        return True
    else:
        return False


def check_ships(data):  # checked
    """ check if the current board falsify the ship_const constraint"""
    ships = count_ships(data)
    if ships["S"] <= ship_const["S"] and ships["D"] <= ship_const["D"] and ships["C"] <= ship_const["C"] and ships["B"] <= ship_const["B"]:
        # the ship_const number match
        return True
    else:
        return False


def domains(state):  # checked
    """
    add all possible move (domain) for each ship & remove the assigned variables
    should have checked that there is bat ship num >= 1 before calling this function
    WARNING: cannot call it anywhere else except in read_file, will cause duplicate domain
    """
    data = state.data
    domain = state.domain
    for i in range(dim):
        for j in range(dim):
            if i+3 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0' and data[i+2][j] == '0' and data[i+3][j] == '0':
                # there is space to place a vertical battleship
                domain["B"].append([[i, j], [i+1, j], [i+2, j], [i+3, j]])
            if j+3 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0' and data[i][j+2] == '0' and data[i][j+3] == '0':
                # there is space to place a horizontal battleship
                domain["B"].append([[i, j], [i, j+1], [i, j+2], [i, j+3]])
            if i+2 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0' and data[i+2][j] == '0':
                # there is space to place a vertical cruiser
                domain["C"].append([[i, j], [i+1, j], [i+2, j]])
            if j+2 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0' and data[i][j+2] == '0':
                # there is space to place a horizontal cruiser
                domain["C"].append([[i, j], [i, j+1], [i, j+2]])
            if i+1 <= dim-1 and data[i][j] == '0' and data[i+1][j] == '0':
                # there is space to place a vertical destroyer
                domain["D"].append([[i, j], [i+1, j]])
            if j+1 <= dim-1 and data[i][j] == '0' and data[i][j+1] == '0':
                # there is space to place a horizontal destroyer
                domain["D"].append([[i, j], [i, j+1]])
            if data[i][j] == '0':
                # there is space to place a submarine
                domain["S"].append([[i, j]])


def check_orientation(positions):  # checked
    """ determine the orientation of given positions """
    old_y, old_x = positions[0][0], positions[0][1]
    new_y, new_x = positions[1][0], positions[1][1]
    if new_y > old_y and new_x == old_x:  # vertical
        return 1
    elif new_y == old_y and new_x > old_x:  # horizontal
        return 0


def insert_into_board(data, var, pos):  # checked
    """ set the given variable into given position """
    if len(pos) > 1:
        ori = check_orientation(pos)
    # pos = all of the squares need to be filled up with 'T', 'B', 'L', 'R', 'M' or 'S'
    if var == 'B':  # a battleship, 1x4
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'M'
            y, x = pos[3][0], pos[3][1]
            data[y][x] = 'B'
    elif var == 'C':  # cruiser, 1x3
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'M'
            y, x = pos[2][0], pos[2][1]
            data[y][x] = 'B'
    elif var == 'D':  # destroyer, 1x2
        if ori == 0:  # horizontal
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'L'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'R'
        else:  # vertical
            y, x = pos[0][0], pos[0][1]
            data[y][x] = 'T'
            y, x = pos[1][0], pos[1][1]
            data[y][x] = 'B'
    elif var == 'S':  # submarine, 1x1
        y, x = pos[0][0], pos[0][1]
        data[y][x] = 'S'
    update_const(data)
    update_data(data)


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
            origin = deepcopy(domain[x])
            domain[x].remove(pos)
            if len(origin) == len(domain[x]):
                print("fail to remove from domain")
        else:  # for Y
            y = 0
            while y < len(domain[x]):
                for k in domain[x][y]:
                    if k in s:
                        l = domain[x].pop(y)
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
        if match_row_const(data, pos[0][1]):
            # filled the rest of the col with W
            update_const(data)
        res.append(check_row_const(data, pos[0][1]))
        if match_col_const(data, pos[0][0]):
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
    """ return True if every ship_const is assigned with a position """
    if match_ships(state.data):
        return True
    return False


def clear_domain(state, var):
    """ clear the domain of the variable """
    for pos in state.domain[var]:
        state.domain[var].remove(pos)


def MRV(state):  # checked
    """" return the name of the unassigned variable with the least CurDom"""
    min = float('inf')
    min_var = ""
    print(print_domain(state))
    for x in state.domain:
        # this variable is not assigned and has least domain
        if state.ships[x] < ship_const[x]:
            if len(state.domain[x]) < min:
                min = len(state.domain[x])
                min_var = str(x)         # update the least domain
            else:
                continue
        else:  # every var for this kind of ship has been assigned, clear its domain
            clear_domain(state, x)

    if min_var == "":
        # no ships satisfy the requirement
        print("problem with MRV")
        print("ships: ", state.ships)
        print("domains: ", print_domain(state))
        exit()
    return min_var

# def GAC1(state):
#     """ forward checking """

#     if all_assigned(state):
#         print(print_data(state))
#         solution = state
#         exit()

#     # filled necessary squares with W
#     # preprocessing(state)

#     # pick an unassigned variable that has the least domain
#     var = MRV(state)

#     # var has to be battleship if num of bat != 0
#     i = 0
#     total = ship_const[var]
#     while i < total:
#         for val in state.domain[var]:
#             stored_domain = deepcopy(state.domain)

#             # assign this val to var (place this var ship in val pos)
#             new_data = deepcopy(state.data)
#             # new board with the ship placed
#             insert_into_board(new_data, var, val)
#             new_domain = deepcopy(state.domain)
#             child = State(parent=state, data=new_data,
#                           domain=new_domain)
#             update_domain(child, var, val)
#             state.ship[var] += 1

#             # add all relevant constraints C into GACQueue
#             # GACQueue.append()

#             # if there's DWO in any Y, this X is pruned
#             if GAC_Enforce(child, var) != 'DWO':
#                 GAC(child)

#             state.domain = stored_domain
#         i += 1
#     # assigned = False  # undo since we have tried all of V's value
#     return


# def GAC_Enforce(state):
#     """ we have assigned a variable, now we need to assign the rest and see if any of them encounter DWO """
#     domain = state.domain
#     # const is a constraint with all its variables already assigned, except for variable x

#     for pos in domain[var]:
#         new_data = deepcopy(state.data)
#         insert_into_board(new_data, var, pos)

#         # for every C, if making x = val violate C
#         Y = deepcopy(state.domain)
#         Y.remove(var)
#         for y in Y:
#             if not check_consistent(new_data, pos):
#         if not check_consistent(new_data, pos):
#             # remove d from CurDom(x)
#             domain[var].remove(pos)
#         else:  # consistent, keep this pos
#             continue
#     if len(domain) == 0:
#         return 'DWO'

def GAC(state):
    """ """
    domain = state.domain

    if all_assigned(state):  # all ships assigned, exit with curr state
        return state

    var = MRV(state)

    # not exit, var should be a ship
    print(state.ships)
    state.ships[var] += 1
    print(state.ships)
    for pos in domain[var]:
        print(var, pos)
        new_data = deepcopy(state.data)
        print(print_data(state))
        # new board with the ship placed
        insert_into_board(new_data, var, pos)

        new_domain = deepcopy(state.domain)
        new_ships = deepcopy(state.ships)
        child = State(parent=state, data=new_data,
                      domain=new_domain, ships=new_ships)
        update_domain(child, var, pos)

        print("inserted: \n")
        print(print_data(child))
        print(print_domain(child))

        # if assigning this variable with pos violate one of the constraints, (already removed) try next pos
        if not check_consistent(child.data, pos):
            continue
        else:  # not violate, assign other variables
            res = GACEnforce(child)
            # child returns DWO
            if res == "DWO":
                continue
            else:
                return res
        # i += 1
    # shouldn't reach here
    # if so, there's no valid pos to place this ship
    print("ERROR")
    exit()


def GACEnforce(state):
    """ """
    domain = state.domain

    for x in state.domain:
        if state.ships[x] != ship_const[x] and len(domain[x]) == 0:
            return "DWO"

    if all_assigned(state):  # all ships assigned, exit with curr state
        return state

    # for an unassigned variable
    var = MRV(state)

    # not exit, var should be a ship
    print(state.ships)
    state.ships[var] += 1
    print(state.ships)
    for pos in domain[var]:
        print(var, pos)
        # while i < total:
        # grab another variable

        # var = MRV(state)
        # state.ships[var] += 1
        # if ship_const[var] == state.ships[var]:
        #     # no other this kind of ship need to be placed, go to the next kind (ie Cruiser)

        # assign this var to pos (place this var ship in pos)
        new_data = deepcopy(state.data)
        print(print_data(state))
        # new board with the ship placed
        insert_into_board(new_data, var, pos)

        new_domain = deepcopy(state.domain)
        new_ships = deepcopy(state.ships)
        child = State(parent=state, data=new_data,
                      domain=new_domain, ships=new_ships)
        update_domain(child, var, pos)

        print("inserted: \n")
        print(print_data(child))
        print(print_domain(child))

        # if assigning this variable with pos violate one of the constraints, (already removed) try next pos
        if not check_consistent(child.data, pos):
            domain[var].remove(pos)

            print(var, child.ships)
            print(print_domain(child))
            print(child.ships[var] != ship_const[var],
                  len(child.domain[var]) == 0)

            # if there's no more other choice for var
            # if child.ships[var] != ship_const[var] and len(child.domain[var]) == 0:
            #     return "DWO"
            # else:
            #     continue
            # if there's other choice for var, assign other val
            print(child.domain[var])
            if len(child.domain[var]) > 0:
                print("next")
                continue
            else:
                return "DWO"
        # else:  # not violate, assign other variables
        res = GACEnforce(child)
        # child returns DWO
        print(res)
        if res == "DWO":
            # TODO: need to figure out if DWO can be solve in this stage
            print(var, state.domain[var])
            if len(state.domain[var]) > 0:
                print("next")
                continue
            else:
                print("DWO")
                return "DWO"
        else:
            return res
        # i += 1
    # shouldn't reach here
    # if so, there's no valid pos to place this ship
    print("ERROR")
    exit()


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


def print_domain(state):  # check
    result = ""
    domain = state.domain
    for x in state.domain:
        result += x
        result += ": "
        for j in range(len(domain[x])):
            result += str(domain[x][j])
        result += "\n"
    return result


def to_list(string):
    res = [int(string[i]) for i in range(len(string)-1)]
    return res


def read_file(filename):
    """ read the state from input file"""
    file = open(filename, "r")

    row_line = file.readline()
    global row_const
    row_const = to_list(row_line)
    print(row_const)

    col_line = file.readline()
    global col_const
    col_const = to_list(col_line)
    print(col_const)

    ships_line = file.readline()
    ships_const = to_list(ships_line)
    if len(ships_const) == 1:
        ship_const["S"] = ships_const[0]
    if len(ships_const) == 2:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
    if len(ships_const) == 3:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
        ship_const["C"] = ships_const[2]
    if len(ships_const) == 4:
        ship_const["S"] = ships_const[0]
        ship_const["D"] = ships_const[1]
        ship_const["C"] = ships_const[2]
        ship_const["B"] = ships_const[3]
    # print(ship_const)

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
    ships = count_ships(new_data)

    # domain (list of possible locations) of each ship
    domain = defaultdict(list)
    domain["B"] = []
    domain["C"] = []
    domain["D"] = []
    domain["S"] = []

    # global assigned
    # assigned = [[False for _ in range(length)] for _ in range(length)]

    res = State(ships=ships, domain=domain, data=new_data)

    preprocessing(res)
    print("Prep")
    print(preprocessing(res))
    # create domains for each variable based on data
    domains(res)
    # print("after eliminate domain: \n", print_domain(res))

    file.close()
    return res


def output_file(filename, state):
    """ print FC output into file """

    file = open(filename, "w")

    final = GAC(state)
    file.write(print_data(final))
    file.close()


if __name__ == '__main__':

    # init = read_file(sys.argv[1])
    # output_file(sys.argv[2], init)

    init = read_file("input1.txt")
    print(print_data(init))
    print("Pre")
    print(preprocessing(init))
    final = GAC(init)
    print(print_data(final))

    # preprocessing(init)
    # print(MRV(init))
    # print("final: \n", print_data(init))

    # FC(init)
    # print(print_data(init))