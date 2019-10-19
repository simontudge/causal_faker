"""
A number of simple example graphs.
"""

from .causal_faker import CausalFaker
from random import random

def random_confonder():

	weights = {
	     (0, 3): random(),
	     (1, 5): random(),
	     (2, 4): random(),
	     (3, 4): random(),
	     (5, 3): random(),
	     (5, 4): random()
	}

	return CausalFaker(weights)

def random_collider():

	weights = {
	     (0, 3): random(),
	     (1, 5): random(),
	     (2, 4): random(),
	     (3, 4): random(),
	     (3, 5): random(),
	     (4, 5): random()
	}

	return CausalFaker(weights)
