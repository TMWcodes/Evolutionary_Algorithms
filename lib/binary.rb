class GeneticAlgorithm
    def generate(length)
      nucleotide = [0,1]
      chromosome = []
      until chromosome.length >= length
      chromosome << nucleotide.sample
      end
      chromosome.join
      # Good Luck!
    end
    
    def select population, fitnesses
      #TODO: Implement the select method
    end
    
    def mutate(chromosome = "1010010110", p = 0)
      has_letters = chromosome.each_char.any?("a".."z")
      # loop 
       if has_letters == true
       fail "invalid nucleotide"
       end
   
   chromosome = chromosome.dup
      for i in 0..(chromosome.size - 1)
           # error catch
           if rand < p
           chromosome[i] = chromosome[i] == "0" ? "1" : "0"
           # reverses numbers, become 1 or 0 based if chromosome i is equal to "0"
           end
       end
       chromosome
   end
    
   def crossover (chromosome1, chromosome2, index)
    chr1 = chromosome1[0...index] + chromosome2[index..-1]
    chr2 = chromosome2[0...index] + chromosome1[index..-1]
    [chr1, chr2]
  end
    
    
    def run fitness, length, p_c, p_m, iterations=100
      #TODO: Implement the run method
    end
  end
