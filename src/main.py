import time

import pygame

from src.algorithms.Individual import *
from src.algorithms.Genetics import *
import copy
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual


def main():
    maze = Maze(size=30,walkback_attempts=10,moves=900)
    visual_maze = copy.deepcopy(maze)
    printed = False

    visual = Visual(10)
    visual.set_maze(visual_maze)

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visual.draw()


        if not printed:
            search_maze = copy.deepcopy(maze)
            distance_maze = copy.deepcopy(maze)
            search, history = breadthFirstSearch(search_maze)
            distance_goal = distance_matrix(distance_maze)
            toview= history
            for i in range(len(toview)):
                x, y = toview[i]
                print(x,y)
                if i != 0:
                    visual_maze.visit_cell(x,y)
                visual.draw()
                #time.sleep(0.01)
            printed = True
        #distances_to_goal(maze)

    pygame.quit()

if __name__ =="__main__":
    main()