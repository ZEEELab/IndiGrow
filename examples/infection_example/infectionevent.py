import random
from copy import deepcopy

class infection_event_update:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __run_handler__(self):
        groups = self.__IndiGrow__.group_by_attributes(['bitstring'])
        for group in groups:
            for member in group:
                if member['genotype'].state == 'notinfected':
                    self.__IndiGrow__.transfer_state(member['genotype'], {'state' : 'infected'}, random.random())
                elif member['genotype'].state == 'infected':
                    self.__IndiGrow__.transfer_state(member['genotype'], {'state' : 'immune'}, random.random())
       
class infection_event_print:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __run_handler__(self):
        groups = self.__IndiGrow__.group_by_attributes(['state'])
        for group in groups:
            frequency = 0
            for member in group:
                frequency += member['frequency']
            print(group[0]['genotype'].state, frequency)
        print('\n')


# environments
    # two different explicit landscapes you switch between √
    # this one (infection) √
    # co-evolutionary thing??? makeup of genotypes of one population determines fitness of other population
    # resources: different genotypes have different phenotypes that use amounts of those resources, becomes less and less beneficial
    # compete for resource, fitness function determined basically by whats in the environment