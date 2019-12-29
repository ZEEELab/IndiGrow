import igraph
import numpy as np
import random
import inspect
import itertools
from numpy.random import binomial as nbinom
from copy import deepcopy
from scipy.special import gammainc as gamma
from numpy import subtract as nsubtract
from numpy import nonzero as nnonzero
from six.moves import range as srange
from backports.functools_lru_cache import lru_cache


def __eq__(self, other):
    """ 
    Unordered maps & sets require an equality operator on top of a hash, so this 
    allows us to compare the equality of genotype classes.
    """
    memberVariables = dir(self)
    memberVariables = list(filter(lambda x: not (x[0] == '_' and x[-1] == '_'), memberVariables))
    for var in memberVariables:
        if getattr(self, var) != getattr(self, var):
            return False
    return True

def __hash__(self):
    """ 
    This is a hashing function designed to hash a whole class, lets us hash a genotype class.
    """
    memberVariables = dir(self)
    memberVariables = list(filter(lambda x: not (x[0] == '_' and x[-1] == '_'), memberVariables))
    tup = tuple((key, getattr(self, key)) for key in memberVariables)
    return hash(tup)


def __mutate__(self):
    """ 
    If for some reason we are given a neighborhood function but not a mutate function,
    we can just randomly select a genotype from the neighborhood.
    """
    return random.choice(self.__mutational_neighborhood__())


class IndiGrow:
    """ 
    This is a class for easily creating and running individual-based lineage simulations.
    """
    def __init__(self, population_size, mutation_rate, genotype=None, environment=None):
        self.pop_map = dict()
        self.fitness_map = dict()
        if not genotype:
            raise RuntimeError('No valid genotype class given')
        self.genotype = genotype
        self.environment = environment() if environment else None
        if self.environment:
            self.environment.__IndiGrow__ = self
        self.population = igraph.Graph(directed=True,
                        graph_attrs={ 'population_size': population_size,
                                      'generations': 0},
                        vertex_attrs={  'name': None,
                                        'parent': None,
                                        'first_seen': None,
                                        'last_seen': None,
                                        'frequency': 0,
                                        'max_frequency': 0,
                                        'genotype': None,
                                        'fitness': 0,
                                        'num_mutations': 0,
                                        'dirty_flag': 0})
        self.population_size = population_size
        self.counter = itertools.count(0)
        self.mutation_rate = mutation_rate
        self.create_population()

    def neighborhood_distribution(self, num_mutant, size):
        """ 
        Randomly distributes num_mutants (an integer) across an array of size "size."
        Example: Distributing 5 mutations across 3 genotypes (size=3) we may see [2,1,2].
        """
        distribution = []
        for _ in range(size - 1):
            val = np.random.randint(0, num_mutant)
            distribution.append(val)
            num_mutant -= val
        distribution.append(num_mutant)
        random.shuffle(distribution)
        return distribution

    def create_population(self):
        """
        Initalization of population with user's class.
        """
        instance = self.genotype()
        instance.__class__.__eq__ = __eq__
        instance.__class__.__hash__ = __hash__
        if '__mutate__' not in dir(instance) and '__mutational_neighborhood__' not in dir(instance):
            raise RuntimeError('No valid __mutate__ or __mutational_neighborhood__ functions given')
        if '__mutate__' not in dir(instance):
            instance.__class__.__mutate__ = __mutate__

        current_counter = next(self.counter)
        self.population.add_vertex(name=current_counter,
                    parent=-1,
                    frequency=1.0,
                    max_frequency=1.0,
                    genotype=instance,
                    num_mutations=0,
                    dirty_flag=1)
        self.pop_map[instance] = self.population.vs.find(name=current_counter)


    def get_fitnesses(self):
        """
        Use fitness function of each genotype to set fitness in each vertex
        """
        # check which nodes have been marked "dirty" meaning their fitness may need to be set
        dirty_subset = self.population.vs.select(dirty_flag=1)
        for vertex in dirty_subset:
            vertex['fitness'] = vertex['genotype'].__fitness__()
            vertex['dirty_flag'] = 0


    def reproduce(self):
        """
        Fill the population using fitness-proportional selection.
        """
        fitnesses = np.array(self.population.vs['fitness'])
        abundances = np.array(self.population.vs['frequency']) * self.population_size
        ab_fit = fitnesses * abundances
        ab_fit_total = ab_fit.sum()
        # use a multinomial distribution to calculate the new frequencies
        self.population.vs['frequency'] = np.random.multinomial(n=self.population_size,
                                                                pvals=ab_fit / ab_fit_total,
                                                                size=1)[0] / self.population_size
        # renormalize all frequencies
        self.population.vs['frequency'] = np.array(self.population.vs['frequency']) / sum(self.population.vs['frequency'])


    def mutate(self, mutation_rate):
        """
        Perform mutations on each genotype.
        """
        assert mutation_rate >= 0 and mutation_rate <= 1
        abundances = [freq * self.population_size for freq in self.population.vs['frequency']]
        num_mutants = nbinom(n= abundances,
                            p=1 - np.exp(-mutation_rate))

        self.population.vs['frequency'] = self.population.vs['frequency'] - (num_mutants / self.population_size)

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
                if k == 1 and '__mutational_neighborhood__' in dir(self.population.vs[0]['genotype']):
                    # get a list of genotypes that are 1 mutation away from the current genotype
                    mutational_neighborhood = self.population.vs[name]['genotype'].__mutational_neighborhood__()
                    # randomly distribute num_mutant amount a list of size=mutational_neighborhood
                    distribution = self.neighborhood_distribution(num_mutant, len(mutational_neighborhood))
                    for dist_index in nnonzero(distribution):
                        dist_index = dist_index[0]
                        mutant_genotype = mutational_neighborhood[dist_index]
                        mutant_count = distribution[dist_index]
                        if mutant_genotype in self.pop_map:
                            self.pop_map[mutant_genotype]['frequency'] += mutant_count / self.population_size
                        else:
                            current_counter = next(self.counter)
                            self.population.add_vertex(name=current_counter,
                                                parent=self.population.vs[name]['name'],
                                                frequency=mutant_count/self.population_size,
                                                max_frequency=mutant_count/self.population_size,
                                                genotype=mutant_genotype,
                                                num_mutations=k,
                                                dirty_flag=1)
                            self.pop_map[mutant_genotype] = self.population.vs.find(name=current_counter)
                # if no mutational neighborhood function or k > 1, just call num_mutant mutations
                else:
                    for _ in range(num_mutant):
                        mutant_genotype = deepcopy(self.population.vs[name]['genotype'])
                        # do k mutations on the genotype to get the new mutant
                        for _ in range(k):
                            mutant_genotype.__mutate__()
                        # if this is not a new genotype, update the frequency
                        if mutant_genotype in self.pop_map:
                            self.pop_map[mutant_genotype]['frequency'] += 1 / self.population_size
                        # if it is new, add it to the 
                        else:
                            current_counter = next(self.counter)
                            self.population.add_vertex(name=current_counter,
                                                    parent=self.population.vs[name]['name'],
                                                    frequency=1/self.population_size,
                                                    max_frequency=1/self.population_size,
                                                    genotype=mutant_genotype,
                                                    num_mutations=k,
                                                    dirty_flag=1)
                            self.pop_map[mutant_genotype] = self.population.vs.find(name=current_counter)

            k += 1
            num_mutants = new_num_mutants


    def group_by_attributes(self, attributes):
        """
        Returns a list of lists - each sublist contains all nodes in the graph whose genotype
        contain matching all attributes in the attribute list.
        """
        groups = []
        # put each genotype/state into a subgroup
        for node in self.population.vs():
            include = False
            # check which subgroup this genotype might belong to
            for group in groups:
                # list of class attributes for the subgroup member and the new genotype we want to
                # potentialy add to this subgroup
                member_attr = group[0]['genotype'].__dict__
                node_attr = node['genotype'].__dict__
                # compare all attributes to make sure they match
                for attr in attributes:
                    # if the attributes don't match this genotype cannot be part of the subgroup
                    if member_attr[attr] != node_attr[attr]:
                        include = False
                        break
                    else:
                        include = True
                # add the genotype to this subgroup
                if include:
                    group.append(node)
                    break
            # if the genotype didn't fit into any subgroups, create a new subgroup
            if not include:
                groups.append([node])
        
        return groups

    def find_all_attributes(self, attributes):
        """
        Make a list of all nodes in our population who's attributes match the given list of
        attributes. Attributes should be given as an unordered map with the key being the member
        variable and the values matching.
        Example:
        attributes = {
                        'bitstring' : 5,
                        'landscape_type' : 'nk',
                        ...
                     }
        """
        nodes = []
        # go through all nodes and find the ones whose attributes match the given ones
        for node in self.population.vs():
            # assume the node has all the proper matching attributes
            nodes.append(node)
            node_attr = node['genotype'].__dict__
            for attr in attributes:
                if attributes[attr] != node_attr[attr]:
                    # if we find that we don't have a match, remove the node from the list
                    # and break out - insert and delete are both O(1) operations so this is cheap
                    nodes.pop()
                    break
        return nodes

    def transfer_state(self, genotype, state_changes, proportion_change):
        """
        Change the frequency of the node associated with genotype and the node associated with
        all the state changes specified as a dictionary based on the proportion given as an arg.
        Example: genotype has member variable "state" which is an int, let's say it's currently 0. 
        state_changes = {'state' : 1}
        proportion_change = .5
        This will 'transfer' .5 of the frequency of the genotype with a state of 0 to the 
        same genotype but with a state of 1. If the frequency of the original genotype is .3 and the
        frequency of the recipient is .1 then after the transfer the original (state=0) will have 
        a frequency of .15 and the new organism (state=1) will have a frequency of .25
        """
        genotype_copy = deepcopy(genotype)
        # change each member variable in the state
        for change in state_changes:
            genotype_copy.__dict__[change] = state_changes[change]

        # find the genotype we are updating in our map
        genotype_node = self.pop_map[genotype]

        # if the copy is not already in the map we need to add it
        if genotype_copy not in self.pop_map:
            current_counter = next(self.counter)
            self.population.add_vertex(name=current_counter,
                                       parent=genotype_node['parent'],
                                       frequency=0,
                                       max_frequency=0,
                                       genotype=genotype_copy,
                                       num_mutations=0,
                                       dirty_flag=1)
            self.pop_map[genotype_copy] = self.population.vs.find(name=current_counter)
        
        # find the change to the frequency, will depend on current frequency and change in proportion
        frequency_change = self.pop_map[genotype]['frequency'] * proportion_change
        # update the original and transfer genotypes' frequencies
        self.pop_map[genotype]['frequency'] -= frequency_change
        self.pop_map[genotype_copy]['frequency'] += frequency_change


    def timestep(self, step):
        """
        Do all the operations associated with a timestep. If the user gave an enviornment we need
        to call their update function, then update all of the fitnesses, then reproduce, then
        mutate.
        """
        if self.environment:
            self.environment.__update__()
        self.get_fitnesses()
        self.reproduce()
        self.mutate(self.mutation_rate)
