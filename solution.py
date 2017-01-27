assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]

column_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

diagonalA = [(rows[index] + cols[index]) for index in range(0,9)]

diagonalB = [(rows[index] + str(10-int(cols[index]))) for index in range(0,9)]

solved_values_already_processed = set()

# -----------------------------------------------------------------------------

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


# -----------------------------------------------------------------------------

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all boxes that store a value with length two
    for box in values:

        if len(values[box]) != 2:
            continue

        # Iterate over the peers and try to find a peer with size two that is
        # in the same column or row and has the same value.

        for peer in peers[box]:

            # Skip peer if its values length is not two.
            if len(values[peer]) != 2:
                continue

            # Skip all peer if it has a different value.
            if values[box] != values[peer]:
                continue

            # Peer is in the same row.
            if box[0] == peer[0]:
                for candidate in units[box][0]:
                    if candidate != peer and candidate != box:
                        for value in values[box]:
                            values[candidate] = values[candidate].replace(value, '')

            # Peer is in the same column.
            elif box[1] == peer[1]:
                for candidate in units[box][1]:
                    if candidate != peer and candidate != box:
                        for value in values[box]:
                            values[candidate] = values[candidate].replace(value, '')

    return values

# -----------------------------------------------------------------------------

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """

    chars = []
    digits = '123456789'

    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)

    # ensure that the composed string holds exactly 81 characters (9x9)
    assert len(chars) == 81

    # return the sudoku grid as a dictionary with every possible value in each
    # field. In an empty field, 1 to 9 could be possible. In later steps the
    # impossible values are going to be eliminated.
    return dict(zip(boxes, chars))

# -----------------------------------------------------------------------------

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# -----------------------------------------------------------------------------

def eliminate(values):
    """
    Find all boxes that have a single value and eliminate this value from all
    of its peers.
    Input: A sudoku puzzle in dictionary form
    Output: The cleaned sudoku puzzle in dictionary form
    """

    # create an array that stores all the boxes that include only one value
    solved_values = [box for box in values.keys() if len(values[box]) == 1 and box not in solved_values_already_processed]

    # iterate over all the solved boxes and clear the value of the box from
    # all of its peers.
    for box in solved_values:
        solved_values_already_processed.add(box)
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box], '')

    return values

# -----------------------------------------------------------------------------

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only
    fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:

        for digit in '123456789':

            # dplaces stores all the boxes that hold the digit of the current
            # iteration.
            dplaces = [box for box in unit if digit in values[box]]

            # if a box includes a digit exclusively, set the boxes value
            # to this digit. For example: If the digit 1 is only possible in
            # box A3, then dplaces[0] stores A3. The directory entry for A3
            # within the values dictionary will be set to the current digit.
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values

# -----------------------------------------------------------------------------

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with
    no available values, return False. If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return
    the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    stalled = False

    while not stalled:

        # Store the number of solved values before the strategies were applied.
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply Eliminate Strategy
        values = eliminate(values)

        # Apply Only Choice Strategy
        values = only_choice(values)

        # Apply Naked Twins Strategy
        #values = naked_twins(values)

        # Store the number of solved values after the strategies were applied.
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, set stalled to True to exit the loop.abs
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

# -----------------------------------------------------------------------------

def diagonalConstraintsHurt(values):
    """
    Evaluates if values of length 1 in one of the two diagonals hurt the
    uniqueness constraint.
    Input: values dictionary
    Output: True if the constraint is hurt
            False if the constraint is met
    """

    if checkDiagonalConstraint(diagonalA, values) is True:
        return True

    if checkDiagonalConstraint(diagonalB, values) is True:
        return True

    return False

# -----------------------------------------------------------------------------

def checkDiagonalConstraint(diagonal, values):
    """
    Checks the uniqueness constraint for a single diagonal.
    Input: List of diagonals
    Output: True if the constraint is hurt
            False if the constraint is met
    """
    seen = []

    for box in diagonal:
        if len(values[box]) == 1:
            for value in values[box]:
                if value in seen:
                    return True  # if value was already seen, return true
                seen.append(value)

    return False

# -----------------------------------------------------------------------------

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    solved_values_already_processed.clear()

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Return false if reduce_puzzle returned false.
    if values is False:
        return False

    # Return false if diagonal uniqueness constrained is hurt.
    if diagonalConstraintsHurt(values) is True:
        return False

    # Return the values when every field holds only one value. The puzzle has been solved!
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Chose one of the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a
    # value (not False), return that answer!

    # Iterate over the values in the box[s]
    for value in values[s]:

        # Copy the board.
        new_sudoku = values.copy()

        # Set the field in the copied board to the value of the current iteration.
        new_sudoku[s] = value

        # Try to solve the game and return the attempt, which could be True, False or
        # a new board which must be iterated.
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# -----------------------------------------------------------------------------

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    if isinstance(grid, str):
        return search(grid_values(grid))

    return search(grid)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
