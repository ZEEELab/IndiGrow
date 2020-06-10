from fujilandscape import fuji
from random import randint
from backports.functools_lru_cache import lru_cache
import numpy


def binary(num, length):
    return format(num, '#0{}b'.format(length + 2))


class switching_class:
    fujilandscape1 = fuji(optimal_genotype=0, n=4)
    fujilandscape2 = fuji(optimal_genotype=15, n=4)

    def __init__(self, n=10):
        self.n = n
        self.bitstring = randint(0,(2**n) - 1)
        self.__current_fuji__ = self.fujilandscape1

    def __fitness__(self):
        return self.__current_fuji__.fitness(self.bitstring)

    def __mutate__(self):
        bstr = binary(self.bitstring, self.n)[2:]
        for _ in range(1):
            bstr = list(bstr)
            flip_index = randint(0, self.fujilandscape1.n - 1)
            bstr[flip_index] = '0' if bstr[flip_index] == '1' else '1'
            bstr = ''.join(bstr)
        self.bitstring = int(bstr, 2)
    
    @lru_cache(maxsize=64)
    def __mutational_neighborhood__(self):
        neighborhood = []
        for i in range(self.n):
            neighbor = self.__IndiGrow__.genotype_deepcopy(self)
            bstr = list(binary(neighbor.bitstring, self.n)[2:])
            bstr[i] = '0' if bstr[i] == '1' else '1'
            bstr = ''.join(bstr)
            neighbor.bitstring = int(bstr, 2)
            neighborhood.append(neighbor)
        return neighborhood