# Genome and Genetic Algorithm Library

## Overview

This library consists of two main classes:

- **`GeneticAlgorithm`**: Implements a genetic algorithm to simulate and solve optimization problems using evolutionary strategies.
- **`Genome`**: Provides tools for biological sequence analysis, including DNA and RNA generation, transcription, translation, and complementary strand operations.

## Features

### `GeneticAlgorithm` Class

- **Generate Population**: Create an initial population of binary chromosomes.
- **Fitness Evaluation**: Map chromosomes to their fitness values using a custom fitness function.
- **Selection**: Use roulette wheel selection to choose individuals based on fitness.
- **Mutation**: Apply mutation to chromosomes with a given probability.
- **Crossover**: Perform crossover between pairs of chromosomes.
- **Run**: Execute the genetic algorithm over multiple generations to evolve solutions.

### `Genome` Class

- **Generate Single-Stranded DNA**: Create random single-stranded DNA sequences.
- **Generate RNA**: Create random RNA sequences.
- **Complementary DNA Strand**: Compute the complementary DNA strand for a given sequence.
- **Check DNA**: Verify if two DNA sequences are complementary.
- **Reading Frames**: Calculate the six possible reading frames of a DNA sequence.
- **Translate DNA**: Convert DNA sequences to RNA and then to protein sequences.
- **Protein Synthesis**: Translate RNA sequences into proteins using a codon dictionary.

## Installation

To use this library, you need to have Ruby installed. You can check your Ruby installation by running:

```bash
ruby -v

# Clone the repository and navigate to the directory:
# Copy code
git clone https://github.com/TMWcodes/https://github.com/TMWcodes/Evolutionary_Algorithms.git
cd https://github.com/TMWcodes/Evolutionary_Algorithms
Usage GeneticAlgorithm
ruby Copy code require './synth_genome'
```

## Usage

### GeneticAlgorithm Example

```ruby
require './synth_genome'

ga = GeneticAlgorithm.new
population = ga.generate(8) # Generate a population of binary strings of length 8

fitness_function = lambda do |chromosome|
  ideal = '10101010'
  1.0 * ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size
end

result = ga.run(8) # Run the genetic algorithm for 100 iterations
```

### Genome Example

```ruby
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

```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

You can save this content as `README.md` in your project directory. Adjust any paths, URLs, or specific details as needed for your project.
