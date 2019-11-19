from nklandscape import nklandscape
from fujilandscape import fuji
from nklandscape import binary
from random import randint
from copy import deepcopy
from backports.functools_lru_cache import lru_cache
import numpy


class nkclass:
    #landscape = nklandscape(10, 5, numpy.random.RandomState(3))
    landscape = fuji()

    def __init__(self):
        self.bitstring = randint(0, (2**self.landscape.n) - 1)

    def __fitness__(self):
        return self.landscape.fitness(self.bitstring)


    def __mutate__(self):
        bstr = binary(self.bitstring, self.landscape.n)[2:]
        for _ in range(1):
            bstr = list(bstr)
            flip_index = randint(0, self.landscape.n - 1)
            bstr[flip_index] = '0' if bstr[flip_index] == '1' else '1'
            bstr = ''.join(bstr)
        self.bitstring = int(bstr, 2)
    
    @lru_cache(maxsize=64)
    def __mutational_neighborhood__(self):
        neighborhood = []
        for i in range(self.landscape.n):
            neighbor = deepcopy(self)
            bstr = list(binary(neighbor.bitstring, self.landscape.n)[2:])
            bstr[i] = '0' if bstr[i] == '1' else '1'
            bstr = ''.join(bstr)
            neighbor.bitstring = int(bstr, 2)
            neighborhood.append(neighbor)
        return neighborhood





# b = nkclass()
# print(b.bitstring)
# print([m.bitstring for m in b.__mutational_neighborhood__()])
# b.mutate()
# print(b.bitstring)
# # c = nkclass()

# print(b.fitness(), c.fitness())