from nklandscape import nklandscape
from nklandscape import binary
from random import randint

class nkclass:
    landscape = nklandscape(5, 1)

    def __init__(self):
        self.bitstring = randint(0, (2**self.landscape.n) - 1)

    def __fitness__(self):
        return self.landscape.fitness(self.bitstring)

    def __mutate__(self):
        bstr = binary(self.bitstring, self.landscape.n)[2:]
        for _ in range(randint(1, self.landscape.n)):
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