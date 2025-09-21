import pygame

from src.maze.Maze import Maze
from src.algorithms import *
from src.visuals.Visuals import Visual


def main():
    maze = Maze()

    visual = Visual(50)
    visual.set_maze(maze)

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visual.draw()
    pygame.quit()

if __name__ =="__main__":
    main()