class Node:

    def __init__(self, idx, data=0):
        self.id = idx
        self.data = data
        self.connectedTo = dict()
        self.availableLabels = set()

    def addNeighbour(self, neighbour, weight=0):
        if neighbour.id not in self.connectedTo.keys():
            self.connectedTo[neighbour.id] = weight

    def setData(self, data):
        self.data = data

    def setAvailableLabels(self, new_labels):
        self.availableLabels = new_labels

    def getID(self):
        return self.id

    def getData(self):
        return self.data

    def getConnections(self):
        return list(self.connectedTo.keys())

    def getWeight(self, neighbour):
        return self.connectedTo[neighbour.id]

    def getAvailableLabels(self):
        return self.availableLabels


class Graph:
    totalV = 0

    def __init__(self):
        self.allNodes = dict()

    def addNode(self, idx):
        if idx in self.allNodes:
            return None

        Graph.totalV += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node

    def addNodeData(self, idx, data):
        if idx in self.allNodes:
            node = self.allNodes[idx]
            node.setData(data)
        else:
            print("No ID to add the data.")

    def addEdge(self, src, dst, wt=0):
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt)
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)

    def isNeighbour(self, u, v):
        if 1 <= u <= 81 and 1 <= v <= 81 and u != v:
            if v in self.allNodes[u].getConnections():
                return True
        return False

    def getNode(self, idx):
        if idx in self.allNodes:
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self):
        return self.allNodes.keys()


# if __name__ == '__main__':
#
#     import json
#
#     with open('data/sudoku_01.json') as json_file:
#         board = json.load(json_file)
#
#     g = Graph()
#     for i in range(1, 82):
#         g.addNode(i)
#         g.addNodeData(i, [item for sublist in board for item in sublist][i-1])
#     # del g.allNodes
#
#     print(board)
