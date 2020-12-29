from sudoku_connections import SudokuConnections
import numpy as np
import json


def getBoard():
    with open('data/sudoku_02.json') as json_file:
        board = json.load(json_file)

    # board = np.zeros(shape=(9, 9), dtype='int64')
    # board[1, 0] = board[1, 1] = 1
    return board


class SudokuBoard:

    def __init__(self):

        self.board = getBoard()
        self.sudokuGraph = SudokuConnections()
        self.mappedGrid = np.arange(1, 82).reshape((9, 9))

        self.allLabelsAvailable()
        self.enforcingArcConsistency()

    def printBoard(self):

        print("    1 2 3     4 5 6     7 8 9")
        for i in range(len(self.board)):
            if i % 3 == 0:  # and i != 0:
                print("  - - - - - - - - - - - - - - ")

            for j in range(len(self.board[i])):
                if j % 3 == 0:  # and j != 0 :
                    print(" |  ", end="")
                if j == 8:
                    print(self.board[i][j], " | ", i + 1)
                else:
                    print(f"{self.board[i][j]} ", end="")
        print("  - - - - - - - - - - - - - - ")

    def allLabelsAvailable(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                idx = self.mappedGrid[row][col]
                if self.board[row][col] != 0:
                    self.sudokuGraph.graph.allNodes[idx].setAvailableLabels({self.board[row][col]})
                else:
                    self.sudokuGraph.graph.allNodes[idx].setAvailableLabels(set(range(10)))

    def enforcingArcConsistency(self):

        for i in range(81):
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    idx = self.mappedGrid[row][col]

                    for connection in self.sudokuGraph.graph.allNodes[idx].getConnections():
                        avaiLabels = self.sudokuGraph.graph.allNodes[connection].getAvailableLabels()

                        try:
                            avaiLabels.remove(self.board[row][col])
                        except KeyError:
                            pass
                        self.sudokuGraph.graph.allNodes[connection].setAvailableLabels(avaiLabels)

            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    idx = self.mappedGrid[row][col]
                    if len(self.sudokuGraph.graph.allNodes[idx].getAvailableLabels()) == 1:
                        self.board[row][col] = list(self.sudokuGraph.graph.allNodes[idx].getAvailableLabels())[0]


if __name__ == "__main__":
    s = SudokuBoard()
    # s.printBoard()
    a = s.board
    for i in range(1, 82):
        print(i, s.sudokuGraph.graph.allNodes[i].getAvailableLabels())
    b = s.board
    # s.printBoard()
    print(a == b)

