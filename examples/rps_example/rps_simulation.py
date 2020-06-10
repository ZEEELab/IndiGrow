from rps_class import rps_class
from rps_print_event import rps_print_event
from IndiGrow.IndiGrow import IndiGrow
import random
import numpy


if __name__ == '__main__':
    random.seed(1892)
    numpy.random.seed(17)

    population_size = 1E5
    num_generations = 1000

    rps_simulation = IndiGrow(population_size=population_size, mutation_rate=0)

    rps_simulation.add_genotype(genotype=rps_class('rock'), frequency=50/100)
    rps_simulation.add_genotype(genotype=rps_class('paper'), frequency=25/100)
    rps_simulation.add_genotype(genotype=rps_class('scissors'), frequency=25/100)
    rps_simulation.add_event(event_class=rps_print_event, trigger_every=10)

    for i in range(num_generations):
        rps_simulation.timestep()
