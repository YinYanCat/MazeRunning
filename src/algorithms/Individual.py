import random

class Individual:

    def __init__(self, x, y):
        self.action_stack = None
        self.moves = ['U','D','L','R']
        self.start_x, self.start_y = x, y
        self.x, self.y = x, y
        self.gen = [random.choice(self.moves)]
        self.fitness_evaluation = []
        self.history = []
        self.wall_matrix = []
        self.max_fitness = None

    def setGenes(self, gen):
        self.gen = gen

    def getFitness(self):
        return self.fitness_evaluation

    def getMaxFitness(self):
        return self.max_fitness

    def pointCross(self, individual):
        cross_point = random.randint(0,len(self.gen)-1)
        crossed_genes = self.gen[:cross_point] + individual.getGenes()[cross_point:]
        new_individual = Individual(self.start_x, self.start_y)
        new_individual.setGenes(crossed_genes)
        return new_individual

    def fitnessCross(self, individual):
        if len(self.gen) > 0 and len(individual.getGenes()) > 0:
            if self.max_fitness < individual.getMaxFitness():
                strong_fitness = self.fitness_evaluation
                strong_genes = self.gen
                weak_genes = individual.getGenes()
            else:
                weak_genes = self.gen
                strong_fitness = individual.getFitness()
                strong_genes = individual.getGenes()

            max_fitness = 0
            for i in range(1,len(strong_fitness)):
                if strong_fitness[max_fitness] < strong_fitness[i]:
                    break
                else:
                    max_fitness = i
            crossed_genes = strong_genes[:max_fitness] + weak_genes[max_fitness:]
            new_individual = Individual(self.start_x, self.start_y)
            new_individual.setGenes(crossed_genes)
            return new_individual


    def mutate(self):
        self.gen[random.randint(0,len(self.gen)-1)] = random.choice(self.moves)

    def grow(self, size):
        for i in range (size):
            self.gen.append(random.choice(self.moves))

    def getGenes(self):
        return self.gen

    def fitness(self, x, y, distance_matrix):
        return distance_matrix[x][y] / len(distance_matrix[0])

    def run(self, maze, distance_matrix, saves_maze_changes, probability=None):
        if probability is None:
            probability = [1, 1]

        self.action_stack = []
        penalty = 0

        matrix = maze.get_matrix()
        size = maze.get_size()
        self.x, self.y = self.start_x, self.start_y
        self.history = [(self.x, self.y)]

        # Fitness inicial
        initial_fitness = self.fitness(self.x, self.y, distance_matrix)
        self.fitness_evaluation = [initial_fitness]
        self.max_fitness = initial_fitness

        opposites = {'U':'D', 'L':'R', 'R':'L', 'D':'U'}

        for move in self.gen:

            penalty = 0
            maze.switch_walls(probability[0], probability[1], self.x, self.y)
            next_x, next_y = self.x, self.y

            if move == 'U':
                next_y -= 1
            elif move == 'D':
                next_y += 1
            elif move == 'L':
                next_x -= 1
            elif move == 'R':
                next_x += 1

            # Manejo de retrocesos
            if self.action_stack and self.action_stack[-1] == opposites[move]:
                penalty += 2
                if len(self.action_stack) > 1:
                    self.action_stack.pop()
                else:
                    self.action_stack.append(move)
            else:
                self.action_stack.append(move)

            # Verificar límites
            if 0 <= next_x < size and 0 <= next_y < size:
                next_cell = matrix[next_x][next_y]

                if next_cell == -3:  # meta
                    self.x, self.y = next_x, next_y
                    self.history.append((self.x, self.y))
                    self.fitness_evaluation.append(0)
                    self.max_fitness = 0
                    break
                elif next_cell in (0, 1, -1):  # camino válido
                    self.x, self.y = next_x, next_y
                elif next_cell == -2:
                    self.x, self.y = next_x, next_y
                    penalty += 10
                else:  # Penalización - golpea pared
                    if next_cell == -5:
                        current_fitness = self.fitness(self.x, self.y, distance_matrix) + penalty + 1
                    else:
                        current_fitness = self.fitness(self.x, self.y, distance_matrix) + penalty + 8
                    self.fitness_evaluation.append(current_fitness)
                    continue
            else:  # fuera de límites
                current_fitness = self.fitness(self.x, self.y, distance_matrix) + penalty + 10
                self.fitness_evaluation.append(current_fitness)
                continue

            # Calcular fitness después de moverse
            current_fitness = self.fitness(self.x, self.y, distance_matrix) + penalty
            self.history.append((self.x, self.y))

            if saves_maze_changes:
                self.wall_matrix.append(maze.get_move_list())

            self.fitness_evaluation.append(current_fitness)

            if current_fitness < self.max_fitness:
                self.max_fitness = current_fitness

    def getHistory(self):
        return self.history

    def getMoveMatrix(self):
        return self.wall_matrix