

def crossover (chromosome1, chromosome2, index)
chr1 = chromosome1[0...index] + chromosome2[index..-1]
chr2 = chromosome2[0...index] + chromosome1[index..-1]
[chr1, chr2]

end

crossover("111000", "000111", 3)