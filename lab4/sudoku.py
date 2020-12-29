import numpy as np
import json


# TODO:
#  - define the order of traversing objects and labels in objects
#  - start with the first object
#  - deep copy the current graph
#  - select the first label in the selected object, make the rest of the labels unavailable
#  - start enforcing arc consistency (deleting)
#  - if everything is crossed out, then go back to the step of copying the graph and select the next label
#  - if there is something left, then we fix this state of the graph and return to the second step,
#  but to the next object
#  - if we have sorted out all objects, then we have a solution
#  - else solution is not found


def print_board(board):

    for i in range(len(board)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(board[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(board[i][j])+" "
        print(line)
    print("\n")


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
