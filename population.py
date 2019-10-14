import igraph
import numpy as np

def create_population(population_size, counter, user_class):
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
    pop.add_vertex(name=next(counter),
                   parent=-1,
                   frequency=1.0,
                   max_frequency=1.0,
                   genotype=user_class())
    pop.add_vertex(name=next(counter),
                   parent=-1,
                   frequency=1.0,
                   max_frequency=1.0,
                   genotype=user_class())
    return pop

def get_fitnesses(population):
    """Use fitness function of each genotype to set fitness in each vertex"""
    population.vs['fitness'] = [genotype.fitness() for genotype in population.vs['genotype']]
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


def mutate(population, population_size, mutation_rate, counter):
    """Perform mutations on each genotype"""
    assert mutation_rate >= 0 and mutation_rate <= 1
    abundances = [freq * population_size for freq in population.vs['frequency']]
    num_mutants = np.random.binomial(n= abundances,
                                     p=1 - np.exp(-mutation_rate))
    population.vs['frequency'] = population.vs['frequency'] - (num_mutants / population_size)
    r = num_mutants
    k = 1
    while any(r > 0):
