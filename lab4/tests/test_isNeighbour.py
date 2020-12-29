from ..graph import Graph


def test_isNeighbour():
    g = Graph()
    for i in range(6):
        g.addNode(i)

    g.addEdge(src=0, dst=1, wt=5)
    g.addEdge(0, 5, 2)
    g.addEdge(1, 2, 4)
    g.addEdge(2, 3, 9)
    g.addEdge(3, 4, 7)
    g.addEdge(3, 5, 3)
    g.addEdge(4, 0, 1)
    g.addEdge(5, 4, 8)
    g.addEdge(5, 2, 1)

    assert not g.isNeighbour(5, 0)
    assert not g.isNeighbour(2, 0)
    assert 3 in g.getNode(2).getConnections()
