
def generate(length, population_size=1)
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

generate(20).join().length

   # to generate a population of chromosomes with initializer
  
  # def initialize
  #   @population_size = 10 # Default population size
  # end

  # def set_population_size(population_size)
  #   @population_size = population_size
  # end

  # def generate(length)
  #   population = []
  #   @population_size.times do
  #     nucleotide = [0,1]
  #     chromosome = []
  #     until chromosome.length >= length
  #     chromosome << nucleotide.sample
  #     end
  #     population << chromosome.join
  #   end
  #   population
  # end