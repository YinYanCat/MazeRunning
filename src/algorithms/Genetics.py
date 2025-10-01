import random

from src.algorithms.Individual import Individual

def choice(individuals) -> Individual:
    return random.choice(individuals)


def geneticAlgorithm(distance_matrix, maze, max_generations, individual_count=10, until_finds=True):

    generation = 0
    start_x, start_y = maze.get_start()
    individuals = [Individual(start_x,start_y) for i in range(individual_count)]
    while until_finds is True or generation < max_generations:
        if until_finds is False:
            prob_fitness_cross = generation / max_generations / 10
        else:
            prob_fitness_cross = generation / maze.get_size()*maze.get_size() / 10

        for individual in individuals:
            individual.run(maze, distance_matrix)

        if any(individual.getMaxFitness() == 0 for individual in individuals):
            break

        new_individuals = []
        for i in range(len(individuals)):
            x = choice(individuals)
            y = choice(individuals)

            if random.random() < prob_fitness_cross:
                child = x.fitnessCross(y)
            else:
                child = x.pointCross(y)

            if random.randint(0,1) == 1:
                child.mutate()
            child.grow(1)
            child.run(maze = maze, distance_matrix=distance_matrix)
            new_individuals.append(child)

        individuals = new_individuals
        generation += 1

    fittest = individuals[0]
    for individual in individuals:
        if individual.getMaxFitness() < fittest.getMaxFitness():
            fittest = individual

    return fittest.getHistory(), fittest.getMoveMatrix()
