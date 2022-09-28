def DNA_strand(dna)
    for i in 0..(dna.size - 1)
        case dna[i]
        when "A"
            dna[i] = "T"
        when "T"
            dna[i] = "A"
        when "G"
            dna[i] = "C"
        when "C" 
            dna[i] = "G"
        end
    end
    dna
  end