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

test = IndiGrow(population_size, mutation_rate, genotype=infectionclass, environment=infectionenvironment)
for i in range(500):
    test.timestep(i)
   