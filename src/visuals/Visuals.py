from src.maze.Maze import Maze
import pygame

class Visual:

    def __init__(self, cell_size:int = 5):
        pygame.init()
        pygame.display.set_caption("MazeRunning")
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.cell_size = cell_size
        self.maze_size = 0
        self.maze = None
        self.screen = None

    def set_maze(self, maze:Maze):
        self.maze = maze
        self.maze_size = self.maze.get_size()
        self.update()

    def set_cell_size(self, cell_size:int):
        self.cell_size = cell_size
        self.update()

    def fit_screen(self):
        pass

    def update(self):
        self.screen = pygame.display.set_mode((self.maze_size * self.cell_size, self.maze_size * self.cell_size))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen, self.cell_size)
        pygame.display.flip()
