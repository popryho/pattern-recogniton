from graph import Graph
from what_to_connect import whatToConnect
import numpy as np


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
        for idx in range(1, self.total_blocks + 1):
            self.graph.addNode(idx)

    def connectEdges(self):
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


if __name__ == "__main__":

    sudoku = SudokuConnections()

    for i in sudoku.graph.getAllNodesIds():
        print(i, "Connected to->", sudoku.graph.allNodes[i].getConnections())
