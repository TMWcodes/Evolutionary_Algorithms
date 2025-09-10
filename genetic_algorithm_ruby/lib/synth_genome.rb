
class GeneticAlgorithm
  
      # to generate a population without initializer, default 1
  
  def generate(length, population_size=10)
    population = []
    population_size.times do
      nucleotide = [0,1]
      chromosome = []
      until chromosome.length >= length
      chromosome << nucleotide.sample
      end
      population << chromosome.join
    end
    population
  end

  
  def map_population_fit(population, &fitness)
    population.map { |chromosome| { chromosome: chromosome, fitness: fitness.call(chromosome) } }
  end
  

  def roulette_wheel_selection(population, fitness_values, num_selections)
    total_fitness = fitness_values.sum
    probabilities = fitness_values.map { |fitness| fitness.to_f / total_fitness }
  
    cumulative_probabilities = []
    cumulative_sum = 0
    probabilities.each do |probability|
      cumulative_sum += probability
      cumulative_probabilities << cumulative_sum
    end
  
    selected_individuals = []
    num_selections.times do
      random_number = rand()
      cumulative_probabilities.each_with_index do |probability, index|
        if random_number <= probability
          selected_individuals << population[index]
          # Remove the selected individual from the population and fitness_values
          # population.delete_at(index)
          # fitness_values.delete_at(index)
          # cumulative_probabilities = cumulative_probabilities.map { |p| p - probability } # Adjust cumulative probabilities
          break
        end
      end
    end
  
    selected_individuals
  end
  
  def mutate(chromosome, p = 0.02)
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
  
  def crossover(chromosome_pair, index = 4)
    chromosome1, chromosome2 = chromosome_pair
    if chromosome1.nil? || chromosome2.nil?
      raise ArgumentError, "Both chromosomes in the pair must be non-nil."
    end
  
    chr1 = chromosome1[0...index] + chromosome2[index..-1]
    chr2 = chromosome2[0...index] + chromosome1[index..-1]
    [chr1, chr2]
  end

  
  def run(length, iterations=100)
    #TODO: Implement the run method
  
    #generate
    p "----STARTING POPULATION---"
    p population = ["11000010", "00100010", "00111110", "11010110", "00111111", "00101101", "01000001", "11101000", "00010000", "10101101"]

    # loop
    fitness = lambda do |chromosome|
      ideal = '10101010'
      # Compare each character of the chromosome with the ideal target
      1.0 * ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size 
    end
    count = 0
    iterations.times do
      # **Evaluate fitness for each chromosome in the population**
      
    
      # fitness calc
   
      fitness_values = map_population_fit(population, &fitness).map { |individual| individual[:fitness]} # [0.625, 0.75, 0.625, 0.375, 0.5, 0.5, 0.25, 0.75, 0.375, 0.625]
    
      # selection
      
      selected_chromosomes = roulette_wheel_selection(population, fitness_values, fitness_values.length) # ["00111110", "01000001", "00111110", "00100010", "10101101", "00111110", "00111110", "10101101", "10101101", "00100010"]
      # p gene.map_population_fit(selected_chromosomes, &fitness)
      # var
      new_population = []
    
      # Pairing
      input = selected_chromosomes.each_slice(2).to_a #=> [["11101000", "10101101"], ["11000010", "11101000"], ["00100010", "10101101"], ["10101101", "00010000"], ["00010000", "00111111"]]
    
      # Crossover
      output = input.map { |pair| crossover(pair) } # [["11110000", "00001111"], ["11111111", "00000000"], ["11100001", "00011110"]]
      new_population << output.flatten
      # mutate
     
      
      population = new_population.flatten # ["00100010", "00100110", "00100010", "00100110", "00100110", "00100010", "00100010", "00100010", "00100110", "00100010"]
    
      
      mutated = population.map {|var| mutate(var)} # ["11101001", "10110110", "10000011", "11001011", "11100100", "10100110", "10110010", "11100010", "10001000", "10100011"]
      population = mutated
      # p best_chromosome = population.max_by(2) { |individual| individual[:fitness]}
      # no implicit conversion of Symbol into Integer (TypeError)
      best_fitness = map_population_fit(population, &fitness).map {|var| var[:fitness]}.max
      # p best_fitness[:chromosome]
      best_chromosome = map_population_fit(population, &fitness).map {|var| var[:chromosome]}.max
      if best_chromosome == '10101010'
        puts "Generation: #{count}"
        break
      end
     
      count += 1
     
    end
   
      # p best_fitness[:chromosome]
    best_chromosome = map_population_fit(population, &fitness).map {|var| var[:chromosome]}.max
    best_fitness = map_population_fit(population, &fitness).map {|var| var[:fitness]}.max
    puts "Best Chromosome: #{best_chromosome}, Best fitness: #{best_fitness}"
      
  end

end
 


#######
# fitness (a fitness function), length (the length of each chromosome), p_c (crossover probability), p_m (mutation probability), and an optional parameter iterations (the number of iterations to run the genetic algorithm, with a default value of 100).


####

gene = GeneticAlgorithm.new
gene.run(8)
  
# Apply the genetic algorithm crossover





