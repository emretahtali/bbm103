import sys
import math


def count_in_row(row, num, table):
    # check how many times the given number exists in the given row
    return table[row].count(str(num))


def count_in_column(column, num, table):
    # check how many times the given number exists in the given column
    number = 0
    for i in range(9):
        if table[i][column] == str(num): number += 1
    return number


def count_in_block(row, column, num, blocks_table):
    # find which block(subgrid) holds the number
    block_row = math.floor(row / 3)
    block_column = math.floor(column / 3)

    # check how many times the given number exists in the given block(subgrid)
    return blocks_table[block_row][block_column].count(str(num))


def update_sudoku_blocks(blocks_table, number_table):
    # empty the blocks(subgrids) table
    for i in range(3):
        for j in range(3):
            blocks_table[i][j] = []

    # refill the blocks(subgrids) table according to the main sudoku table
    for i in range(9):
        for j in range(9):
            block_x = math.floor(i / 3)
            block_y = math.floor(j / 3)

            blocks_table[block_x][block_y].append(number_table[i][j])


def log_step(row, column, num, output, number_table, step):
    # add the new step to the output string

    # add the step information
    if output != "": output += "\n"
    output += f"------------------\nStep {step} - {num} @ R{row + 1}C{column + 1}\n------------------"

    # add the new state of the sudoku table
    for i in range(9):
        output += "\n"

        for j in range(8): output += number_table[i][j] + " "
        output += number_table[i][8]

    # return the updated output string
    return output


def main():
    # get the text from the input file
    input_file = open(sys.argv[1], "r")
    input_txt = input_file.read()
    input_file.close()

    output_str = ""
    step_number = 1

    # determine the desired step count
    sudoku_list = input_txt.split()
    step_count = sudoku_list.count("0")

    # create the sudoku table
    sudoku_table = [sudoku_list[i * 9: (i + 1) * 9] for i in range(9)]

    # create a separate table for the blocks(subgrids) for convenience
    sudoku_blocks = [[[] for i in range(3)] for j in range(3)]
    update_sudoku_blocks(sudoku_blocks, sudoku_table)

    # for every step, go through every 0 one by one in order to find the one that can get only one value
    for steps in range(step_count):
        next_step = False
        for i in range(9):
            for j in range(9):
                if sudoku_table[i][j] == "0":
                    # check how many numbers can the cell hold
                    numbers = []

                    for k in range(1, 10):
                        # from 1 to 10, check how many times the number can be found in the same row, column and block(subgrid)
                        in_row = count_in_row(i, k, sudoku_table)
                        in_column = count_in_column(j, k, sudoku_table)
                        in_block = count_in_block(i, j, k, sudoku_blocks)

                        # if the number doesn't exist in the row, column and block(subgrid), add it to the list
                        if in_row + in_column + in_block == 0: numbers.append(k)

                    if len(numbers) == 1:
                        # if there is only one number that the cell can hold, update the sudoku tables
                        sudoku_table[i][j] = str(numbers[0])
                        update_sudoku_blocks(sudoku_blocks, sudoku_table)

                        # update the output string
                        output_str = log_step(i, j, numbers[0], output_str, sudoku_table, step_number)

                        # get to the next step
                        step_number += 1
                        next_step = True

                        break

            if next_step: break

    # add the final dashes at the end of the file
    output_str += "\n------------------"

    # write the results to the output file
    output_file = open(sys.argv[2], "w")
    output_file.write(output_str)
    output_file.flush()
    output_file.close()


if __name__ == "__main__":
    main()