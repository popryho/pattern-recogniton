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

    row = []
    col = []
    block = []

    # ROWS
    for c in range(cols + 1, 9):
        row.append(matrix[rows][c])

    connections["rows"] = row

    # COLS
    for r in range(rows + 1, 9):
        col.append(matrix[r][cols])

    connections["cols"] = col

    # BLOCKS

    if rows % 3 == 0:

        if cols % 3 == 0:

            block.append(matrix[rows + 1][cols + 1])
            block.append(matrix[rows + 1][cols + 2])
            block.append(matrix[rows + 2][cols + 1])
            block.append(matrix[rows + 2][cols + 2])

        elif cols % 3 == 1:

            block.append(matrix[rows + 1][cols - 1])
            block.append(matrix[rows + 1][cols + 1])
            block.append(matrix[rows + 2][cols - 1])
            block.append(matrix[rows + 2][cols + 1])

        elif cols % 3 == 2:

            block.append(matrix[rows + 1][cols - 2])
            block.append(matrix[rows + 1][cols - 1])
            block.append(matrix[rows + 2][cols - 2])
            block.append(matrix[rows + 2][cols - 1])

    elif rows % 3 == 1:

        if cols % 3 == 0:

            block.append(matrix[rows - 1][cols + 1])
            block.append(matrix[rows - 1][cols + 2])
            block.append(matrix[rows + 1][cols + 1])
            block.append(matrix[rows + 1][cols + 2])

        elif cols % 3 == 1:

            block.append(matrix[rows - 1][cols - 1])
            block.append(matrix[rows - 1][cols + 1])
            block.append(matrix[rows + 1][cols - 1])
            block.append(matrix[rows + 1][cols + 1])

        elif cols % 3 == 2:

            block.append(matrix[rows - 1][cols - 2])
            block.append(matrix[rows - 1][cols - 1])
            block.append(matrix[rows + 1][cols - 2])
            block.append(matrix[rows + 1][cols - 1])

    elif rows % 3 == 2:

        if cols % 3 == 0:

            block.append(matrix[rows - 2][cols + 1])
            block.append(matrix[rows - 2][cols + 2])
            block.append(matrix[rows - 1][cols + 1])
            block.append(matrix[rows - 1][cols + 2])

        elif cols % 3 == 1:

            block.append(matrix[rows - 2][cols - 1])
            block.append(matrix[rows - 2][cols + 1])
            block.append(matrix[rows - 1][cols - 1])
            block.append(matrix[rows - 1][cols + 1])

        elif cols % 3 == 2:

            block.append(matrix[rows - 2][cols - 2])
            block.append(matrix[rows - 2][cols - 1])
            block.append(matrix[rows - 1][cols - 2])
            block.append(matrix[rows - 1][cols - 1])

    connections["blocks"] = block
    return connections


if __name__ == '__main__':
    import numpy as np

    a = b = 9
    matrix = np.arange(1, a * b + 1).reshape((a, b))
    rows = np.random.choice(a=np.arange(a), size=[])
    cols = np.random.choice(a=np.arange(b), size=[])

    print(rows, cols, whatToConnect(matrix, rows, cols))
    print(matrix)
