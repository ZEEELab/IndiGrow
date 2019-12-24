from user_classes.infectionclass import infectionclass
from user_environments.infectionenvironment import infectionenvironment
from IndiGrow import IndiGrow
import itertools
import random
import numpy

random.seed(13221)
numpy.random.seed(12137)

# genotype_counter = itertools.count(0)
population_size = 10E7
mutation_rate = 10E-4


test = IndiGrow(population_size, genotype_counter)
test.create_population(nkclass)
for i in range(50000):
    test.get_fitnesses()
    if i % 1000 == 0:
      print(max(test.population.vs['fitness']))
    test.reproduce()
    test.mutate(mutation_rate)
