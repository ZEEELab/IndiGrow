import random

class nk_fuji_environment:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __update__(self):
        current_state = 'nk' if self.__IndiGrow__.step % 2 == 0 else 'fuji'
        next_state = 'nk' if current_state == 'fuji' else 'fuji'
        nodes = self.__IndiGrow__.find_all_attributes({'landscape_state' : current_state})
        for node in nodes:
            self.__IndiGrow__.transfer_state(node['genotype'], {'landscape_state' : next_state}, 1)
       



# environments
    # two different explicit landscapes you switch between
    # this one (infection)
    # co-evolutionary thing??? makeup of genotypes of one population determines fitness of other population
    # resources: different genotypes have different phenotypes that use amounts of those resources, becomes less and less beneficial
    # compete for resource, fitness function determined basically by whats in the environment