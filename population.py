import igraph
import numpy as np
from copy import deepcopy

def __eq__(self, other):
    memberVariables = dir(self)
    memberVariables = list(filter(lambda x: not (x[0] == '_' and x[-1] == '_'), memberVariables))
    for var in memberVariables:
        if getattr(self, var) != getattr(self, var):
            return False
    return True

def __hash__(self):
    memberVariables = dir(self)
    memberVariables = list(filter(lambda x: not (x[0] == '_' and x[-1] == '_'), memberVariables))
    tup = tuple((key, getattr(self, key)) for key in memberVariables)
    return hash(tup)

def create_population(population_size, counter, user_class, pop_map):
    pop = igraph.Graph(directed=True,
                       graph_attrs={'population_size': population_size,
                                    'generations': 0},
                       vertex_attrs={'name': None,
                                     'parent': None,
                                     'first_seen': None,
                                     'last_seen': None,
                                     'frequency': 0,
                                     'max_frequency': 0,
                                     'genotype': None,
                                     'fitness': 0})
    instance = user_class()
    instance.__class__.__eq__ = __eq__
    instance.__class__.__hash__ = __hash__

    current_counter = next(counter)
    pop.add_vertex(name=current_counter,
                   parent=-1,
                   frequency=1.0,
                   max_frequency=1.0,
                   genotype=instance)
    pop_map[instance] = pop.vs.find(name=current_counter)

    return pop

def get_fitnesses(population):
    """Use fitness function of each genotype to set fitness in each vertex"""
    population.vs['fitness'] = [genotype.__fitness__() for genotype in population.vs['genotype']]
    return population

def reproduce(population, population_size):
    """Fill the population using fitness-proportional selection"""

    fitnesses = np.array(population.vs['fitness'])
    abundances = np.array(population.vs['frequency']) * population_size
    ab_fit = fitnesses * abundances
    ab_fit_total = ab_fit.sum()
    # use a multinomial distribution to calculate the new frequencies
    population.vs['frequency'] = np.random.multinomial(n=population_size,
                                                       pvals=ab_fit / ab_fit_total,
                                                       size=1)[0] / population_size
                                                  
    return population


def mutate(population, population_size, mutation_rate, counter, pop_map):
    """Perform mutations on each genotype"""
    assert mutation_rate >= 0 and mutation_rate <= 1
    abundances = [freq * population_size for freq in population.vs['frequency']]
    num_mutants = np.random.binomial(n= abundances,
                                     p=1 - np.exp(-mutation_rate))
    population.vs['frequency'] = population.vs['frequency'] - (num_mutants / population_size)
    mutants = []
    for i, num_mutant in enumerate(num_mutants):
        for _ in range(num_mutant):
            mutants.append((deepcopy(population.vs['genotype'][i]), population.vs['name'][i]))
        
    for mutant in mutants:
        mutant_genotype = mutant[0]
        parent = mutant[1]
        mutant_genotype.__mutate__()
        if mutant_genotype in pop_map:
            pop_map[mutant_genotype]['frequency'] += 1/ population_size
        else:
            current_counter = next(counter)
            population.add_vertex(name=current_counter,
                                    parent=mutant[1],
                                      frequency=1 / population_size,
                                      max_frequency=1 / population_size,
                                      genotype=mutant_genotype)
            pop_map[mutant_genotype] = population.vs.find(name=current_counter)
    return population

