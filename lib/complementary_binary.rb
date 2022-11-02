
def binary_double(chromosome)
    chromosome = chromosome.dup
    for i in 0..(chromosome.size-1)
        case chromosome[i]
        when "1"
            chromosome[i] = "0"
        when "0"
            chromosome[i] = "1"
        end
    end
    chromosome
end
