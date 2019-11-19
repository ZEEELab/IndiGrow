import numpy
import networkx as nx
import random

def hamming_dist(n1, n2): 
    x = n1 ^ n2  
    set_bits = 0

    while (x > 0) : 
        set_bits += x & 1
        x >>= 1
    return set_bits

def get_rough_mt_fuji(optimal_genotype, num_bits, cost_of_mismatch, noise_dist, **noise_dist_args):
    #print(noise_dist(**noise_dist_args))
    genotype_graph = nx.Graph(optimal_genotype=optimal_genotype, num_bits=num_bits)
    fitnesses = numpy.zeros(2**num_bits)
    for i in range(0, 2**num_bits):
        distance_to_optimal = hamming_dist(i, optimal_genotype)
        distance_to_unity = hamming_dist(i, 2**num_bits-1)
        fitness = max(1 - cost_of_mismatch * distance_to_optimal + noise_dist(**noise_dist_args), 0.0001)
        

        genotype_graph.add_node(i, 
                                abundance=0,
                                fitness=fitness,
                                genotype_int=i, 
                                distance_to_opt=distance_to_optimal,
                                distance_to_unity=distance_to_unity)

        fitnesses[i] = fitness

    for i in range(0, 2**num_bits):
        for j in range(i, 2**num_bits):
            if hamming_dist(i, j) == 1:  
                genotype_graph.add_edge(i, j)

    return genotype_graph, fitnesses


class fuji:
    def __init__(self):
        graph, fitnesses = get_rough_mt_fuji(1011, 12, .01, numpy.random.exponential, scale=0.0001, size=None)
        print(max(fitnesses))
        self.n = 12
        self.fitnesses = fitnesses

    def fitness(self, genotype):
        return self.fitnesses[genotype]

