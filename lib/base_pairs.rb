def generate_strand(length)
    nucleotide = ["A", "T", "G", "C"]
    chromosome = []
    until chromosome.length >= length
    chromosome << nucleotide.sample
    end
    chromosome.join
    # Good Luck!
  end