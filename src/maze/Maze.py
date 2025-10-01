import random

import numpy as np
import pygame


class Maze:
    def __init__(self, size=20, walkback_attempts=0, moves=400, fake_goal=30, move_walls=5):
        self.goal_y = None
        self.goal_x = None
        self.start = [None, None]
        self.moves = moves
        self.walkback_attempts =  walkback_attempts
        self.prob_fake_goal = fake_goal
        self.prob_move_walls = move_walls
        self.wall_list = []
        self.size = size
        self.matrix = np.zeros((self.size,self.size))
        self.create_maze()

    def get_size(self):
        return self.size

    def get_start(self):
        return self.start

    def get_end(self):
        return [self.goal_x, self.goal_y]

    def get_matrix(self):
        return self.matrix

    def moveObstacles(self):
        pass

    def next_expandable(self, cursor_x, cursor_y):
        neighbours = self.cell_neighbours(cursor_x,cursor_y)
        candidates = [(x,y) for x,y in neighbours if self.matrix[x][y]>0]
        if not candidates:
            return None, None
        min_visits = min(self.matrix[x][y] for x, y in candidates)
        best = [(x,y) for x,y in candidates if self.matrix[x][y] == min_visits]

        return random.choice(best)

    def cell_neighbours(self, cursor_x, cursor_y):
        neighbours = []
        if cursor_x < self.size - 1:
            neighbours.append((cursor_x + 1, cursor_y))
        if cursor_x > 0:
            neighbours.append((cursor_x - 1, cursor_y))
        if cursor_y < self.size -1:
            neighbours.append((cursor_x, cursor_y + 1))
        if cursor_y > 0:
            neighbours.append((cursor_x, cursor_y - 1))

        return neighbours

    def cell_corners(self, cursor_x, cursor_y):
        corners = []
        if cursor_x < self.size - 1 and cursor_y < self.size - 1:
            corners.append((cursor_x + 1, cursor_y + 1))
        if cursor_x > 0 and cursor_y > 0:
            corners.append((cursor_x - 1, cursor_y - 1))
        if cursor_y < self.size - 1 and cursor_x > 0:
            corners.append((cursor_x - 1, cursor_y + 1))
        if cursor_y > 0 and cursor_x < self.size - 1:
            corners.append((cursor_x + 1, cursor_y - 1))

        return corners

    def expand(self, cursor_x, cursor_y):
        possible_moves = self.cell_neighbours(cursor_x, cursor_y)
        possible_moves = [(x, y) for x, y in possible_moves if self.matrix[x][y] == 0 and self.is_carveable(cursor_x, cursor_y, x, y)]
        if possible_moves:
            cursor_x, cursor_y = random.choice(possible_moves)
            self.matrix[cursor_x][cursor_y] += 1
        return cursor_x, cursor_y

    def create_maze(self):
        self.goal_x,self.goal_y = np.random.randint(0, self.size,size=2)
        self.matrix[self.goal_x][self.goal_y] = -1
        cursor_x, cursor_y = self.goal_x, self.goal_y
        moves = self.moves

        while moves > 0:
            attempts = 0
            while self.expand(cursor_x, cursor_y) == (cursor_x, cursor_y): # and check not stuck:
                next_cell = self.next_expandable(cursor_x, cursor_y)
                if next_cell == (None,None):
                    continue
                self.matrix[next_cell] += 1
                cursor_x,cursor_y = next_cell
                attempts += 1
                if attempts >= self.walkback_attempts:
                    break
            moves -= 1
        self.matrix[cursor_x][cursor_y] = -2
        self.normalize_maze()

    def normalize_maze(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.matrix[x][y] > 0:
                    self.matrix[x][y] = 0       # Path
                    if np.random.randint(0, self.prob_fake_goal) == 0:
                        self.matrix[x][y] = -2  # Fake Goal
                    if np.random.randint(0, self.prob_move_walls) == 0:
                        self.matrix[x][y] = -1  # Path (Can be Wall)
                        self.wall_list.append([x, y])
                elif self.matrix[x][y] == -2:
                    self.start = [x, y]
                    self.matrix[x][y] = 1       # Start
                elif self.matrix[x][y] == -1:
                    self.matrix[x][y] = -3      # Goal
                else:
                    self.matrix[x][y] = -4      # Wall
                    if np.random.randint(0, self.prob_move_walls) == 0:
                        self.matrix[x][y] = -5  # Wall (Can be Path)
                        self.wall_list.append([x, y])

    def switch_walls(self, probability):
        for i in range(len(self.wall_list)):
            if self.matrix[self.wall_list[i][0]][self.wall_list[i][1]] == -1:
                if np.random.randint(0, probability) == 1:
                    self.matrix[self.wall_list[i][0]][self.wall_list[i][1]] = -5
            else:
                self.matrix[self.wall_list[i][0]][self.wall_list[i][1]] = -1


    def is_carveable(self, cursor_x, cursor_y, carve_x, carve_y):
        neigbours = self.cell_neighbours(carve_x,carve_y) + self.cell_corners(carve_x, carve_y)

        if (cursor_x,cursor_y) not in neigbours:
            return False
        neigbours.remove((cursor_x, cursor_y))
        dx, dy = carve_x - cursor_x, carve_y - cursor_y
        if (dx, dy) == (0, 1) or (dx, dy) == (0, -1):
            neigbours = [(x,y) for x,y in neigbours if (x,y) not in [(cursor_x - 1, cursor_y),(cursor_x + 1, cursor_y)]]
        if (dx, dy) == (1, 0) or (dx, dy) == (-1, 0):
            neigbours = [(x, y) for x, y in neigbours if (x, y) not in [(cursor_x, cursor_y - 1), (cursor_x, cursor_y + 1)]]

        for x,y in neigbours:
            if self.matrix[x][y] > 0:
                return False
        return True

    def visit_cell(self, x, y, value):
        self.matrix[x][y] = value

    def draw(self, screen, cell_size):
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(y*cell_size, x*cell_size, cell_size, cell_size)
                if self.matrix[x][y] == 0:      # Path
                    color = (230,230,230)
                elif self.matrix[x][y] == -1:   # Path (Can be Wall)
                    color = (230,230,230)
                elif self.matrix[x][y] == -2:   # Fake Goal
                    color = (255,20,20)
                elif self.matrix[x][y] == -3:   # Goal
                    color = (0,255,0)
                elif self.matrix[x][y] == -4:   # Wall
                    color = (0,0,0)
                elif self.matrix[x][y] == -5:   # Wall (Can be Path)
                    color = (0,0,0)
                elif self.matrix[x][y] == -6:   # Visits
                    color = (255,255,0)
                elif self.matrix[x][y] == -7:   # Fill
                    color = (255,150,50)
                else:                           # Start (1)
                    color = (0,0,255)

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (50,50,50), rect, 1)  # borde


