from causal_faker import CausalFaker
from numpy.random import random

weights = {
            (0, 1): random(),
            (1, 4): random(),
            (1, 5): random(),
            (2, 3): random(),
            (3, 1): random(),
            (3, 4): random(),
            (4, 5): random()
        }

cf = CausalFaker( weights)
df = cf.get_n(25)

print(df)
