from random import randint
import random
from copy import deepcopy
import numpy


class infectionclass:

    def __init__(self):
        self.bitstring = randint(0, (2**4) - 1)
        self.state = 'notinfected'

    def __fitness__(self):
        if self.state != 'infected':
            return self.bitstring
        else:
            return self.bitstring / 2

    def __mutate__(self):
        self.bitstring += 1 if random.random() > .5 else -1
    
    def __mutational_neighborhood__(self):
        neighborhood = [deepcopy(self), deepcopy(self)]
        neighborhood[0].bitstring += 1
        neighborhood[1].bitstring -= 1
        return neighborhood





# b = nkclass()
# print(b.bitstring)
# print([m.bitstring for m in b.__mutational_neighborhood__()])
# b.mutate()
# print(b.bitstring)
# # c = nkclass()

# print(b.fitness(), c.fitness())