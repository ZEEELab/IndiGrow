from myclass import nkclass
from population import IndiGrow
import itertools
import random
import numpy

random.seed(101)
numpy.random.seed(110)

genotype_counter = itertools.count(0)
population_size = 10E5
mutation_rate = 10E-6
maxf = 0


test = IndiGrow(population_size, genotype_counter)
test.create_population(nkclass)
for i in range(50000):
    test.get_fitnesses()
    if i % 1000 == 0:
      print(max(test.population.vs['fitness']))
    test.reproduce()
    test.mutate(mutation_rate)
