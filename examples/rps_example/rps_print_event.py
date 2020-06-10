import json

class rps_print_event:
    def __init__(self):
        self.__IndiGrow__ = None
        # clear current contents of file
        open('rps_data.txt', 'w').close()

    def __run_handler__(self):
        frequencies = {}
        for i in self.__IndiGrow__.population.vs:
            frequencies[i['genotype'].type] = i['frequency']
        with open('rps_data.txt', 'a+') as write_file:
            write_file.write(json.dumps(frequencies) + '\n')
        