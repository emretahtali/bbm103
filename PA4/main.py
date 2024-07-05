import sys


def has_same_neighbor(row, col, valley_list):
    """checks if the given cell has an identical neighbor"""
    for i in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        try:
            if valley_list[row][col] == valley_list[row + i[0]][col + i[1]]: return True
        except IndexError: continue
    return False


def cons_met(row, col, valley_list, constraints):
    """checks if the given cell is at one of the sides of the grid, if it is, checks if the given constraints are met"""
    row_highs, row_bases, col_highs, col_bases = constraints

    if (col == len(valley_list[row]) - 1 and valley_list[row].count("H") < row_highs[row]
        or col == len(valley_list[row]) - 1 and valley_list[row].count("B") < row_bases[row]
            or row == len(valley_list) - 1 and [i[col] for i in valley_list].count("H") < col_highs[col]
                or row == len(valley_list) - 1 and [i[col] for i in valley_list].count("B") < col_bases[col]):
        return False
    else: return True


def wrong_highs(row, col, valley_list, constraints, next_row, next_col):
    """checks if the 'high' value is placed incorrectly at the given cell"""
    row_highs, row_bases, col_highs, col_bases = constraints

    if (row_highs[row] != -1 and valley_list[row].count("H") > row_highs[row]
        or col_highs[col] != -1 and [i[col] for i in valley_list].count("H") > col_highs[col]
            or not cons_met(row, col, valley_list, constraints)
                or has_same_neighbor(row, col, valley_list)
                    or not try_cell(next_row, next_col, valley_list, constraints)):
        return True
    else: return False


def wrong_bases(row, col, valley_list, constraints, next_row, next_col):
    """checks if the 'base' value is placed incorrectly at the given cell"""
    row_highs, row_bases, col_highs, col_bases = constraints

    if (row_bases[row] != -1 and valley_list[row].count("B") > row_bases[row]
        or col_bases[col] != -1 and [i[col] for i in valley_list].count("B") > col_bases[col]
            or not cons_met(row, col, valley_list, constraints)
                or has_same_neighbor(row, col, valley_list)
                    or not try_cell(next_row, next_col, valley_list, constraints)):
        return True
    else: return False


def wrong_neutrals(row, col, valley_list, constraints, next_row, next_col):
    """checks if the 'neutral' value is placed incorrectly at the given cell"""
    if (not cons_met(row, col, valley_list, constraints)
            or not try_cell(next_row, next_col, valley_list, constraints)):
        return True
    else: return False


def try_cell(row, col, valley_list, constraints):
    """checks if the given cell has any potential for further playing, if so, keeps playing"""
    # base condition.
    if row == -1:
        if cons_met(len(valley_list) - 1, len(valley_list[0]) - 1, valley_list, constraints):
            return True

    val = valley_list[row][col]

    # gets the next cell's coordinates
    if col + 1 >= len(valley_list[row]):
        next_row = -1 if row + 1 >= len(valley_list) else row + 1
        next_col = 0
    else:
        next_row = row
        next_col = col + 1

    # if the cell holds "L" or "U" start checking the values one after another
    if val == "L" or val == "U":
        valley_list[row][col] = "H"

        if wrong_highs(row, col, valley_list, constraints, next_row, next_col):
            valley_list[row][col] = "B"

            if wrong_bases(row, col, valley_list, constraints, next_row, next_col):
                valley_list[row][col] = "N"

                if wrong_neutrals(row, col, valley_list, constraints, next_row, next_col):
                    valley_list[row][col] = val

                    return False

    # if the cell holds "R" or "D", write a new value based on the opposite of the linked cell's value
    else:
        offset = [0, -1] if val == "R" else [-1, 0]

        if valley_list[row + offset[0]][col + offset[1]] == "H":
            valley_list[row][col] = "B"

            if wrong_bases(row, col, valley_list, constraints, next_row, next_col):
                valley_list[row][col] = val
                return False

        elif valley_list[row + offset[0]][col + offset[1]] == "B":
            valley_list[row][col] = "H"

            if wrong_highs(row, col, valley_list, constraints, next_row, next_col):
                valley_list[row][col] = val
                return False

        else:
            valley_list[row][col] = "N"

            if wrong_neutrals(row, col, valley_list, constraints, next_row, next_col):
                valley_list[row][col] = val
                return False

    return True


def main():
    # read the input from the file and making preparations
    with open(sys.argv[1], "r") as f:
        f_list = f.readlines()

    row_highs = [int(i) for i in f_list[0].split()]
    row_bases = [int(i) for i in f_list[1].split()]
    col_highs = [int(i) for i in f_list[2].split()]
    col_bases = [int(i) for i in f_list[3].split()]

    constraints = [row_highs, row_bases, col_highs, col_bases]

    valley_list = list(map(lambda x: x.split(), f_list[4:]))

    # call the program and write the results to the output file
    with open(sys.argv[2], "w") as f:
        if not try_cell(0, 0, valley_list, constraints): f.write("No solution!")
        else:
            output_list = []
            for i in valley_list:
                output_list.append("")
                for j in range(len(i) - 1): output_list[-1] += i[j] + " "
                output_list[-1] += i[len(i) - 1]

            for i in range(len(output_list) - 1):
                f.write(output_list[i] + "\n")
            f.write((output_list[len(output_list) - 1]))


if __name__ == "__main__": main()