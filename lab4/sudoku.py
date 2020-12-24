import numpy as np
import json


def print_board(board):
    print("    1 2 3     4 5 6     7 8 9")
    for i in range(len(board)):
        if i % 3 == 0:
            print("  - - - - - - - - - - - - - - ")

        for j in range(len(board[i])):
            if j % 3 == 0:
                print(" |  ", end="")
            if j == 8:
                print(board[i][j], " | ", i + 1)
            else:
                print(f"{board[i][j]} ", end="")
    print("  - - - - - - - - - - - - - - \n")


def find_cell_to_fill(board):
    for x in range(9):
        for y in range(9):
            if board[x][y] == 0:
                return x, y
    return -1, -1


def is_valid(board, i, j, e):
    if all([e != board[i][x] for x in range(9)]):
        if all([e != board[x][j] for x in range(9)]):
            for x in range(3 * (i // 3), 3 * (i // 3) + 3):
                for y in range(3 * (j // 3), 3 * (j // 3) + 3):
                    if board[x][y] == e:
                        return False
            return True
    return False


def solve_sudoku(board, i=0, j=0):
    i, j = find_cell_to_fill(board)
    if i == -1:
        return True
    for e in range(1, 10):
        if is_valid(board, i, j, e):
            board[i][j] = e
            if solve_sudoku(board, i, j):
                return True
            board[i][j] = 0
    return False


if __name__ == '__main__':

    with open('data/sudoku_02.json') as json_file:
        sudoku = np.array(json.load(json_file))

    print_board(sudoku)

    if solve_sudoku(sudoku):
        print_board(sudoku)
    else:
        print("markup not found")
