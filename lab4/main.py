from sudoku_connections import SudokuConnections
import numpy as np
import json
import copy


# TODO:
#  - start with the first object
#  - deep copy the current graph
#  - select the first label in the selected object, make the rest of the labels unavailable
#  - start enforcing arc consistency (deleting)
#  - if everything is crossed out, then go back to the step of copying the graph and select the next label
#  - if there is something left, then we fix this state of the graph and return to the second step,
#  but choosing the next label
#  - if we have sorted out all objects, then we have a solution
#  - else solution is not found

class SudokuBoard(object):

    def __init__(self, board):

        self.board = board
        self.sudokuGraph = SudokuConnections()

        # Maps all the ids to the position in the matrix
        self.mappedGrid = np.arange(1, self.sudokuGraph.total_blocks + 1).reshape((self.sudokuGraph.rows,
                                                                                   self.sudokuGraph.cols))
        # Initializing all labels as available
        self.allLabelsAvailable()

    def printBoard(self):

        print("    1 2 3     4 5 6     7 8 9")
        for i in range(len(self.board)):
            if i % 3 == 0:  # and i != 0:
                print("  - - - - - - - - - - - - - - ")

            for j in range(len(self.board[i])):

                label = ' ' if self.board[i][j] == 0 else self.board[i][j]
                if j % 3 == 0:  # and j != 0 :
                    print(" |  ", end="")
                if j == 8:
                    print(label, " | ", i + 1)
                else:
                    print(f"{label} ", end="")
        print("  - - - - - - - - - - - - - - ")

    def allLabelsAvailable(self):

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                idx = self.mappedGrid[row][col]

                if self.board[row][col] != 0:
                    avaiLabel = {self.board[row][col]}
                    self.sudokuGraph.graph.allNodes[idx].setAvailableLabels(avaiLabel)
                else:
                    avaiLabels = set(range(1, self.sudokuGraph.rows + 1))
                    self.sudokuGraph.graph.allNodes[idx].setAvailableLabels(avaiLabels)

    def enforcingArcConsistency(self):
        """
        A function that checks if G is equal to one

        - loop through all objects;
        - go through all the vertices in the object;
        - see which vertices are allowed (q (kappa) = 1), which are not;
        - do they leave the vertices at all the necessary neighbors of the arc
        - if there is no arc to a neighbor, the vertex is marked as unavailable.

        :return: 0 if G = 0 and 1 if G = 1
        """
        while True:

            upd = 0  # a variable that tracks changes

            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    idx = self.mappedGrid[row][col]

                    for connection in self.sudokuGraph.graph.allNodes[idx].getConnections():
                        avaiLabels = self.sudokuGraph.graph.allNodes[connection].getAvailableLabels()
                        try:
                            avaiLabels.remove(self.board[row][col])
                            upd += 1
                        except KeyError:
                            pass
                        if avaiLabels == set():
                            return 0

                        self.sudokuGraph.graph.allNodes[connection].setAvailableLabels(avaiLabels)

                    if self.board[row][col] == 0 and \
                            len(self.sudokuGraph.graph.allNodes[idx].getAvailableLabels()) == 1:
                        finalValue = list(self.sudokuGraph.graph.allNodes[idx].getAvailableLabels())[0]
                        self.board[row][col] = finalValue
                        upd += 1
                        break
            if upd == 0:
                return 1

    def searchMarkup(self):

        """
        A function that tries to find valid markup

        - select objects in turn
        - in each object we iterate over possible labels
        - substitute these labels into the problem as a solution to the problem for a given object
        - if the algorithm still gives one, then this markup is part of a good markup
        - keep going
        - ig G = 0 - choose another label from the object
        :return: self
        """
        for idx in range(1, self.sudokuGraph.graph.totalV + 1):
            avaiLabels = self.sudokuGraph.graph.allNodes[idx].getAvailableLabels()
            if len(avaiLabels) > 1:
                self.sudokuGraph.graph.allNodes[idx].setAvailableLabels({list(avaiLabels)[0]})
                return self

    def sudokuSolver(self):
        """
        A function that bundles the whole solution together.
        - Execute enforcingArcConsistency and then search for the desired markup.
        - If the function chose an unsuccessful label, it means G = 0
        - return a copy of the graph and select the desired label.
        - Go to the step 2 and try again
        :return:
        """
        i, temp = 0, 0
        self.printBoard()
        board = self.board.copy()

        while 0 in [item for sublist in self.board for item in sublist]:

            G = self.enforcingArcConsistency()
            if G == 0 and i == 0:
                print("G = 0. There is no solution for this problem.")
                return 0
            if G == 0 and temp != 0:
                self.sudokuGraph.graph = temp

            temp = copy.deepcopy(self.sudokuGraph.graph)
            self.searchMarkup()

            if i != 0 and (np.abs(self.board - board) < 1).all():
                self.printBoard()
                print("For this problem there is no good polymorphism, which is the semi-lattice operator.")
                return 0

            board = self.board.copy()
            i += 1
        print("\nSolution:")
        self.printBoard()


def getBoard():
    """
    Load sudoku board
    :return: ndarray
    """
    with open('data/sudoku_02.json') as json_file:
        board = np.array(json.load(json_file))

    # board = np.zeros(shape=(9, 9), dtype='int64')
    # board[1, 0] = board[1, 1] = 1
    return board


if __name__ == "__main__":
    sudoku = getBoard()

    s = SudokuBoard(sudoku)
    s.sudokuSolver()
