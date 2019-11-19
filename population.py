import igraph
import numpy as np
from numpy.random import binomial as nbinom
from copy import deepcopy
from scipy.special import gammainc as gamma
from numpy import subtract as nsubtract
from numpy import nonzero as nnonzero
from six.moves import range as srange
import random


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


def __mutate__(self):
    return random.choice(self.__mutational_neighborhood__())


def neighborhood_distribution(num_mutant, size):
    distribution = []
    for _ in range(size - 1):
        val = np.random.randint(0, num_mutant)
        distribution.append(val)
        num_mutant -= val
    distribution.append(num_mutant)
    random.shuffle(distribution)
    return distribution


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
                                     'fitness': 0,
                                     'num_mutations': 0,
                                     'dirty_flag': 0})
    instance = user_class()
    instance.__class__.__eq__ = __eq__
    instance.__class__.__hash__ = __hash__
    if '__mutate__' not in dir(instance) and '__mutational_neighborhood__' not in dir(instance):
        raise RuntimeError('No valid __mutate__ or __mutational_neighborhood__ functions given')
    if '__mutate__' not in dir(instance):
        instance.__class__.__mutate__ = __mutate__

    current_counter = next(counter)
    pop.add_vertex(name=current_counter,
                   parent=-1,
                   frequency=1.0,
                   max_frequency=1.0,
                   genotype=instance,
                   num_mutations=0,
                   dirty_flag=1)
    pop_map[instance] = pop.vs.find(name=current_counter)

    return pop


def get_fitnesses(population, fitness_map):
    """Use fitness function of each genotype to set fitness in each vertex"""
    dirty_subset = population.vs.select(dirty_flag=1)
    for vertex in dirty_subset:
        vertex['fitness'] = vertex['genotype'].__fitness__()
        vertex['dirty_flag'] = 0
    # print(population.vs['fitness'])
    #population.vs['fitness'] = [genotype.__fitness__() for genotype in population.vs['genotype']]
    # alive_genotype_indexes = nnonzero(population.vs['frequency'])
    # for index in alive_genotype_indexes[0]:
    #     genotype = population.vs[index]['genotype']
    #     if genotype not in fitness_map:
    #         fitness_map[genotype] = genotype.__fitness__()
    #     population.vs[index]['fitness'] = fitness_map[genotype]

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
    num_mutants = nbinom(n= abundances,
                         p=1 - np.exp(-mutation_rate))

    population.vs['frequency'] = population.vs['frequency'] - (num_mutants / population_size)

    k = 1
    while(any(num_mutants > 0)):
        new_num_mutants = nbinom(n=num_mutants,
                                 p=gamma(k+1, mutation_rate)/gamma(k, mutation_rate),
                                 size=len(num_mutants))
        # we want a list of how many mutants will have k mutations for each genotype
        num_k_mutants = nsubtract(num_mutants, new_num_mutants)
        # skip over any count of mutants that is 0
        for name in nnonzero(num_k_mutants):
            if not len(name):
                continue
            name = name[0]
            num_mutant = num_k_mutants[name]
            # if we have a mutational neighborhood function, it will be MUCH faster
            if k == 1 and '__mutational_neighborhood__' in dir(population.vs[0]['genotype']):
                # get a list of genotypes that are 1 mutation away from the current genotype
                mutational_neighborhood = population.vs[name]['genotype'].__mutational_neighborhood__()
                # randomly distribute num_mutant amount a list of size=mutational_neighborhood
                distribution = neighborhood_distribution(num_mutant, len(mutational_neighborhood))
                for dist_index in nnonzero(distribution):
                    dist_index = dist_index[0]
                    mutant_genotype = mutational_neighborhood[dist_index]
                    mutant_count = distribution[dist_index]
                    if mutant_genotype in pop_map:
                        pop_map[mutant_genotype]['frequency'] += mutant_count / population_size
                    else:
                        current_counter = next(counter)
                        population.add_vertex(name=current_counter,
                                              parent=population.vs[name]['name'],
                                              frequency=mutant_count/population_size,
                                              max_frequency=mutant_count/population_size,
                                              genotype=mutant_genotype,
                                              num_mutations=k,
                                              dirty_flag=1)
                        pop_map[mutant_genotype] = population.vs.find(name=current_counter)
            # if no mutational neighborhood function or k > 1, just call num_mutant mutations
            else:
                for _ in range(num_mutant):
                    mutant_genotype = deepcopy(population.vs[name]['genotype'])
                    # do k mutations on the genotype to get the new mutant
                    for _ in range(k):
                        mutant_genotype.__mutate__()
                    # if this is not a new genotype, update the frequency
                    if mutant_genotype in pop_map:
                        pop_map[mutant_genotype]['frequency'] += 1 / population_size
                    # if it is new, add it to the 
                    else:
                        current_counter = next(counter)
                        population.add_vertex(name=current_counter,
                                                parent=population.vs[name]['name'],
                                                frequency=1/population_size,
                                                max_frequency=1/population_size,
                                                genotype=mutant_genotype,
                                                num_mutations=k,
                                                dirty_flag=1)
                        pop_map[mutant_genotype] = population.vs.find(name=current_counter)

        k += 1
        num_mutants = new_num_mutants

    return population

