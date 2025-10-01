import time

import pygame

from src.algorithms.Individual import *
from src.algorithms.Genetics import *
import copy
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual

def main():

    print('\n-------------\nPROGRAM KEYS:\n-------------')
    print('[B] BFS Algorithm\n[N] BFS Original Path and Maze\n[M] BFS Best Path and Maze Found')
    print('[G] Genetic Algorithm')

    maze_size = 30
    maze_walk_att = 200
    maze_moves = 900
    maze_fake_goal = 30
    maze_move_wall = 5
    maze_switch = 3

    maze = Maze(maze_size,maze_walk_att,maze_moves,maze_fake_goal,maze_move_wall)
    bfs_maze = copy.deepcopy(maze)
    BFS_Search = False
    first_bfs = None
    best_bfs = None
    best_bfs_maze = None

    gen_maze = copy.deepcopy(maze)
    Gen_Search = False
    distance_maze = copy.deepcopy(maze)
    distance_mat = distance_matrix(distance_maze)

    visual_maze = copy.deepcopy(maze)
    visual = Visual(20)
    visual.set_maze(visual_maze)

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    Gen_Search = False
                    BFS_Search = not BFS_Search
                    if BFS_Search:
                        print('Breadth-first search algorithm [Activated]')
                    else:
                        print('Breadth-first search algorithm [Deactivate]')

                if event.key == pygame.K_n:
                    if first_bfs is not None:
                        print('Original Breadth-first search path')
                        BFS_Search = False
                        visual_maze = copy.deepcopy(maze)
                        draw_path_maze(visual, visual_maze, first_bfs, -6)
                    else:
                        print('ERROR N: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_m:
                    if best_bfs is not None:
                        print('Best Breadth-first search path and maze distribution')
                        BFS_Search = False
                        best_bfs_maze.unsearch_matrix()
                        visual_maze = copy.deepcopy(best_bfs_maze)
                        draw_path_maze(visual, visual_maze, best_bfs, -6)
                    else:
                        print('ERROR M: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_g:
                    Gen_Search = True
                    BFS_Search = False

                if event.key == pygame.K_d:
                    print('Distance Matrix from Goal:')
                    for x in range(maze.size):
                        for y in range(maze.size):
                            print(f"{int(distance_mat[x][y]):02d}", end=" ")
                        print('')
        visual.draw()

        if BFS_Search:
            visual_maze = copy.deepcopy(bfs_maze)
            visual.set_maze(visual_maze)
            search, history = breadthFirstSearch(bfs_maze)
            toview = search
            value = -6
            if len(search) == 0:
                toview = history
                value = -7
            elif best_bfs is None or len(search) < len(best_bfs):
                best_bfs = copy.deepcopy(search)
                best_bfs_maze = copy.deepcopy(bfs_maze)
            if first_bfs is None:
                first_bfs = copy.deepcopy(search)
            draw_path_maze(visual, visual_maze, toview, value)
            time.sleep(1)
            bfs_maze.unsearch_matrix()
            bfs_maze.switch_walls(maze_switch)


        elif Gen_Search:
            search_maze = copy.deepcopy(gen_maze)
            history = geneticAlgorithm(maze=search_maze, distance_matrix=distance_mat, max_generations=200,individual_count=10, until_finds=True)
            for i in range(len(history)):
                x, y = history[i]
                if i != 0:
                    visual_maze.visit_cell(x, y, -6)
                visual.draw()
            #time.sleep(3)
            visual_maze = copy.deepcopy(gen_maze)
            visual.set_maze(visual_maze)


    pygame.quit()

def draw_path_maze(visual, maze, path, color):
    visual.set_maze(maze)
    for i in range(len(path)):
        x, y = path[i]
        if i != 0:
            maze.visit_cell(x, y, color)
        visual.draw()

if __name__ =="__main__":
    main()