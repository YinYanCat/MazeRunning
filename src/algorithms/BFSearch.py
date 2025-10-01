from src.maze.Maze import Maze
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.value = 0
        self.children = []

def breadthFirstSearch(maze):
    matrix = maze.get_matrix()
    start = maze.get_start()
    history = []
    end = None
    queue = [start]

    while end is None:
        parent = queue[0]
        history.append(parent)
        for child in maze.cell_neighbours(parent[0], parent[1]):
            if 1 > matrix[child[0]][child[1]] > -3:   # Walkable Cell
                matrix[child[0]][child[1]] = matrix[parent[0]][parent[1]] + 1
                queue.append(child)
            elif matrix[child[0]][child[1]] == -3:
                matrix[child[0]][child[1]] = matrix[parent[0]][parent[1]] + 1
                queue = [child]
                end = child
                break
        queue.pop(0)

    route = get_route(maze, matrix, end)
    return route, history

def distance_matrix(maze):
    matrix = maze.get_matrix()
    start = maze.get_end()
    queue = [start]
    while len(queue) != 0:
        parent = queue[0]
        for child in maze.cell_neighbours(parent[0], parent[1]):
            if matrix[child[0]][child[1]] == 0:
                matrix[child[0]][child[1]] = matrix[parent[0]][parent[1]] + 1
                queue.append(child)
        queue.pop(0)
    return matrix

def get_route(maze, matrix, end):
    reverse_route = []
    route = []
    cycle = True
    while cycle:
        for neighbour in maze.cell_neighbours(end[0], end[1]):
            if matrix[neighbour[0]][neighbour[1]] == (matrix[end[0]][end[1]]) - 1:
                end = neighbour
                reverse_route.append(end)
                if matrix[neighbour[0]][neighbour[1]] == 1:
                    cycle = False
                break
    for i in range(len(reverse_route)):
        route.append(reverse_route[len(reverse_route) - i - 1])
    return route

