from random import uniform
from random import choices
from random import randint
def binary(num, length):
    return format(num, '#0{}b'.format(length + 2))

class nklandscape:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.fitnesses = dict()

    def fitness(self, genotype):
        total = 0
        bstr = binary(genotype, self.n)[2:]
        bstr += bstr[::-1]
        for i in range(self.n):
            val = int(bstr[i:i + self.k + 1], 2)
            if val not in self.fitnesses:
                self.fitnesses[val] = uniform(0, 1)
            total += self.fitnesses[val]
        return total


a = nklandscape(20, 10)
b = nklandscape(4, 0)
c = nklandscape(10, 5)

for _ in range(10000):
    rand = randint(0, 2**(10))
    a.fitness(rand)

