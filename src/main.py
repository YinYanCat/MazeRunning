import time

import pygame

from src.algorithms.Individual import *
from src.algorithms.Genetics import *
import copy
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual

def main():
    maze = Maze(size=30,walkback_attempts=200,moves=900,fake_goal=30,move_walls=5)

    bfs_maze = copy.deepcopy(maze)
    BFS_Search = False
    gen_maze = copy.deepcopy(maze)
    Gen_Search = False

    visual_maze = copy.deepcopy(maze)
    visual = Visual(30)
    visual.set_maze(visual_maze)

    actual_maze = visual_maze
    loop = False
    search = None
    history = None

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    actual_maze = bfs_maze
                    loop = True
                    BFS_Search = True

                if event.key == pygame.K_n:
                    loop = False
                    first_bfs = copy.deepcopy(maze)
                    search, history = breadthFirstSearch(first_bfs)
                    for i in range(len(search)):
                        x, y = search[i]
                        if i != 0:
                            visual_maze.visit_cell(x, y, -6)
                        visual.draw()

                if event.key == pygame.K_g:
                    actual_maze = gen_maze
                    loop = True
                    Gen_Search = True
                    BFS_Search = False

                if event.key == pygame.K_d:
                    distance_maze = copy.deepcopy(maze)
                    distance_mat = distance_matrix(distance_maze)
                    for x in range(maze.size):
                        for y in range(maze.size):
                            print(int(distance_mat[x][y]), end=' ')
                        print('')
        visual.draw()

        if loop:
            search_maze = copy.deepcopy(actual_maze)
            if BFS_Search:
                search, history = breadthFirstSearch(search_maze)
            elif Gen_Search:
                distance_maze = copy.deepcopy(maze)
                distance_mat = distance_matrix(distance_maze)
                history = geneticAlgorithm(maze=search_maze, distance_matrix=distance_mat, max_generations=200, individual_count=10, until_finds=True)
            toview = history
            value = -6
            #if len(search) == 0:
            #    toview = history
            #    value = -7
            for i in range(len(toview)):
                x, y = toview[i]
                if i != 0:
                    visual_maze.visit_cell(x, y, value)
                visual.draw()
            #time.sleep(3)
            #actual_maze.switch_walls(2)
            visual_maze = copy.deepcopy(actual_maze)
            visual.set_maze(visual_maze)

    pygame.quit()

if __name__ =="__main__":
    main()