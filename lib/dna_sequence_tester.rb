require_relative 'complementary_dna'

DNA_strand('')

def check_DNA(seq1, seq2)
    
    strand2 = seq2.reverse
    strand2_check = DNA_strand(seq1)
    strand2.eql? strand2_check
   
end

check_DNA('ATGCTACG','CGTAGCAT')