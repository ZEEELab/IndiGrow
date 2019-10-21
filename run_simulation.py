from myclass import nkclass
from population import create_population
from population import get_fitnesses
from population import reproduce
from population import mutate
import itertools

genotype_counter = itertools.count(0)
population_size = 1000
mutation_rate = .05
maxf = 0

pop_map = dict()

pop = create_population(population_size, genotype_counter, nkclass, pop_map)
for i in range(1000):
  pop = get_fitnesses(pop)
    # average = 0
    # for fit, freq in zip(pop.vs['fitness'], pop.vs['frequency']):
    #   average += fit * freq
    # print(average, max(pop.vs['fitness']))
    #print(len(pop.vs['frequency']))
  newmax = max(pop.vs['fitness'])
  if (newmax > maxf):
    maxf = newmax
    print(maxf)
  pop = reproduce(pop, population_size)
  pop = mutate(pop, population_size, mutation_rate, genotype_counter, pop_map)
#print(pop.vs['genotype'][0].fitness())