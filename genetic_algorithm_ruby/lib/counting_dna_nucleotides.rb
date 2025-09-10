def get_counted_nucleotides(dna)
 counted = Hash.new
 
 nucleobases = "ATGC"
 dna.upcase
# adds Nucleobases to hash with value of 0
 nucleobases.each_char do |char| 
    counted[char] = 0
 end

 #counter
 dna.each_char do |base|
      case base
      when "A"
      counted['A'] += 1   
      when "T"
         counted['T'] += 1   
      when "G"
         counted['G'] += 1   
      when "C"
         counted['C'] += 1   
      end
   end
    
 counted
 
end

# get_counted_nucleotides('TTT')