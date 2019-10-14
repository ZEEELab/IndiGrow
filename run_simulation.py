from myclass import nkclass
from population import create_population
from population import get_fitnesses
from population import reproduce
from population import mutate
import itertools

genotype_counter = itertools.count(0)
population_size = 100
mutation_rate = .05

pop = create_population(population_size, genotype_counter, nkclass)
pop = get_fitnesses(pop)
pop = reproduce(pop, population_size)
mutate(pop, population_size, mutation_rate, genotype_counter)
#print(pop.vs['genotype'][0].fitness())