def generate_ssDNA(length) # single strand dna
    nucleotide = ["A", "T", "G", "C"]
    chromosome = []
    until chromosome.length >= length
    chromosome << nucleotide.sample
    end
    chromosome.join
    # Good Luck!
  end

  def generate_rna
    nucleotide = ["A", "U", "G", "C"]
    chromosome = []
    until chromosome.length >= length
    chromosome << nucleotide.sample
    end
    chromosome.join
  end