import numpy as np
from graph import Graph


def whatToConnect(matrix, rows, cols):
    """
    matrix : stores the id of each node representing each cell

    returns dictionary

    connections - dictionary
    rows : [all the ids in the rows]
    cols : [all the ids in the cols]
    blocks : [all the ids in the block]

    ** to be connected to the head.
    """
    connections = dict()

    connections["rows"] = [matrix[rows][c] for c in range(cols + 1, 9)]  # ROWS
    connections["cols"] = [matrix[r][cols] for r in range(rows + 1, 9)]  # COLS
    connections["blocks"] = [matrix[x][y] for x in range(3 * (rows // 3), 3 * (rows // 3) + 3)
                             for y in range(3 * (cols // 3), 3 * (cols // 3) + 3) if matrix[x][y] not in
                             matrix[rows, :] and matrix[x][y] not in matrix[:, cols]]  # BLOCKS
    return connections


class SudokuConnections:
    def __init__(self):

        self.graph = Graph()  # Graph Object

        self.rows = 9
        self.cols = 9
        self.total_blocks = self.rows * self.cols  # 81

        self.__generateGraph()  # Generates all the nodes
        self.connectEdges()  # connects all the nodes according to sudoku constraints

        self.allIds = self.graph.getAllNodesIds()  # storing all the ids in a list

    def __generateGraph(self):
        """
        Generates nodes with id from 1 to 81.
        Both inclusive
        """
        for idx in range(1, self.total_blocks + 1):
            self.graph.addNode(idx)

    def connectEdges(self):
        """
        Connect nodes according to Sudoku Constraints :

        # ROWS
        from start of each id number connect all the successive numbers till you reach a multiple of 9


        # COLS (add 9 (+9))
        from start of id number. +9 for each connection till you reach a number >= 73 and <= 81

        # BLOCKS
        Connect all the elements in the block which do not come in the same column or row.
        1   2   3
        10  11  12
        19  20  21

        1 -> 11, 12, 20, 21
        2 -> 10, 19, 12, 21
        3 -> 10, 11, 19, 20
        Similarly for 10, 11, 12, 19, 20, 21.

        """
        matrix = np.arange(1, self.total_blocks + 1).reshape((self.rows, self.cols))
        head_connections = dict()  # head : connections
        for row in range(self.rows):
            for col in range(self.cols):
                head = matrix[row][col]  # id of the node
                connections = whatToConnect(matrix, row, col)
                head_connections[head] = connections
        # connect all the edges
        self.__connectThose(head_connections=head_connections)

    def __connectThose(self, head_connections):
        for head in head_connections.keys():  # head is the start idx
            connections = head_connections[head]
            for key in connections:  # get list of all the connections
                for v in connections[key]:
                    self.graph.addEdge(src=head, dst=v)


def test_whatToConnect():

    a = b = 9
    matrix = np.arange(1, a * b + 1).reshape((a, b))
    rows = np.random.choice(a=np.arange(a), size=[])
    cols = np.random.choice(a=np.arange(b), size=[])

    assert type(whatToConnect(matrix, rows, cols)) == dict
    assert len(whatToConnect(matrix, rows, cols).keys()) == 3
    assert list(whatToConnect(matrix, rows, cols).keys()) == ["rows", "cols", "blocks"]


if __name__ == "__main__":

    sudoku = SudokuConnections()

    for i in sudoku.graph.getAllNodesIds():
        print(i, "Connected to->", sudoku.graph.allNodes[i].getConnections())

    test_whatToConnect()
