from infectionclass import infectionclass
from infectionenvironment import infectionenvironment
from infectionevent import infection_event_update, infection_event_print
from IndiGrow.IndiGrow import IndiGrow
import random
import numpy


if __name__ == '__main__':
    random.seed(182)
    numpy.random.seed(1277)

    population_size = 10E7
    mutation_rate = 10E-4

    test = IndiGrow(population_size=10E7)
    test.add_event(event_class=infection_event_update)
    test.add_event(event_class=infection_event_print, trigger_every=5)
    test.add_genotype(genotype=infectionclass())

    for i in range(50):
        test.timestep()
