# Import necessary libraries
import sys
import copy
import numpy as np
import string
from itertools import chain
from constraint import *

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

# ------------- BACKTRACKING WITH MRV ----------------
class BacktrackingBattleshipSolver(Solver):

    def __init__(self, neighbourLookupTable, forwardcheck=True):
        """
        @param forwardcheck: If false forward checking will not be requested
                             to constraints while looking for solutions
                             (default is true)
        @type  forwardcheck: bool
        """

        self._forwardcheck = forwardcheck
        self._neighbourLookupTable = neighbourLookupTable
    
    def isNeighbourOfAssignedVar(self, variable, assignedVariables):
        for neighbour in self._neighbourLookupTable[variable]:
            if neighbour in assignedVariables:
                return 0
        return 1
        
    def getSolutionIter(self, domains, constraints, vconstraints):
        forwardcheck = self._forwardcheck
        assignments = {}

        queue = []

        while True:
            assignedVariables = []
            for var, value in assignments.items():
                if value != 7:
                    assignedVariables.append(var)

            # Mix the Degree and Minimum Remaing Values (MRV) heuristics
            lst = [
                (
                    len(domains[variable]),
                    self.isNeighbourOfAssignedVar(variable, assignedVariables),
                    -len(vconstraints[variable]),
                    variable,
                )
                for variable in domains
            ]
            lst.sort()
            for item in lst:
                if item[-1] not in assignments:
                    # Found unassigned variable
                    variable = item[-1]
                    values = domains[variable][:]
                    if forwardcheck:
                        pushdomains = [
                            domains[x]
                            for x in domains
                            if x not in assignments and x != variable
                        ]
                    else:
                        pushdomains = None
                    break
            else:
                # No unassigned variables. We've got a solution. Go back
                # to last variable, if there's one.
                yield assignments.copy()
                if not queue:
                    return
                variable, values, pushdomains = queue.pop()
                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            while True:
                # We have a variable. Do we have any values left?
                if not values:
                    # No. Go back to last variable, if there's one.
                    del assignments[variable]
                    while queue:
                        variable, values, pushdomains = queue.pop()
                        if pushdomains:
                            for domain in pushdomains:
                                domain.popState()
                        if values:
                            break
                        del assignments[variable]
                    else:
                        return

                # Got a value. Check it.
                assignments[variable] = values.pop()

                if pushdomains:
                    for domain in pushdomains:
                        domain.pushState()

                for constraint, variables in vconstraints[variable]:
                    if not constraint(variables, domains, assignments, pushdomains):
                        # Value is not good.
                        break
                else:
                    break

                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            # Push state before looking for next variable.
            queue.append((variable, values, pushdomains))

        raise RuntimeError("Can't happen")

    def getSolution(self, domains, constraints, vconstraints):
        iter = self.getSolutionIter(domains, constraints, vconstraints)
        try:
            return next(iter)
        except StopIteration:
            return None

    def getSolutions(self, domains, constraints, vconstraints):
        return list(self.getSolutionIter(domains, constraints, vconstraints))

def change_variables(config):
    for i in range(n):
        for j in range(n):
            if config[i][j] == '0':
                config[i][j] = 0
            elif config[i][j] == 'S':
                config[i][j] = 6
            elif config[i][j] == 'W':
                config[i][j] = 7
            elif config[i][j] == 'L':
                config[i][j] = 4
            elif config[i][j] == 'R':
                config[i][j] = 2
            elif config[i][j] == 'U':
                config[i][j] = 1
            elif config[i][j] == 'B':
                config[i][j] = 3
            elif config[i][j] == 'M':
                config[i][j] = 5
    return config

numerical_board = change_variables(board)

ships_dict = {
    1: num_submarines,
    2: num_destroyers,
    3: num_cruisers,
    4: num_battleships,
}

top = 1
right = 2
bottom = 3
left = 4
middle = 5
submarine = 6
water = 7

ship_parts = [
    top,
    right,
    bottom,
    left,
    middle,
    submarine,
]

print(numerical_board)
print(row_line, col_line)

rownames = list(range(n))
colnames = [*string.ascii_letters[0:n]]

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(j+str(i))
    rows.append(row)

cols = []
for j in colnames:
    col = []
    col_declarations.append(col)
    for i in rownames:
        col.append(j+str(i))

flat_vars = list(chain.from_iterable(cols))

boxes = []

for i in range(n-2):
    for j in range(n-2):
        box = []
        for rowi in range(3):
            for coli in range(3):
                box.append(rows[i+rowi][j+coli])
        boxes.append(box)

border_boxes_left = []
for i in range(n-2):
    box = []
    for j in range(3):
        box.append(rows[i+j][0])
        box.append(rows[i+j][1])
    border_boxes_left.append(box)

border_boxes_right = []
for i in range(n-2):
    box = []
    for j in range(3):
        box.append(rows[i+j][n-2])
        box.append(rows[i+j][n-1])
    border_boxes_right.append(box)

border_boxes_top = []
for i in range(n-2):
    box = []
    for j in range(3):
        box.append(rows[0][i+j])
        box.append(rows[1][i+j])
    border_boxes_top.append(box)

border_boxes_bottom = []
for i in range(n-2):
    box = []
    for j in range(3):
        box.append(rows[n-2][i+j])
        box.append(rows[n-1][i+j])
    border_boxes_bottom.append(box)

corner_top_left_box = [
    rows[0][0],
    rows[0][1],
    rows[1][0],
    rows[1][1],
]

corner_top_right_box = [
    rows[0][len(cols)-2],
    rows[0][len(cols)-1],
    rows[1][len(cols)-2],
    rows[1][len(cols)-1],
]

corner_bottom_left_box = [
    rows[len(rows)-2][0],
    rows[len(rows)-2][1],
    rows[len(rows)-1][0],
    rows[len(rows)-1][1],
]

corner_bottom_right_box = [
    rows[len(rows)-2][len(cols)-2],
    rows[len(rows)-2][len(cols)-1],
    rows[len(rows)-1][len(cols)-2],
    rows[len(rows)-1][len(cols)-1],
]

# ----- Lookup table for bimaru solver -----
neighbourLookupTable = {}
for box in boxes:
    neighbourLookupTable[box[4]] = [*box[0:4], *box[5:]]

# borders
for box in border_boxes_top:
    neighbourLookupTable[box[2]] = [*box[0:2], *box[3:]]

for box in border_boxes_right:
    neighbourLookupTable[box[3]] = [*box[0:3], *box[4:]]

for box in border_boxes_bottom:
    neighbourLookupTable[box[3]] = [*box[0:3], *box[4:]]

for box in border_boxes_left:
    neighbourLookupTable[box[2]] = [*box[0:2], *box[3:]]

# corners
neighbourLookupTable[corner_top_left_box[0]] = [*corner_top_left_box[1:]]
neighbourLookupTable[corner_top_right_box[1]] = [*corner_top_right_box[0:1], *corner_top_right_box[2:]]
neighbourLookupTable[corner_bottom_left_box[2]] = [*corner_bottom_left_box[0:2], *corner_bottom_left_box[3:]]
neighbourLookupTable[corner_bottom_right_box[3]] = [*corner_bottom_right_box[0:3]]

# ------------------------------------------------------------------------------
# formulate bimaru as CSP
# ------------------------------------------------------------------------------
bimaru = csp.Problem(BacktrackingBattleshipSolver(neighbourLookupTable))

for i, row in enumerate(rows):
    for j, col in enumerate(row):
        bimaru.addVariable(col,
                           list(range(1, 8)) if board[i][j] == 0 else [board[i][j]])


def getNumberOfPartsConstraint(exactNumberOfParts, rowIndex=-1, colIndex=-1):
    def constraint(*args, assignments=None, _unassigned=csp.Unassigned):
        numberOfParts = 0
        anyUnassigned = False

        for value in args:
            if (value == _unassigned):
                anyUnassigned = True
            numberOfParts += 1 if value in parts else 0

        unassignedAndOk = anyUnassigned and numberOfParts <= exactNumberOfParts
        exact = not anyUnassigned and numberOfParts == exactNumberOfParts
        if unassignedAndOk or exact:
            return True
        else:
            return False

    return constraint


def noNeighbourConstraintFunction(a, b, c, d, e, f, g, h, i, assignments=None, _unassigned=csp.Unassigned):
    if (e == submarine):
        water_values = [a, b, c, d, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == top):
        if (h not in (bottom, middle, _unassigned)):
            return False
        water_values = [a, b, c, d, f, g, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == bottom):
        if (b not in (top, middle, _unassigned)):
            return False
        water_values = [a, c, d, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == left):
        if (f not in (right, middle, _unassigned)):
            return False
        water_values = [a, b, c, d, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == right):
        if (d not in (left, middle, _unassigned)):
            return False
        water_values = [a, b, c, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False
    
    if (e == middle):

        if b in (top, middle) and (
            d not in (water, _unassigned) 
            or f not in (water, _unassigned)
            or h == water
        ):
            return False

        if h in (bottom, middle) and (
            d not in (water, _unassigned)
            or f not in (water, _unassigned)
            or b == water
            ):
            return False

        if d in (left, middle) and (
            b not in (water, _unassigned) 
            or h not in (water, _unassigned)
            or f == water
        ):
            return False

        if f in (right, middle) and (
            b not in (water, _unassigned) 
            or h not in (water, _unassigned)
            or d == water
        ):
            return False

        water_values = [a, c, g, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    return True


def borderTopConstraintFunction(a1, a2, b1, b2, c1, c2, assignments=None, _unassigned=csp.Unassigned):
    if b1 == bottom:
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a1, b1, c1, a2, b2, c2, _unassigned)):
        return False

    return True


def borderBottomConstraintFunction(a1, a2, b1, b2, c1, c2, assignments=None, _unassigned=csp.Unassigned):
    if b2 == top:
        return False

    if (not noNeighbourConstraintFunction(a1, b1, c1, a2, b2, c2, 7, 7, 7, _unassigned)):
        return False

    return True


def borderLeftConstraintFunction(a1, b1, a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if a2 == right:
        return False

    if (not noNeighbourConstraintFunction(7, a1, b1, 7, a2, b2, 7, a3, b3, _unassigned)):
        return False

    return True


def borderRightConstraintFunction(a1, b1, a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 == left:
        return False

    if (not noNeighbourConstraintFunction(a1, b1, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


for rowIndex, numberOfParts in enumerate(parts_in_row):
    row = rows[rowIndex]
    constraint = csp.FunctionConstraint(getNumberOfPartsConstraint(
        numberOfParts, rowIndex=rowIndex), assigned=debugAssigned)
    bimaru.addConstraint(constraint, row)

for colIndex, numberOfParts in enumerate(parts_in_col):
    col = cols[colIndex]
    constraint = csp.FunctionConstraint(getNumberOfPartsConstraint(
        numberOfParts, colIndex=colIndex), assigned=debugAssigned)
    bimaru.addConstraint(constraint, col)

noNeighbourConstraint = csp.FunctionConstraint(
    noNeighbourConstraintFunction, assigned=debugAssigned)
for box in boxes:
    bimaru.addConstraint(noNeighbourConstraint, box)


borderTopConstraint = csp.FunctionConstraint(
    borderTopConstraintFunction, assigned=debugAssigned)
for box in border_boxes_top:
    bimaru.addConstraint(borderTopConstraint, box)

borderBottomConstraint = csp.FunctionConstraint(
    borderBottomConstraintFunction, assigned=debugAssigned)
for box in border_boxes_bottom:
    bimaru.addConstraint(borderBottomConstraint, box)

borderLeftConstraint = csp.FunctionConstraint(
    borderLeftConstraintFunction, assigned=debugAssigned)
for box in border_boxes_left:
    bimaru.addConstraint(borderLeftConstraint, box)

borderRightConstraint = csp.FunctionConstraint(
    borderRightConstraintFunction, assigned=debugAssigned)
for box in border_boxes_right:
    bimaru.addConstraint(borderRightConstraint, box)


def cornerTopLeftConstraintFunction(b2, c2, b3, c3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (right, bottom, middle):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, 7, b2, c2, 7, b3, c3, _unassigned)):
        return False

    return True


def cornerTopRightConstraintFunction(a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (left, bottom, middle):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


def cornerBottomRightConstraintFunction(a1, b1, a2, b2, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (left, top, middle):
        return False

    if (not noNeighbourConstraintFunction(a1, b1, 7, a2, b2, 7, 7, 7, 7, _unassigned)):
        return False

    return True


def cornerBottomLeftConstraintFunction(b1, c1, b2, c2, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (right, bottom, middle):
        return False

    if (not noNeighbourConstraintFunction(7, b1, c1, 7, b2, c2, 7, 7, 7, _unassigned)):
        return False

    return True


                     
def cornerTopRightConstraintFunction(a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (left, bottom, middle):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


cornerTopLeftConstraint = csp.FunctionConstraint(
    cornerTopLeftConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerTopLeftConstraint, corner_top_left_box)

cornerTopRightConstraint = csp.FunctionConstraint(
    cornerTopRightConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerTopRightConstraint, corner_top_right_box)

cornerBottomRightConstraint = csp.FunctionConstraint(
    cornerBottomRightConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerBottomRightConstraint, corner_bottom_right_box)

cornerBottomLeftConstraint = csp.FunctionConstraint(
    cornerBottomLeftConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerBottomLeftConstraint, corner_bottom_left_box)

def partTypeCountConstraintFunction(*args, assignments=None, _unassigned=csp.Unassigned):
    count_top = args.count(top)
    count_right = args.count(right)
    count_bottom = args.count(bottom)
    count_left = args.count(left)
    count_boat_submarine = args.count(submarine)
    count_unassigned = args.count(_unassigned)
    count_middles = args.count(middle)

    target_nr_big_boats = target_boat_double + \
        target_boat_triple + target_boat_quadrouple
    target_middles = target_boat_triple + 2*target_boat_quadrouple

    if (count_top + count_left) > target_nr_big_boats:
        return False
    if (count_bottom + count_right) > target_nr_big_boats:
        return False

    if (count_boat_submarine > target_boat_submarine):
        return False

    if count_middles > target_middles:
        return False

    if count_unassigned == 0:
        if (count_top + count_left) != target_nr_big_boats:
            return False
        if count_middles != target_middles:
            return False

        if count_top != count_bottom or count_left != count_right:
            return False

    return True


partTypeCountConstraint = csp.FunctionConstraint(
    partTypeCountConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(partTypeCountConstraint, flatVariables)


def boatTypeCountConstraintFunction(*args, assignments=None, _unassigned=csp.Unassigned):
    boatTypes = {}
    anyBoatIncomplete = False

    for i, value in enumerate(args):
        colIndex = i % len(cols)
        rowIndex = int(i / len(cols))
        boatLength = 0

        if value == top:
            for j in range(1, 4):
                if i + j*len(cols) > len(args)-1:
                    return False

                field = args[i + j*len(cols)]
                if field in [middle, bottom]:
                    if field == bottom:
                        boatLength = j+1
                        break
                else:
                    anyBoatIncomplete = True
                    break

        if value == left:
            for j in range(1, 4):
                if colIndex + j > len(cols)-1:
                    return False

                field = args[i + j]
                if field in [middle, right]:
                    if field == right:
                        boatLength = j+1
                        break
                else:
                    anyBoatIncomplete = True
                    break

        if value == submarine:
            boatLength = 1

        if boatLength != 0:
            boatTypes[boatLength] = boatTypes.get(boatLength, 0) + 1

    if args.count(_unassigned) == 0:
        if len(boatTypes) != len(targetBoatTypes) or anyBoatIncomplete:
            return False
        for boatType, count in boatTypes.items():
            if targetBoatTypes[boatType] != count:
                return False
    else:
        for boatType, count in boatTypes.items():
            if boatType not in targetBoatTypes:
                return False

            if targetBoatTypes[boatType] < count:
                return False

    return True

boatTypeCountConstraint = csp.FunctionConstraint(
    boatTypeCountConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(boatTypeCountConstraint, flatVariables)

# ------------------------------------------------------------------------------
# solve CSP
# ------------------------------------------------------------------------------
start_time = time.time()
solutions = bimaru.getSolutions()

# solutions = [solutions[randrange(len(solutions)-1)]]
# solutions = [bimaru.getSolution()]

print('')
print('Time taken:')
print(f"--- {time.time() - start_time} seconds ---")

print('')
print(f'Number of solutions found: {len(solutions)}')

part_map = {
    1: '∩',
    2: '⊃',
    3: '∪',
    4: '⊂',
    5: '□',
    6: '○',
    7: '░',
}

for solution in solutions:
    col_count = len(cols)
    row_count = len(cols)
    h_length = (4*col_count)-1
    space_between_cols = math.floor((h_length)/2)

    print('')
    print('┌' + space_between_cols*'─' + '┬' + space_between_cols*'─' + '┐')
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            print(
                (" " if j > 0 else "") + \
                ("| " if j % (col_count/2) == 0 else "  ") + \
                str(part_map[solution[col]]) \
            , end="")
        print(' |')
        if i == math.floor(row_count/2) - 1:
            print('├' + space_between_cols*'─' + '┼' + space_between_cols*'─' + '┤')
        elif i < row_count-1:
            print('│' + space_between_cols*' ' + '│' + space_between_cols*' ' + '│')
    print('└' + space_between_cols*'─' + '┴' + space_between_cols*'─' + '┘')

    # break

conversions = {
    1: 'U',
    2: 'R',
    3: 'D',
    4: 'L',
    5: 'M',
    6: 'S',
    7: 'W',
}

# Output the file
output = open(output_file, "w")
for i in range(n):
    for j in range(n):
        output.write((str(board[i][j])))
    output.write("\n")