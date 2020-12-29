from ..graph import Graph


def test_getAllNodesIds():

    g = Graph()
    for i in range(1, 10):
        g.addNode(i)
    assert list(g.getAllNodesIds()) == ([1, 2, 3, 4, 5, 6, 7, 8, 9])
