from rps_example.rps_class import rps_class
from rps_example.rps_print_event import rps_print_event
from IndiGrow.IndiGrow import IndiGrow
import random
import numpy


if __name__ == '__main__':
    random.seed(182)
    numpy.random.seed(1277)

    population_size = 10E7
    mutation_rate = 10E-4

    test = IndiGrow(population_size=10E7, mutation_rate=0)

    test.add_genotype(genotype=rps_class('rock'), frequency=98/100)
    test.add_genotype(genotype=rps_class('paper'), frequency=1/100)
    test.add_genotype(genotype=rps_class('scissors'), frequency=1/100)
    test.add_event(event_class=rps_print_event, trigger_every=100)

    for i in range(300):
        test.timestep()
