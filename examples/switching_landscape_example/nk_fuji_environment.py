from nk_fuji_class import nk_fuji_class

class nk_fuji_environment:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __update__(self):
        current_state = 'nk' if self.__IndiGrow__.step % 2 == 0 else 'fuji'
        if current_state == 'fuji':
             self.__IndiGrow__.fitness_function = nk_fuji_class.nklandscape.fitness 
        else:
             self.__IndiGrow__.fitness_function = nk_fuji_class.fujilandscape.fitness
        self.__IndiGrow__.mark_as_dirty(all_dirty=True)



# environments
    # two different explicit landscapes you switch between
    # this one (infection)
    # co-evolutionary thing??? makeup of genotypes of one population determines fitness of other population
    # resources: different genotypes have different phenotypes that use amounts of those resources, becomes less and less beneficial
    # compete for resource, fitness function determined basically by whats in the environment