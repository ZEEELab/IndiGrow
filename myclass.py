from nklandscape import nklandscape
from nklandscape import binary
from random import randint

class nkclass:
    landscape = nklandscape(5, 3)

    def __init__(self):
        self.bitstring = randint(0, 31)

    def fitness(self):
        return self.landscape.fitness(self.bitstring)

    def mutate(self):
        bstr = binary(self.bitstring, self.landscape.n)[2:]
        bstr = list(bstr)
        flip_index = randint(0, self.landscape.n - 1)
        bstr[flip_index] = '0' if bstr[flip_index] == '1' else '1'
        bstr = ''.join(bstr)
        self.bitstring = int(bstr, 2)



# b = nkclass()
# print(b.bitstring)
# b.mutate()
# print(b.bitstring)
# # c = nkclass()

# print(b.fitness(), c.fitness())