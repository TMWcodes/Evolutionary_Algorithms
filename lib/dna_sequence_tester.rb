require_relative 'complementary_dna'

DNA_strand('')

def check_DNA(seq1, seq2)
    
    strand2 = seq2.reverse
    strand2_check = seq1.tr("ACTG", "TGAC")
    strand2_check.include? strand2
end

p check_DNA('ATGCTACG','CGTAGCAT')