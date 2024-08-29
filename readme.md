Genome and Genetic Algorithm Library

Overview
This library consists of two main classes:

GeneticAlgorithm: Implements a genetic algorithm to simulate and solve optimization problems using evolutionary strategies.
Genome: Provides tools for biological sequence analysis, including DNA and RNA generation, transcription, translation, and complementary strand operations.
Features
GeneticAlgorithm Class
Generate Population: Create an initial population of binary chromosomes.
Fitness Evaluation: Map chromosomes to their fitness values using a custom fitness function.
Selection: Use roulette wheel selection to choose individuals based on fitness.
Mutation: Apply mutation to chromosomes with a given probability.
Crossover: Perform crossover between pairs of chromosomes.
Run: Execute the genetic algorithm over multiple generations to evolve solutions.
Genome Class
Generate Single-Stranded DNA: Create random single-stranded DNA sequences.
Generate RNA: Create random RNA sequences.
Complementary DNA Strand: Compute the complementary DNA strand for a given sequence.
Check DNA: Verify if two DNA sequences are complementary.
Reading Frames: Calculate the six possible reading frames of a DNA sequence.
Translate DNA: Convert DNA sequences to RNA and then to protein sequences.
Protein Synthesis: Translate RNA sequences into proteins using a codon dictionary.
Installation
To use this library, you need to have Ruby installed. You can check your Ruby installation by running:

bash
Copy code
ruby -v
Clone the repository and navigate to the directory:

bash
Copy code
git clone https://github.com/TMWcodes/genome-genetic-algorithm.git
cd genome-genetic-algorithm
Usage
GeneticAlgorithm Example
ruby
Copy code
require './synth_genome'

ga = GeneticAlgorithm.new
population = ga.generate(8) # Generate a population of binary strings of length 8
fitness_function = lambda { |chromosome| # Define your fitness function
ideal = '10101010'
1.0 \* ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size
}

result = ga.run(8) # Run the genetic algorithm for 100 iterations
Genome Example
ruby
Copy code
require './bio_genome'

genome = Genome.new

# DNA and RNA operations

dna = genome.generate_ssDNA(10)
puts "DNA is #{dna}"
cdna = genome.complementary_DNA_strand(dna)
puts "Complementary strand: #{cdna}"

rna = genome.dna_to_rna(dna)
puts "mRNA: #{rna}"

protein = genome.protein(rna)
puts "Protein: #{protein}"

frames = genome.six_reading_frames(dna, cdna)
puts "Reading frames: #{frames}"

Contributing
Feel free to submit issues and pull requests. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to adjust paths, URLs, and any specific details based on your project setup and repository.
