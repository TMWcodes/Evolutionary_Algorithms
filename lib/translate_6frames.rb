



def translate_with_frame(dna="TGCGATGAATGGGCTCGCTCC", frames=[1,2,3,-1,-2,-3])
    aminoacid_dictionary = {'UUC'=>'F', 'UUU'=>'F','UUA'=>'L', 'UUG'=>'L', 'CUU'=>'L', 'CUC'=>'L','CUA'=>'L','CUG'=>'L', 'AUU'=>'I', 'AUC'=>'I', 'AUA'=>'I','AUG'=>'M','GUU'=>'V', 'GUC'=>'V', 'GUA'=>'V', 'GUG'=>'V', 'UCU'=>'S', 'UCC'=>'S', 'UCA'=>'S', 'UCG'=>'S', 'AGU'=>'S', 'AGC'=>'S', 'CCU'=>'P', 'CCC'=>'P', 'CCA'=>'P', 'CCG'=>'P', 'ACU'=>'T', 'ACC'=>'T', 'ACA'=>'T', 'ACG'=>'T', 'GCU'=>'A', 'GCC'=>'A', 'GCA'=>'A', 'GCG'=>'A', 'UAU'=>'Y', 'UAC'=>'Y', 'CAU'=>'H', 'CAC'=>'H', 'CAA'=>'Q', 'CAG'=>'Q', 'AAU'=>'N', 'AAC'=>'N', 'AAA'=>'K', 'AAG'=>'K', 'GAU'=>'D', 'GAC'=>'D', 'GAA'=>'E', 'GAG'=>'E', 'UGU'=>'C', 'UGC'=>'C', 'UGG'=>'W', 'CGU'=>'R', 'CGC'=>'R', 'CGA'=>'R', 'CGG'=>'R', 'AGA'=>'R', 'AGG'=>'R', 'GGU'=>'G',  'GGC'=>'G', 'GGA'=>'G', 'GGG'=>'G', 'UAA'=>'*', 'UGA'=>'*', 'UAG'=>'*'}
    
    output = []

    if dna == ""
        for i in 0...frames.length
        output << ""
        end
    return output
    end

   
    frame1 = dna.gsub('T','U').scan(/.../).join""
    frame2 = dna.gsub('T','U')[1..-3].scan(/.../).join""
    frame3 = dna.gsub('T','U')[2..-2].scan(/.../).join""
  
    rframe1 = dna.tr("ACGT", "TGCA").reverse.gsub('T','U').scan(/.../).join""
    rframe2 = dna.tr("ACGT", "TGCA").reverse.gsub('T','U')[1..-3].scan(/.../).join""
    rframe3 = dna.tr("ACGT", "TGCA").reverse.gsub('T','U')[2..-2].scan(/.../).join""
  
    output << [frame1, frame2, frame3, rframe1,rframe2, rframe3] 

    
    translations = output.flatten.map do |frames| 
        frames.scan(/.../).map{|match|aminoacid_dictionary[match]}.join 
    end

    frames.map do |frame| 
        case
            when frame == -1 then frame = 4
            when frame == -2 then frame = 5
            when frame == -3 then frame = 6
            else 
                ""
        end
    translations[frame-1]
    end
    
end

p translate_with_frame()
