from nk_fuji_environment import nk_fuji_environment
from nk_fuji_class import nk_fuji_class
from IndiGrow.IndiGrow import IndiGrow
import random
import numpy


if __name__ == '__main__':
    random.seed(182)
    numpy.random.seed(1277)

    population_size = 10E7
    mutation_rate = 10E-4

    test = IndiGrow(population_size=10E7, environment=nk_fuji_environment)

    test.add_genotype(genotype=nk_fuji_class(), frequency=1)
    

    for i in range(300):
        test.timestep()
