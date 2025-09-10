
def generate(length):
    # Good Luck!
    base_pairs = ["0","1"]
    chromosome = []
    import random
    while not len(chromosome) >= length:
        nucleotide  = random.choice(base_pairs)
        chromosome.append(nucleotide)
    return chromosome
