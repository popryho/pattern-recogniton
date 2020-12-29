class Node:

    def __init__(self, idx, data=0):  # Constructor
        """
        id : Integer (1, 2, 3, ...)
        """
        self.id = idx
        self.data = data
        self.connectedTo = dict()
        self.availableLabels = set()

    def addNeighbour(self, neighbour, weight=0):
        """
        neighbour : Node Object
        weight : Default Value = 0

        adds the neighbour_id : wt pair into the dictionary
        """
        if neighbour.id not in self.connectedTo.keys():
            self.connectedTo[neighbour.id] = weight

    # setter
    def setData(self, data):
        self.data = data

    def setAvailableLabels(self, new_labels):
        self.availableLabels = new_labels

    # getter
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
    totalV = 0  # total vertices in the graph

    def __init__(self):
        """
        allNodes = Dictionary (key:value)
                   idx : Node Object
        """
        self.allNodes = dict()

    def addNode(self, idx):
        """ adds the node """
        if idx in self.allNodes:
            return None

        Graph.totalV += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node

    def addNodeData(self, idx, data):
        """ set node data acc to idx """
        if idx in self.allNodes:
            node = self.allNodes[idx]
            node.setData(data)
        else:
            print("No ID to add the data.")

    def addEdge(self, src, dst, wt=0):
        """
        Adds edge between 2 nodes
        Undirected graph

        src = node_id = edge starts from
        dst = node_id = edge ends at

        To make it a directed graph comment the second line
        """
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt)
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)

    def isNeighbour(self, u, v):
        """
        check neighbour exists or not
        """
        if 1 <= u <= 81 and 1 <= v <= 81 and u != v:
            if v in self.allNodes[u].getConnections():
                return True
        return False

    # getter
    def getNode(self, idx):
        if idx in self.allNodes:
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self):
        return self.allNodes.keys()


if __name__ == '__main__':

    g = Graph()
    for i in range(1, 10):
        g.addNode(i)
    print(g.getAllNodesIds())
