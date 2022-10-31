from copy import deepcopy

EMPTY_CELL = "E"
WATER_CELL = "W"

SHIP_BITS = ["U",  # Up ship end
             "D",  # Down ship end
             "L",  # Left ship end
             "R",  # Right ship end
             "C",  # center ship
             "O",  # Baby ship 1U
             "-",  # left-right ship mid section
             "|"]  # up-down ship mid section

WATERING_PATTERNS = {
    "U":
        """
        WXW
        WUW
        WWW
        """,
    "D":
        """
        WWW
        WDW
        WXW
        """,
    "L":
        """
        WWW
        WLX
        WWW
        """,
    "R":
        """
        WWW
        XRW
        WWW
        """,
    "C":
        """
        WXW
        XCX
        WXW
        """,
    "O":
        """
        WWW
        WOW
        WWW
        """,
    "-":
        """
        WWW
        X-X
        WWW
        """,
    "|":
        """
        WXW
        W|W
        WXW
        """,
}


class BimaruPuzzle:
    def __init__(self, ascii_grid, counts_per_col, counts_per_row, ships_to_place):
        """
        :param ascii_grid: E=empty, U=ship up, L=ship left, R=ship right, D=ship down, C=ship centre, W=water
        :param counts_per_col:
        :param counts_per_row:
        :param ships_to_place:
        """
        self.grid = ascii_grid
        self.linegrid = None
        self.counts_per_col = counts_per_col  # Number of ship cells in each column
        self.counts_per_row = counts_per_row  # Number of ship cells in each row
        self.ships_to_place = ships_to_place  # The lengths of the ships to be placed
        self.clean_grid()
        self.add_autowater_empty_rows_cols()
        pass

    def solve(self):
        self.add_autowater_empty_rows_cols()
        self.surround_ship_bits()
        self.autofill_water_in_full_rows_cols()

    def get_grid_dims(self):
        return len(self.linegrid), len(self.linegrid[0])

    def clean_grid(self):
        self.linegrid = self.get_clean_grid(self.grid)

    @staticmethod
    def get_clean_grid(stringgrid):
        """
        Converts a string based grid into a cell based grid where each cell is a list element
        :param stringgrid:
        :return:
        """
        gridlines = stringgrid.splitlines(False)
        temp_linegrid = []
        for row in gridlines:
            row = row.strip()
            if row:
                temp_linegrid.append(list(row))
        #print(temp_linegrid)
        return temp_linegrid

    def get_remaining_rol_col_ship_counts(self):
        """
        Returns the number of ship parts still to be placed in each row/column
        :return:
        """
        row_counts = deepcopy(self.counts_per_row)
        col_counts = deepcopy(self.counts_per_col)
        for row_idx, row in enumerate(self.linegrid):
            for col_idx, cell_char in enumerate(row):
                if cell_char in SHIP_BITS:
                    row_counts[row_idx] -= 1
                    col_counts[col_idx] -= 1
        return row_counts, col_counts

    def check_row_col_counts(self, new_grid):
        """
        This method checks if the proposed grid meets all constraints or not
        :param new_grid: A grid in the standard format
        :return: True if all of the row col counts are valid
        """
        row_counts = deepcopy(self.counts_per_row)
        col_counts = deepcopy(self.counts_per_col)
        for row_idx, row in enumerate(new_grid):
            for col_idx, cell_char in enumerate(row):
                if cell_char in SHIP_BITS:
                    row_counts[row_idx] -= 1
                    col_counts[col_idx] -= 1

        # Check that all of the counts are positive still
        rows_healthy = all([count >= 0 for count in row_counts])
        cols_healthy = all([count >= 0 for count in col_counts])
        return rows_healthy and cols_healthy

    def autofill_water_in_full_rows_cols(self):
        """
        Add water cells if all the ship bits for that column/row are populated already.
        :return:
        """
        ships_to_add_to_row, ships_to_add_to_col = self.get_remaining_rol_col_ship_counts()
        for row_idx, row in enumerate(self.linegrid):
            for col_idx, cell_char in enumerate(row):
                if ships_to_add_to_row[row_idx] == 0 or ships_to_add_to_col[col_idx] == 0:
                    if self.linegrid[row_idx][col_idx] == EMPTY_CELL:
                        self.linegrid[row_idx][col_idx] = WATER_CELL

    def add_autowater_empty_rows_cols(self):
        """
        Adds water to rows/cols with no ship bits
        :return:
        """
        for row_idx, row in enumerate(self.linegrid):
            for col_idx, cell_char in enumerate(row):
                if self.counts_per_row[row_idx] == 0 or self.counts_per_col[col_idx] == 0:
                    self.linegrid[row_idx][col_idx] = WATER_CELL

    def _superimpose_grids(self, grid_pattern, centre_row, centre_column):
        # Iterate over the old_grid and modify entries
        new_grid = deepcopy(self.linegrid)
        # Check the center coords are in the grid
        row_healthy = centre_row < len(new_grid)
        col_healthy = centre_column < len(new_grid[0])
        if False in [row_healthy, col_healthy]:
            print("Something is wrong here")
            return

        # Checking the dimensions on the pattern should be 3x3
        patt = self.get_clean_grid(grid_pattern)
        dims_healthy = len(patt) == 3 and len(patt[0]) == 3
        if not dims_healthy:
            print("Provided grid is inadequate")
            return

        grid_row_count, grid_col_count = self.get_grid_dims()
        top_row = min(centre_row - 1, grid_row_count-1)
        bottom_row = max(centre_row + 1, 0)
        right_col = min(centre_column + 1, grid_col_count-1)
        left_col = max(centre_column - 1, 0)

        for row_idx in range(top_row, bottom_row+1):
            for col_idx in range(left_col, right_col+1):
                subgrid_row = row_idx - centre_row + 1
                subgrid_col = col_idx - centre_column + 1
                subcell = patt[subgrid_row][subgrid_col]
                if subcell == WATER_CELL:
                    new_grid[row_idx][col_idx] = subcell  # update cell
        self.linegrid = new_grid

    def surround_ship_bits(self):
        """
        Populates the ship surrounds with water
        :return:
        """
        # Search for ship bits
        for row_idx, row in enumerate(self.linegrid):
            for col_idx, cell in enumerate(row):
                if cell in SHIP_BITS:
                    # Got a bit o ship
                    self._superimpose_grids(WATERING_PATTERNS[cell], row_idx, col_idx)

    def __str__(self):
        if self.linegrid:
            stringgrid = "\n".join(["".join(row) for row in self.linegrid])
            return stringgrid

    def fix_shipbit_orientations(self):
        """
        This method scans the grid for shipbits that are non-orientated "C"
        and attempts to orientate them by finding extremedies of the ship to
        determine the orientation.
        We scan the grid from top-left to bottom right and then use recursion to detect the ship's
        direction
        :return: number of bits fixed
        """
        pass


if __name__ == "__main__":
    puzzle_grid = """EEEEEE
                    EEEEEU
                    EEEEEE
                    EEEEEE
                    EEEEEE
                    EEEEWE
                    """
    sample_puzzle_a = BimaruPuzzle(puzzle_grid,
                                   [3, 1, 3, 3, 1, 3],
                                   [2, 3, 1, 3, 0, 5],
                                   [4, 3, 2, 2, 1, 1, 1]
                                   )
    sample_puzzle_a.solve()
    print(sample_puzzle_a)