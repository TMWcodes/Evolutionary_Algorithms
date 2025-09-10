
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

def check_binary(seq1, seq2)
    
 
    if seq1.length >= seq2.length

        strand2 = seq2.reverse
        strand2_check = seq1.tr("01", "10")
        strand2_check.include? strand2
    else
        strand1 = seq1.reverse
        strand1_check = seq2.tr("10", "01")
        strand1_check.include? strand1
    end

end