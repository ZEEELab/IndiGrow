import random

class infectionenvironment:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __update__(self):
        groups = self.__IndiGrow__.group_by_attributes(['bitstring'])
        for group in groups:
            for member in group:
                if member['genotype'].state == 'notinfected':
                    self.__IndiGrow__.transfer_state(member['genotype'], {'state' : 'infected'}, random.random())
                elif member['genotype'].state == 'infected':
                    self.__IndiGrow__.transfer_state(member['genotype'], {'state' : 'immune'}, random.random())
       



# environments
    # two different explicit landscapes you switch between
    # this one (infection)
    # co-evolutionary thing??? makeup of genotypes of one population determines fitness of other population
    # resources: different genotypes have different phenotypes that use amounts of those resources, becomes less and less beneficial
    # compete for resource, fitness function determined basically by whats in the environment