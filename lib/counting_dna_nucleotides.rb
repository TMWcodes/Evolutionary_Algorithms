def get_counted_nucleotides(dna)
 counted = Hash.new
 
 nucleobases = "ATGC"
 dna.upcase

 nucleobases.each_char do |char| 
    counted[char] = 0
 end



 dna.each_char do |base|
    case base
    when "T"
     counted['T'] += 1   
    end
    
 end
    
 counted
 
end

get_counted_nucleotides('TTT')