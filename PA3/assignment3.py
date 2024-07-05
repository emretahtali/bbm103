import sys

# get the input and turn it into a list
file = open(sys.argv[1], "r")
bubble_list = [[i for i in j.split()] for j in file.read().split("\n")]
file.close()

score = 0


def print_bubbles():
    """print the current state of the board and the score"""
    global bubble_list, score

    for i in range(len(bubble_list)):
        for j in range(len(bubble_list[i]) - 1):
            print(bubble_list[i][j] + " ", end="")
        print(bubble_list[i][len(bubble_list[i]) - 1])

    print(f"\nYour score is: {score}")


def check_bubble(row, col, num):
    """if there is an identical cell around the given cell, empty it and this time start checking around the new one"""
    global bubble_list, score
    no_neighbors = True

    # right
    if col + 1 < len(bubble_list[row]):
        if bubble_list[row][col + 1] == num:
            pop_bubble(row, col + 1, num)
            no_neighbors = False

    # bottom
    if row + 1 < len(bubble_list):
        if bubble_list[row + 1][col] == num:
            pop_bubble(row + 1, col, num)
            no_neighbors = False

    # left
    if col - 1 >= 0:
        if bubble_list[row][col - 1] == num:
            pop_bubble(row, col - 1, num)
            no_neighbors = False

    # top
    if row - 1 >= 0:
        if bubble_list[row - 1][col] == num:
            pop_bubble(row - 1, col, num)
            no_neighbors = False

    return no_neighbors


def pop_bubble(row, col, num):
    """empty the cell, add it's value to the score and start checking around it"""
    global bubble_list, score

    bubble_list[row][col] = " "
    score += int(num)
    check_bubble(row, col, num)


def shift_rows():
    """if the whole row is empty, discard it"""
    global bubble_list

    # shift the rows up if there is an empty row
    row = 0
    while row < len(bubble_list):
        if bubble_list[row].count(" ") == len(bubble_list[row]):
            bubble_list.pop(row)
        else:
            row += 1


def shift_columns():
    """if the whole column is empty, discard it"""
    global bubble_list

    # shift the columns left if there is an empty column
    col = 0
    while col < len(bubble_list[0]):
        list_ = [bubble_list[row][col] for row in range(len(bubble_list))]
        if list_.count(" ") == len(list_):
            for row in range(len(bubble_list)):
                bubble_list[row].pop(col)
        else:
            col += 1


def shift_bubbles():
    """if there is a cell with an empty neighbor below, shift it down"""
    global bubble_list

    # shift the bubbles down if there is an empty bubble below
    while True:
        not_done = False

        for i in range(len(bubble_list) - 1):
            for j in range(len(bubble_list[i])):
                if bubble_list[i][j] != " " and bubble_list[i + 1][j] == " ":
                    not_done = True
                    # swap elements
                    bubble_list[i][j], bubble_list[i + 1][j] = bubble_list[i + 1][j], bubble_list[i][j]

        if not not_done: break


def shift_grid():
    """reshape the grid, getting rid of the empty rows, columns and fixing the flying cells"""
    shift_rows()
    shift_bubbles()
    shift_rows()
    shift_columns()
    main()


def check_if_playable():
    """check if there are any cells left that has an identical neighbor cell, if so, keep playing"""
    global bubble_list

    playable = False
    for row in range(len(bubble_list)):
        for col in range(len(bubble_list[row])):
            num = bubble_list[row][col]
            if num != " ":
                if row + 1 < len(bubble_list):
                    if num == bubble_list[row + 1][col]: playable = True

                if row - 1 >= 0:
                    if num == bubble_list[row - 1][col]: playable = True

                if col + 1 < len(bubble_list[row]):
                    if num == bubble_list[row][col + 1]: playable = True

                if col - 1 >= 0:
                    if num == bubble_list[row][col - 1]: playable = True

    if not playable:
        print("\nGame over")
        exit()


def take_input():
    """ask the player for which cell to play on"""
    global bubble_list

    coords = input("\nPlease enter a row and a column number: ").split()
    print("\n", end="")
    coords = list(map(int, coords))
    coords[0] -= 1
    coords[1] -= 1

    if coords[0] < 0 or coords[0] > len(bubble_list) - 1 or coords[1] < 0 or coords[1] > len(bubble_list[0]) - 1:
        print("Please enter a correct size!")
        coords = take_input()

    elif bubble_list[coords[0]][coords[1]] == " ":
        print("No movement happened try again")
        coords = take_input()

    return coords


def main():
    """print the current state of the board, check if it can still be played, if so take input and play the game"""
    global bubble_list, score

    print_bubbles()

    check_if_playable()

    coords = take_input()

    num = bubble_list[coords[0]][coords[1]]

    if check_bubble(coords[0], coords[1], num):
        print("No movement happened try again\n")
        main()
    else:
        if bubble_list.count([" " for i in bubble_list[0]]) == len(bubble_list):
            print(f"Your score is {score}\n\nGame over")
            exit()
        shift_grid()


if __name__ == '__main__': main()