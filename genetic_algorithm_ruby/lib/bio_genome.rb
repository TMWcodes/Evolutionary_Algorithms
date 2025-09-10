class Genome
    def initialize
        
    end
    
    def generate_ssDNA(length) # single strand DNA
        nucleotide = ["A", "T", "G", "C"]
        chromosome = []
        until chromosome.length >= length
        chromosome << nucleotide.sample
        end
        chromosome.join
    end

    def generate_rna(length)
        nucleotide = ["A", "U", "G", "C"]
        chromosome = []
        until chromosome.length >= length
        chromosome << nucleotide.sample
        end
        chromosome.join
    end

    def complementary_DNA_strand(dna)
        dna = dna.upcase
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

    def six_reading_frames(seq1, rseq2)
        output = []
        
        frame1 = seq1.scan(/.../).join" "
        f2 = seq1[1..-3].scan(/.../).join" "
        frame2 = seq1[0] + " " + f2 + " " + seq1[-2..-1]
        f3 = seq1[2..-2].scan(/.../).join" "
        frame3 = seq1[0..1] + " " + f3 + " " + seq1[-1]
        output << [frame1, f2, f3].join("\n")
        # output << "\n"
    
        
        rframe1 = rseq2.scan(/.../).join" "
        f2 = rseq2[1..-3].scan(/.../).join" "
        rframe2 = rseq2[0] + " " + f2 + " " + rseq2[-2..-1]
        f3 = rseq2[2..-2].scan(/.../).join" "
        rframe3 = rseq2[0..1] + " " + f3 + " " + rseq2[-1]
        output << [rframe1, f2, f3].join("\n")
      
        return output
    end
    
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

    def dna_to_rna(dna = "GATCTCCGTC")
        #your code here
        for i in 0..(dna.size - 1)
          # if i == "T"
          dna[i] = dna[i] == "T" ? "U" : dna[i]
        end
        dna
    end

    $aminoacid_dictionary = {'UUC'=>'F', 'UUU'=>'F','UUA'=>'L', 'UUG'=>'L', 'CUU'=>'L', 'CUC'=>'L','CUA'=>'L','CUG'=>'L', 'AUU'=>'I', 'AUC'=>'I', 'AUA'=>'I','AUG'=>'M','GUU'=>'V', 'GUC'=>'V', 'GUA'=>'V', 'GUG'=>'V', 'UCU'=>'S', 'UCC'=>'S', 'UCA'=>'S', 'UCG'=>'S', 'AGU'=>'S', 'AGC'=>'S', 'CCU'=>'P', 'CCC'=>'P', 'CCA'=>'P', 'CCG'=>'P', 'ACU'=>'T', 'ACC'=>'T', 'ACA'=>'T', 'ACG'=>'T', 'GCU'=>'A', 'GCC'=>'A', 'GCA'=>'A', 'GCG'=>'A', 'UAU'=>'Y', 'UAC'=>'Y', 'CAU'=>'H', 'CAC'=>'H', 'CAA'=>'Q', 'CAG'=>'Q', 'AAU'=>'N', 'AAC'=>'N', 'AAA'=>'K', 'AAG'=>'K', 'GAU'=>'D', 'GAC'=>'D', 'GAA'=>'E', 'GAG'=>'E', 'UGU'=>'C', 'UGC'=>'C', 'UGG'=>'W', 'CGU'=>'R', 'CGC'=>'R', 'CGA'=>'R', 'CGG'=>'R', 'AGA'=>'R', 'AGG'=>'R', 'GGU'=>'G',  'GGC'=>'G', 'GGA'=>'G', 'GGG'=>'G', 'UAA'=>'Stop', 'UGA'=>'Stop', 'UAG'=>'Stop'}
    def protein(rna)
        rna.upcase.scan(/.../).take_while{|s| s }.map{|match|$aminoacid_dictionary[match]}.join
        # != 'UAA' && s != 'UGA' && s != 'UAG'
    end

    def run()
    end

end


genome = Genome.new

dna = genome.generate_ssDNA(10)
# p rna
dna = "TGCGATGAATGGGCTCGCTCC"
puts "DNA is #{dna}"
cdna = genome.complementary_DNA_strand(dna)
puts "the complementary strand is #{cdna}" 
rcdna = cdna.reverse
checked = genome.check_DNA(dna,rcdna)
puts "The complementary strand, when arranged 5 prime to 3 prime, is '#{rcdna}' , confirmed to be #{checked}"

mrna = genome.dna_to_rna(dna)
puts "when the dna undergoes transcription, the mrna reads #{mrna}"
# proteins = genome.protein(mrna) 
# puts "When translated it is #{proteins}"
  
# # frames = genome.six_reading_frames(dna, rcdna)
# # puts "the dna read as 6 frames looks like"
# # puts frames
# tframes = genome.translate_with_frame(dna)
# puts "The protiens read as 6 frames looks like" 
# puts tframes


