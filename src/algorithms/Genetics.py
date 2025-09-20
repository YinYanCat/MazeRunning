import random

from src.algorithms.Individual import Individual

def geneticAlgorithm(individuals: list[Individual]):
    fitness = [individual.fitness() for individual in individuals]
    while 0 not in fitness:
        new_individuals = []
        for i in range(len(individuals)):
            x = choice(individuals)
            y = choice(individuals)
            child = x.pointCross(y)
            if 1 == random.randint(0,1): 
                child.mutate()
            new_individuals.append(child)
    fittest = individuals[0]
    for individual in individuals:
        if individual.fitness() < fittest.fitness():
            fittest = individual
    return fittest

def choice(individuals) -> Individual:
    pass