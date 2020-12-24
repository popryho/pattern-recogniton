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
