import random

def rand_uniform(rng, lo, hi):
    return lo + (hi - lo) * rng.random()

def choose(rng, seq):
    return seq[int(rng.random() * len(seq))]
