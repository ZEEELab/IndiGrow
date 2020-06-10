class switching_event:
    def __init__(self):
        self.__IndiGrow__ = None
        self.state = 1
    
    def __run_handler__(self):
        for node in self.__IndiGrow__.population.vs():
            if self.state == 1:
                node['genotype'].__current_fuji__ = node['genotype'].fujilandscape2
            else:
                node['genotype'].__current_fuji__ = node['genotype'].fujilandscape1
        self.state = ~self.state + 2
        self.__IndiGrow__.mark_as_dirty(all_dirty=True)

class print_event:
    def __init__(self):
        self.__IndiGrow__ = None
    
    def __run_handler__(self):
        print(sum((self.__IndiGrow__.population.vs['fitness']))/len(self.__IndiGrow__.population.vs()))


# environments
    # two different explicit landscapes you switch between
    # this one (infection)
    # co-evolutionary thing??? makeup of genotypes of one population determines fitness of other population
    # resources: different genotypes have different phenotypes that use amounts of those resources, becomes less and less beneficial
    # compete for resource, fitness function determined basically by whats in the environment