from user_classes.infectionclass import infectionclass
from user_classes.nk_fuji_class import nk_fuji_class
from user_environments.infectionenvironment import infectionenvironment
from user_environments.nk_fuji_environment import nk_fuji_environment
from IndiGrow import IndiGrow
import itertools
import random
import numpy

random.seed(13221)
numpy.random.seed(12907)

# genotype_counter = itertools.count(0)
population_size = 10E7
mutation_rate = 10E-4

test = IndiGrow(population_size, mutation_rate, genotype=nk_fuji_class, environment=nk_fuji_environment)
for i in range(10000):
    test.timestep()
   