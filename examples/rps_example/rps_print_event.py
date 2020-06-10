class rps_print_event:
    def __init__(self):
        self.__IndiGrow__ = None

    def __run_handler__(self):
        frequencies = {}
        for i in self.__IndiGrow__.population.vs:
            frequencies[i['genotype'].type] = i['frequency']
        print(frequencies)
        