from random import uniform
from random import choices
from random import randint
import random

def binary(num, length):
    return format(num, '#0{}b'.format(length + 2))


class nklandscape:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.fitnesses = dict()
        self.cached_vals = dict()

    def fitness(self, genotype):
        if genotype in self.cached_vals:
            return self.cached_vals[genotype]
        total = 0
        bstr = binary(genotype, self.n)[2:]
        bstr += bstr[::-1]
        for i in range(self.n):
            val = int(bstr[i:i + self.k + 1], 2)
            if val not in self.fitnesses:
                self.fitnesses[val] = random.random()
            total += self.fitnesses[val]
        self.cached_vals[genotype] = total
        return total
