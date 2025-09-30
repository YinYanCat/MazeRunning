import pygame

from src.algorithms.Individual import *
from src.algorithms.Genetics import *
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual


def main():
    maze = Maze()
    printed = False

    visual = Visual(50)
    visual.set_maze(maze)

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visual.draw()


        if not printed:
            search = breadthFirstSearch(maze)
            for i in range(len(search)):
                print(search[len(search)-i-1])
            printed = True

    pygame.quit()

if __name__ =="__main__":
    main()