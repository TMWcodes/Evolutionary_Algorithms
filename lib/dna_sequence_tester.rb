require_relative 'complementary_dna'

DNA_strand('')

def check_DNA(seq1, seq2)
    
 
    if seq1.length >= seq2.length

        strand2 = seq2.reverse
        strand2_check = seq1.tr("ACTG", "TGAC")
        strand2_check.include? strand2
    else
        strand1 = seq1.reverse
        strand1_check = seq2.tr("ACTG", "TGAC")
        strand1_check.include? strand1
    end

end

# check_DNA('ATGCTACG','CGTAGCAT')