from collections import namedtuple

def fitness(c):
    ideal = '11110000'
    return float(len([a for a, b in zip(c, ideal) if a == b])) / len(ideal)

def map_population_fit(population, fitness):
    population = ['10100111', '11011100', '01000101', '01110000']
    # <class '__main__.ChromosomeWrap'>
    ChromosomeWrap = namedtuple("ChromosomeWrap", ["chromosome", "fitness"])
    
    return (ChromosomeWrap(chromosome, fitness(chromosome)) for chromosome in population)
  
#<generator object map_population_fit.<locals>.<genexpr> at 0x0000028169527370>
print(map_population_fit(['10100111', '11011100', '01000101', '01110000'], fitness))