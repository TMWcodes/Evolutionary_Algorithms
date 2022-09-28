def get_counted_nucleotides(dna)
 counted = Hash.new
 
 nucleobases = "ATGC"
 dna.upcase

 nucleobases.each_char do |char| 
    counted[char] = 0
 end
 counted
 
end

get_counted_nucleotides('')