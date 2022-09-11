def mutate (chromosome = "1010010110", p = 0)
   has_letters = chromosome.each_char.any?("a".."z")
   # loop 
    if has_letters == true
    fail "invalid nucleotide"
    end

p chromosome = chromosome.dup
   for i in 0..(chromosome.size - 1)
        # error catch
        if rand < p
        chromosome[i] = chromosome[i] == "0" ? "1" : "0"
        # reverses numbers, become 1 or 0 based if chromosome i is equal to "0"
        end
    end
    chromosome
end

mutate("00000", 1 )

# "11010"
# "10010"
# "10110"
# "10100"
# "10101"

 # --- 1
# def mutate(probability_of_mutation)
#     @value = value.map { |ch| rand < probability_of_mutation ? invert(ch) : ch }
#   end

  
#   def invert(binary)
#     binary == "0" ? "1" : "0"
#   end
# ---- trial
# def mutate(chromosome = "1010010110", p)
# binary == "0" ? "1" : "0"
# p chromosome_array = chromosome.split("")
# value.map { |ch| rand < p ? chromosome == "0" ? "1" : "0"(ch):ch} 
# end
# --- 2
# def mutate(chromosome, p)
#     # chromosome = chromosome.dup
#     for i in 0..(chromosome.size - 1) do # loop, binary values
#       if rand < p then # random float e.g. 0.114 is less than p 
#         chromosome[i] = chromosome[i] == "1" ? "0" : "1" # that index if 1 will become "0" if false will become 1.
#       end
#     end
#     return chromosome
#   end

#   p mutate("111111", 0.25)
#   p rand
# ---- 3
# def mutate(chromosome, p)
#     chromosome.gsub(/./) { |m| rand < p ? m.tr("01", "10") : m }
#   end

# ----4 
# def mutate (chromosome, p)
#     chromosome.chars.map { |i| rand < p ? i.tr('01', '10') : i }.join
#   end