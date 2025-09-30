from src.maze.Maze import Maze


class Node:
    def __init__(self, data):
        self.data = data
        self.value = 0
        self.children = []

def breadthFirstSearch(maze):

    old_matrix = maze.get_matrix()
    matrix = []
    size = maze.get_size()
    start = [None, None]

    for x in range(size):
        matrix.append([])
        for y in range(size):
            if old_matrix[x][y] > 0:
                matrix[x].append(0)
            elif old_matrix[x][y] == -2:
                matrix[x].append(1)
                start[0] = x
                start[1] = y
            else:
                matrix[x].append(old_matrix[x][y] - 1)

    root = start
    end = None
    queue = [root]

    while len(queue) != 0:
        parent = queue[0]
        for child in maze.cell_neighbours(parent[0], parent[1]):
            if matrix[child[0]][child[1]] == 0:
                matrix[child[0]][child[1]] = matrix[parent[0]][parent[1]] + 1
                queue.append(child)
            elif matrix[child[0]][child[1]] == -2:
                matrix[child[0]][child[1]] = matrix[parent[0]][parent[1]] + 1
                queue = [child]
                end = child
                break
        queue.pop(0)

    route = []
    cycle = True

    while cycle:
        for neighbour in maze.cell_neighbours(end[0], end[1]):
            if matrix[neighbour[0]][neighbour[1]] == (matrix[end[0]][end[1]])-1:
                end = neighbour
                route.append(end)
                if matrix[neighbour[0]][neighbour[1]] == 1:
                    cycle = False
                break

    return route