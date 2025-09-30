import random

class Individual:
    Moves = ['U','D','L','R']
    def __init__(self):
        self.gen = []
        self.fitness_evaluation = []
        self.fitness = 0

    def pointCross(self, individual):
        cross_point = random.randint(0,len(self.gen)-1)
        crossed_genes = self.gen[:cross_point] + individual.getGenes()[cross_point:]
        return Individual().setGenes(crossed_genes)

    def fitnessCross(self):
        pass

    def mutate(self):
        pass

    def setGenes(self, gen):
        self.gen = gen

    def getGenes(self):
        return self.gen

    def fitness(self, distance_matrix):
        pass

    def run(self, maze):
        pass

