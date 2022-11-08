
require_relative 'rna_to_protein_sequence'
require_relative '6_reading_frames'
require_relative 'complementary_dna'
require_relative 'dna_to_rna'

def translate_with_frame(dna="TGCGATGAATGGGCTCGCTCC", frames=[1,2,3,-1,-2,-3])
    aminoacid_dictionary = {'UUC'=>'F', 'UUU'=>'F','UUA'=>'L', 'UUG'=>'L', 'CUU'=>'L', 'CUC'=>'L','CUA'=>'L','CUG'=>'L', 'AUU'=>'I', 'AUC'=>'I', 'AUA'=>'I','AUG'=>'M','GUU'=>'V', 'GUC'=>'V', 'GUA'=>'V', 'GUG'=>'V', 'UCU'=>'S', 'UCC'=>'S', 'UCA'=>'S', 'UCG'=>'S', 'AGU'=>'S', 'AGC'=>'S', 'CCU'=>'P', 'CCC'=>'P', 'CCA'=>'P', 'CCG'=>'P', 'ACU'=>'T', 'ACC'=>'T', 'ACA'=>'T', 'ACG'=>'T', 'GCU'=>'A', 'GCC'=>'A', 'GCA'=>'A', 'GCG'=>'A', 'UAU'=>'Y', 'UAC'=>'Y', 'CAU'=>'H', 'CAC'=>'H', 'CAA'=>'Q', 'CAG'=>'Q', 'AAU'=>'N', 'AAC'=>'N', 'AAA'=>'K', 'AAG'=>'K', 'GAU'=>'D', 'GAC'=>'D', 'GAA'=>'E', 'GAG'=>'E', 'UGU'=>'C', 'UGC'=>'C', 'UGG'=>'W', 'CGU'=>'R', 'CGC'=>'R', 'CGA'=>'R', 'CGG'=>'R', 'AGA'=>'R', 'AGG'=>'R', 'GGU'=>'G',  'GGC'=>'G', 'GGA'=>'G', 'GGG'=>'G', 'UAA'=>'*', 'UGA'=>'*', 'UAG'=>'*'}
    output = []
    # dna is string
    # frames is an array of integers, used to select which reading frames to translate and display
    seq1 = dna # TGCGATGAATGGGCTCGCTCC"
    seq2 = DNA_strand(dna).reverse #"GGAGCGAGCCCATTCATCGCA"
    mrna1 = dna_to_rna(seq1) # "UGCGAUGAAUGGGCUCGCUCC"
    mrna2 = dna_to_rna(seq2.reverse) #"ACGCUACUUACCCGAGCGAGG"
    frame1 = mrna1.scan(/.../).join""
    frame2 = mrna1[1..-3].scan(/.../).join""
    frame3 = mrna1[2..-2].scan(/.../).join""
    rframe1 = mrna2.scan(/.../).join""
    rframe2 = mrna2[1..-3].scan(/.../).join""
    rframe3 = mrna2[2..-2].scan(/.../).join""
    output << [frame1, frame2, frame3, rframe1,rframe2, rframe3] #[["UGCGAUGAAUGGGCUCGCUCC", "GCGAUGAAUGGGCUCGCU", "CGAUGAAUGGGCUCGCUC"]]
    
    trans_array = output.flatten.map do |frames| 
        frames.scan(/.../).map{|match|aminoacid_dictionary[match]}.join 
    end
    frames.map { |frame| 
        if frame == -1
            frame = 4
        elsif frame == -2
            frame = 5
        elsif frame == -3
            frame = 6
        end
        frame = trans_array[frame-1]
    }
    # ["CDEWARS", "AMNGLA", "R*MGSL", "TLLTRAR", "RYLPER", "ATYPSE"] 1-6
end

translate_with_frame("TGCGATGAATGGGCTCGCTCC")