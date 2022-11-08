def dna_to_rna(dna = "GATCTCCGTC")
    #your code here
    for i in 0..(dna.size - 1)
      # if i == "T"
      dna[i] = dna[i] == "T" ? "U" : dna[i]
    end
    dna
end

# dna_to_rna()