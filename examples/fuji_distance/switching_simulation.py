from switching_class import switching_class
from switching_event import switching_event, print_event
from IndiGrow.IndiGrow import IndiGrow
import random
import numpy


if __name__ == '__main__':
    random.seed(182)
    numpy.random.seed(1277)

    population_size = 10E7
    mutation_rate = 10E-4

    test = IndiGrow(population_size=10E7, mutation_rate=mutation_rate)

    test.add_genotype(genotype=switching_class(n=4), frequency=1)
    test.add_event(event_class=switching_event, trigger_every=10)
    test.add_event(event_class=print_event, trigger_every=1)
    

    

    for i in range(300):
        test.timestep()
