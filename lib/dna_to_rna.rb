def dna_to_rna(dna = "GATCTCCGTC")
    #your code here
    for i in 0..(dna.size - 1)
      # if i == "T"
      dna[i] = dna[i] == "T" ? "U" : dna[i]
    end
    dna
end

def rna_to_dna(rna = "UGCGAUGAAUGGGCUCGCUCC")
  for i in 0..(rna.size - 1)
    # if i == "T"
    rna[i] = rna[i] == "U" ? "T" : rna[i]
  end
  rna
end

puts rna_to_dna()