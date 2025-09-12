# Biology

Bio-Genome

bio_genome.py implements a biologically inspired genetic algorithm (GA). It draws inspiration from real molecular biology processes (DNA, RNA, proteins, mutations, codon-aware crossover) to evolve candidate DNA sequences toward a target. Unlike a standard GA, this system emphasizes biological realism while keeping modularity (fitness functions are interchangeable)

# Overview of bio_genome.py

Encodes DNA, RNA, and proteins realistically.
Evolves populations with codon-aware mutation & crossover.
Uses pluggable fitness functions to adapt to different optimization goals.
Demonstrates both exact sequence matching and functional protein-level convergence.

Key Features

1. Biological Building Blocks

DNA & RNA generation: Creates random single-stranded DNA (ATGC) or RNA (AUGC) sequences.
Complementary DNA (cDNA): Builds the complementary strand.
DNA → RNA → Protein translation: Simulates transcription & translation using the genetic code.
Reading Frames: Supports six-frame translation, capturing overlapping ORFs like in mitochondrial DNA.
DNA Checking: Verifies complementarity (analogous to replication error-checking).

2. Evolutionary Mechanisms

Mutation: Codon-aware with a transition/transversion bias (mimics real mutation probabilities).
Crossover: Codon-aware recombination, ensures splits at multiples of 3 to preserve codon integrity.
Selection: Roulette-wheel proportional to fitness (higher fitness = higher chance of passing on genes).
Origin of life option: Can enforce biologically mandatory start (ATG) and stop codons, biasing the system toward valid open reading frames (ORFs).

3. Fitness Functions (Modular)

Fitness functions are separated into bio_fitness_functions.py and can be swapped in depending on the goal:
DNA fitness: Matches candidate DNA to a target sequence, with penalties for length, missing start/stop codons, and incorrect reading frame.
Phenotype fitness: Evaluates candidate DNA by its protein translation, rewarding functional similarity even if the codons differ (biologically realistic because of codon redundancy).
Pluggable: Any fitness function can be passed into the GA — e.g., GC-content balancing, protein stability, or external simulation scores.

4. Evolutionary Run (run_evolution)

Starts with a random population of DNA sequences.
Repeatedly applies fitness evaluation → selection → crossover → mutation.
Tracks both generation-best and overall-best solutions.
Verbose output shows best and average fitness per 100 generations, making progress clear.
Stops early if a perfect match is found.

## Use cases

The framework generalizes to any optimization problem where:
A solution can be expressed as a "sequence" (DNA = data representation).
Quality can be measured by a fitness function.

Examples:
Script scheduling / productivity automation: Candidate solutions = task schedules; fitness = productivity points/time.
Configuration optimization: DNA encodes parameter sets for simulations or workflows.
Resource allocation: DNA encodes assignments of resources, fitness = efficiency.
Automated testing: DNA encodes test strategies, fitness = coverage or bug-finding rate.

The biological realism (codon-aware mutation, redundancy, frames) is not just metaphorical — it makes the GA more robust and better at exploring solution space without breaking structure, which can be valuable in automation contexts where invalid solutions would otherwise dominate.

# Fitness modules

### Bio_fitness_functions

bio_auto_fitness
points_per_hour → optimizes raw efficiency.
weighted_balance → balances absolute output with efficiency.
deadline_penalty → simulates daily/weekly capacity with
penalties for exceeding limits.

### bio_auto_fitness

## WIP output

#### version 2

Perfect match at generation 63: ATGCGTACGTTAGC
Evolved result: {'dna': 'ATGCGTACGTTAGC', 'fitness': 1.0}

Best after 200 generations: ATGCGTACGTCAAG (fitness=0.79)
Evolved result: {'dna': 'ATGCGTACGTCAAG', 'fitness': 0.7857142857142857}

lost
def check_DNA(self, seq1, seq2):
def six_reading_frames(self, seq1, rseq2):
def translate_with_frame(self, dna, frames=[1,2,3,-1,-2,-3]):

### version 3

PS C:\Users\Tyrone\Documents\Programming\coding\Evolutionary_algorithms\genetic_algorithm_python\lib> python -m bio_genome
Best after 200 generations: AAGCGTAGTTTACCGCCGATTAACGATAATCATCGTTGCAGA (fitness=0.71)
Perfect match at generation 6: ATGGTACCT

### version 4

DNA fitness now enforces:

Length discipline (to fix version 3)

Start codon ATG

Stop codon (TAA, TAG, TGA)

DNA similarity + protein similarity combined

codon-aware crossover → recombination only at multiples of 3

Codon-aware mutation → only one base inside a codon mutates at a time, with transition bias

result.
random sequences that don’t start with ATG, end with stop codons, or match protein targets are exactly like these nonfunctional early molecules.
best = max(scored, key=lambda x: x["fitness"])
ValueError: max() arg is an empty sequence

### version 5

“origin-of-life - fitness floor, Population regeneration. solution

All bio functions (generate_ssDNA, cDNA, protein, six_reading_frames, etc.)

Evolutionary functions (mutate, codon-aware crossover)

DNA and protein fitness

Fitness floor and population regeneration to prevent empty sequences

Best after 200 generations: GATACTAATTACCGGAACAATTAATCACACTTTGTCGAAGAG (fitness=0.01)
Perfect match at generation 1: ATGGTTCCT

biologically accurate constraints dramatically reduce the probability of early success.

### version 6

Separate out fitness functions so GA framework could accept any fitness function

Any candidate sequence will always score at least 0.01.
python -m bio_genome
Best after 500 generations: ATGCGTACGCTTGA (fitness=0.89)
Best after 500 generations: GCTACCGGATGCGG (fitness=0.29)

check DNA useful if you want biologically inspired constraints beyond simple DNA/protein matching.

six_reading_frames(seq1, rseq2) explore multi-objective coding problems or overlapping functionality.

Translate_frames
for a more biologically realistic fitness evaluation or to simulate overlapping open reading frames.
use: Evolving sequences for synthetic biology where multiple proteins are encoded compactly.

### version 7

protein function low fitness
add best of all and avg of gen.

shows best and average/
Gen 0: Best 0.075, Avg 0.011
Gen 100: Best 0.893, Avg 0.704
Gen 200: Best 0.893, Avg 0.686
Gen 300: Best 0.893, Avg 0.749
Gen 400: Best 0.893, Avg 0.697
Gen 499: Best 0.893, Avg 0.773
Best after 500 generations: ATGCGTACGCTTGA (fitness=0.89)
Gen 0: Best 0.071, Avg 0.020
Gen 100: Best 0.286, Avg 0.240
Gen 200: Best 0.286, Avg 0.256
Gen 300: Best 0.286, Avg 0.261
Gen 400: Best 0.286, Avg 0.250
Gen 499: Best 0.286, Avg 0.254
Best after 500 generations: GCCACTGGATGTTT (fitness=0.29)

### version 8

improved fitness functions

Gen 0: Best 0.300, Avg 0.026
Gen 100: Best 0.864, Avg 0.682
Gen 200: Best 0.864, Avg 0.690
Gen 300: Best 0.864, Avg 0.730
Gen 400: Best 0.864, Avg 0.711
Gen 499: Best 0.864, Avg 0.699
Best after 500 generations: ATGCGTACGTTAGC (fitness=0.90)
Gen 0: Best 0.250, Avg 0.030
Perfect match at generation 30: ATGCGCACTTTATA

with start stop = true

Gen 0: Best 0.536, Avg 0.325
Gen 100: Best 0.857, Avg 0.676
Gen 200: Best 0.893, Avg 0.675
Gen 300: Best 0.900, Avg 0.747
Gen 400: Best 0.864, Avg 0.780
Gen 499: Best 0.900, Avg 0.756
Best after 500 generations: ATGCGTACGTTAGC (fitness=0.90)
Gen 0: Best 0.750, Avg 0.330
Perfect match at generation 7: ATGCGTACCCTTA

# version 1 (auto_fitness)

Gen 0: Best 8.790, Avg 4.569
Perfect match at generation 0: ATGTGACTGCCAATTACATAG

Best evolved schedule:

- Model Training (30 pts, 5.0 hr)
- Code Review (9 pts, 0.75 hr)
- Backup Verification (9 pts, 0.5 hr)
- Quick Health Check (3 pts, 0.1 hr)
- Deploy Script (18 pts, 1.5 hr)
  DNA sequence: ATGTGACTGCCAATTACATAG
  Fitness: 8.790

Remove the if fitness >= 1.0 stop condition in automation runs.

# version 2 (bio accurate)

Gen 0: Best 0.010, Avg 0.010
Gen 100: Best 0.010, Avg 0.010
Gen 200: Best 0.010, Avg 0.010
Gen 300: Best 0.010, Avg 0.010
Gen 400: Best 0.010, Avg 0.010
Gen 499: Best 0.010, Avg 0.010
Best after 500 generations: ATGGACGTAACCGCTAAATAG (fitness=0.010)

Best evolved schedule:
DNA sequence: ATGGACGTAACCGCTAAATAG
Fitness: 0.010

# version 3

C:\Users\Tyrone\Documents\Programming\coding\Evolutionary_algorithms\genetic_algorithm_python\lib> python -m bio_genome
Gen 0: Best 7.704, Avg 6.044
Gen 100: Best 8.129, Avg 6.462
Gen 200: Best 8.652, Avg 7.327
Gen 300: Best 8.000, Avg 6.830
Gen 400: Best 8.535, Avg 7.147
Gen 499: Best 8.645, Avg 6.924
Best after 500 generations: ATGAATATTAACATTAGCACG (fitness=9.128)

Best evolved schedule:

- Model Training (30 pts, 5.0 hr)
- Email Summary (5 pts, 0.25 hr)
- Quick Health Check (3 pts, 0.1 hr)
- Email Summary (5 pts, 0.25 hr)
- Quick Health Check (3 pts, 0.1 hr)
- Unit Test Run (10 pts, 0.75 hr)
- Data Aggregation (12 pts, 1.0 hr)
  DNA sequence: ATGAATATTAACATTAGCACG
  Fitness: 9.128
