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

# Dependancies

```
automation_fitness.py:
  ← collections
  ← math
  ← typing
binary_genome.py:
  ← random
bio_genome.py:
  ← lib.genome_fitness
  ← random
  ← typing
compare_main.py:
  ← lib.automation_fitness
  ← lib.compare_results
  ← lib.reporting
  ← lib.run_bio_ga
compare_results.py:
  ← lib.automation_fitness
  ← lib.binary_genome
  ← lib.bio_genome
  ← lib.hybrid_genome
  ← lib.knapsack
fitness_wrappers.py:
  ← lib
hybrid_genome.py:
  ← lib.bio_genome
  ← math
  ← random
knapsack.py:
  ← lib
  ← lib.automation_fitness
reporting.py:
  ← collections
run_bio_ga.py:
  ← collections
  ← lib.automation_fitness
  ← lib.bio_genome
  ← lib.fitness_wrappers
  ← lib.genome_fitness
  ← lib.reporting
  ← random
Dependency graph saved to full_lib_graph.png
```

# Directory tree

```
 ./
    binary_genome_build.md
    bio_genome_build.md
    combined_graph.png
    compare_main_graph.png
    full_lib_graph.png
    structure.txt
    synth_graph.png
lib/
    automation_fitness.py
    binary_genome.py
    bio_genome.py
    compare_main.py
    compare_results.py
    fitness_wrappers.py
    genome_fitness.py
    hybrid_genome.py
    knapsack.py
    reporting.py
    run_bio_ga.py
    __init__.py
tests/
    test_automation_fitness.py
    test_automation_fitness_integration.py
    test_automation_sequences.py
    test_bio_genome.py
    test_genome_edge_cases.py
    test_genome_fitness.py
    test_genome_fitness_integration.py
    test_hybrid_genome.py
    test_knapsack.py
    _init_.py
```

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

### version 9 (big refactor + testing)

Gen 0: Best 0.542, Avg 0.347
Gen 100: Best 0.900, Avg 0.692
Gen 199: Best 0.900, Avg 0.661
Best after 200 generations: ATGTTTAAAGGG (fitness=0.900)
Best sequence: ATGTTTAAAGGG
Fitness: 0.9

### version 10

added best seq print
Gen 0: Best 0.583, Avg 0.348, Best Seq: ATGTCTAAATAA
Gen 100: Best 0.858, Avg 0.641, Best Seq: ATGTTTAAAGGC
Gen 199: Best 0.900, Avg 0.694, Best Seq: ATGTTTAAAGGG
Best after 200 generations: ATGTTTAAAGGG (fitness=0.900)
Best sequence: ATGTTTAAAGGG
Fitness: 0.9

### version 11

Gen 0: Best 0.583, Avg 0.362, Best Seq: ATGGTAAAATGA
Gen 100: Best 0.692, Avg 0.633, Best Seq: ATGATTAAGGGG
Gen 199: Best 0.733, Avg 0.725, Best Seq: ATGCTTAAAGGG
Best after 200 generations: ATGTTTAAGGGG (fitness=0.858)

Best DNA sequence: ATGTTTAAGGGG
Fitness: 0.858
Best protein (phenotype): MFKG

### version 12

Gen 0: Best 0.625, Avg 0.341, Best Seq: ATGTTTGAATAG
Gen 100: Best 0.858, Avg 0.656, Best Seq: ATGTTTAAGGGG
Gen 199: Best 0.900, Avg 0.724, Best Seq: ATGTTTAAAGGG
Best after 200 generations: ATGTTTAAAGGG (fitness=0.900)

--- GA Result ---
Target DNA sequence: ATGTTTAAAGGG
Best DNA sequence: ATGTTTAAAGGG

Target protein: MFKG
Best protein: MFKG

Final fitness: 0.900

### version 13

Gen 0: Best 0.542, Avg 0.344, Best Seq: ATGTTCTGATAG
Gen 100: Best 0.750, Avg 0.673, Best Seq: ATGTTTAAGTGA
Gen 199: Best 0.817, Avg 0.699, Best Seq: ATGTTTAAGGGA
Best after 200 generations: ATGTTTAAGGGG (fitness=0.858)

--- GA Result ---
Target DNA sequence: ATGTTTAAAGGG
Best DNA sequence: ATGTTTAAGGGG

Target protein: MFKG
Best protein: MFKG

DNA fitness: 0.917
Protein fitness: 1.000
Combined fitness: 0.858

### Version 14 (Long genome tests)

tested at high character number 5400 (tiny genome - microvirus MP11 5517.)
50 population - 200 runs
--- GA Result ---
DNA fitness: 0.260
Protein fitness: 0.072
Combined fitness: 0.166

50 population - 500 runs.

--- GA Result ---
DNA fitness: 0.261
Protein fitness: 0.066
Combined fitness: 0.163

with such a small population, the GA explores only a fraction.
GA quickly converges on mediocre local optima.
Evolutionary runs on larger genomes often require tens of thousands of generations.

add gene duplication and modular crossover methods

### version 15

20 pop, 200 gen
added gene duplication and modular crossover methods
--- GA Result ---
DNA fitness: 0.261
Protein fitness: 0.070
Combined fitness: 0.165

200 pop, 200 gen (run time 1m)
--- GA Result ---
DNA fitness: 0.273
Protein fitness: 0.079
Combined fitness: 0.176

more population wont do much
problem isn’t computational power — it’s the combinatorial complexity.

establish
Current GA performance vs genome size
Variability with mutation rate and population size
How often valid proteins are produced

test
Population diversity
Number of modular events applied
Average fitness impact of events

increased mutation to 5%
20 population, 200 gens
--- GA Result ---
DNA fitness: 0.269
Protein fitness: 0.063
Combined fitness: 0.166

20 gens, 200 population
--- GA Result ---
DNA fitness: 0.277
Protein fitness: 0.068
Combined fitness: 0.173

at 20, 200, 10% mutations
DNA fitness: 0.269
Protein fitness: 0.063
Combined fitness: 0.166

50, 1000, 10%
--- GA Result ---
DNA fitness: 0.263
Protein fitness: 0.072
Combined fitness: 0.168

Even at 10% per codon, random mutations in very long sequences (~5,000 bases) mostly introduce noise rather than functional improvements.

### version 16

long sequence
with Local duplications, Transpositions, Recombination.
100 pop, 2000, gen
DNA fitness: 0.276
Protein fitness: 0.075
Combined fitness: 0.176

### version 1 (auto_fitness)

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

### version 2 (bio accurate)

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

### version 3

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

### version 4

ithm_python> python -m lib.run_bio_ga
Gen 0: Best 0.010, Avg 0.010, Best Seq: ATGAAGGATTAAAGGGCAGCACGGAACTAA
Gen 100: Best 0.010, Avg 0.010, Best Seq: CTGGAGTTGCCTAATGCGGTGTTAGCATAA
Gen 199: Best 0.010, Avg 0.010, Best Seq: CTAGGCTTGCCCCACGCGACATTGGCATGG
Best after 200 generations: ATGAAGGATTAAAGGGCAGCACGGAACTAA (fitness=0.010)

--- Automation GA Result ---
Best DNA sequence: ATGAAGGATTAAAGGGCAGCACGGAACTAA
Translated RNA seq: AUGAAGGAUUAAAGGGCAGCACGGAACUAA
Translated protein:
Task list: []
Automation fitness: 0.010

### version 5

Gen 0: Best 0.771, Avg 0.438, Best Seq: ATGTGCTTGTGAGGTAGACAGCCGGACTAG
Gen 100: Best 0.771, Avg 0.753, Best Seq: ATGTCATCCTGATCTTGGCGACTTCATTAG
Gen 199: Best 0.800, Avg 0.783, Best Seq: ATGTTGTCATGATTCCGGCAACTTAATTAG
Best after 200 generations: ATGTTGTTATGATTCCGACAACTTCATTAG (fitness=0.825)

--- Automation GA Result ---
Best DNA sequence: ATGTTGTTATGATTCCGACAACTTCATTAG
Translated RNA seq: AUGUUGUUAUGAUUCCGACAACUUCAUUAG
Translated protein: MLL*FRQLH*
Task list: [('Model Training', 30, 5.0), ('Deploy Script', 18, 1.5), ('Deploy Script', 18, 1.5)]
Automation fitness: 0.825

### version 6

```
Gen 0: Best 0.070, Avg 0.048
Gen 100: Best 0.292, Avg 0.235
Gen 200: Best 0.366, Avg 0.309
Gen 300: Best 0.334, Avg 0.294
Gen 400: Best 0.269, Avg 0.231
Gen 499: Best 0.293, Avg 0.264
Best after 500 generations:(fitness=0.394)

--- Automation GA Result ---
Translated protein: ANTKPDNQLNLTGLAPRQLAAQTNPLQQKKQDSLMSKLAKLISPILTLTNPYLKQTCRQKQDSLKLILT**TR*CQTATTANVRLLATKLPTLAKLILT*LDYLPPNLPNSSFATPRQA*LDYSTTNPYHNLT

Total amino acids in translated protein: 128

Task Schedule:
Idx  Task                      Pts   Time(min)  Cum.Time(min) Cum.Pts
---------------------------------------------------------------------------
1    Log Analysis              9     10.0       10.0         9.0
2    Unit Test Run             10    15.0       25.0         19.0
3    DB Sync                   20    25.0       50.0         39.0
4    Email Parsing             6     10.0       60.0         45.0
5    User Report Gen           14    15.0       75.0         59.0
6    Data Cleanup              10    15.0       90.0         69.0
7    Unit Test Run             10    15.0       105.0        79.0
8    Quick Health Check        3     10.0       115.0        82.0
9    Deploy Script             18    15.0       130.0        100.0
10   Unit Test Run             10    15.0       145.0        110.0
11   Deploy Script             18    15.0       160.0        128.0
12   DB Sync                   20    25.0       185.0        148.0
13   Data Aggregation          12    15.0       200.0        160.0
14   Deploy Script             18    15.0       215.0        178.0
15   Log Analysis              9     10.0       225.0        187.0
16   User Report Gen           14    15.0       240.0        201.0
17   Report Generation         15    20.0       260.0        216.0
18   Quick Health Check        3     10.0       270.0        219.0
19   Deploy Script             18    15.0       285.0        237.0
20   Log Analysis              9     10.0       295.0        246.0
21   Log Analysis              9     10.0       305.0        255.0
23   DB Sync                   20    25.0       340.0        278.0
24   Unit Test Run             10    15.0       355.0        288.0
25   User Report Gen           14    15.0       370.0        302.0
26   Deploy Script             18    15.0       385.0        320.0
27   Quick Health Check        3     10.0       395.0        323.0
28   Quick Health Check        3     10.0       405.0        326.0
29   Email Parsing             6     10.0       415.0        332.0
30   Email Parsing             6     10.0       425.0        338.0
31   Quick Health Check        3     10.0       435.0        341.0
32   Data Cleanup              10    15.0       450.0        351.0
33   Web Scraping              12    15.0       465.0        363.0
34   Deploy Script             18    15.0       480.0        381.0

Total points: 381.0
Final cumulative time (minutes): 480.0

Automation fitness: 0.394
```

Cycling top 6 tasks would have been 507 points

### version 7

adding run specs

```
Gen 0: Best 0.083, Avg 0.054
Gen 100: Best 0.304, Avg 0.265
Gen 200: Best 0.370, Avg 0.306
Gen 300: Best 0.363, Avg 0.308
Gen 400: Best 0.385, Avg 0.300
Gen 499: Best 0.421, Avg 0.376

--- GA Run Specs ---
Population size: 20, Generations: 500
p_c=0.7, p_m=0.002, p_recomb=0.05, p_transp=0.02, p_locdup=0.02
use_frames=False, check_complement=False, normalized=False

Best after 500 generations: fitness=0.451
Translated protein: APHRSIV*QCYFEDPKTMSFMLF*GLND*RLTN
Total amino acids in translated protein: 33

Task Schedule:
Idx  Task                      Pts   Time(min)  Cum.Time(min) Cum.Pts
---------------------------------------------------------------------------
1    Log Analysis              9     10.0       10.0         9.0
2    User Report Gen           14    15.0       25.0         23.0
3    API Health Check          8     10.0       35.0         31.0
4    Report Generation         15    20.0       55.0         46.0
5    Web Scraping              12    15.0       70.0         58.0
6    Code Linting              4     10.0       80.0         62.0
7    System Audit              16    20.0       100.0        78.0
8    Quick Health Check        3     10.0       110.0        81.0
9    Cache Clean               6     10.0       120.0        87.0
10   Data Normalization        11    15.0       135.0        98.0
11   Database Migration        25    20.0       155.0        123.0
12   Email Summary             5     10.0       165.0        128.0
13   Data Cleanup              10    15.0       180.0        138.0
14   User Report Gen           14    15.0       195.0        152.0
15   Email Parsing             6     10.0       205.0        158.0
16   DB Sync                   20    25.0       230.0        178.0
17   Model Training            30    25.0       255.0        208.0
18   Web Scraping              12    15.0       270.0        220.0
19   Database Migration        25    20.0       290.0        245.0
20   Model Training            30    25.0       315.0        275.0
21   Deploy Script             18    15.0       330.0        293.0
22   Database Migration        25    20.0       350.0        318.0
23   Data Aggregation          12    15.0       365.0        330.0
24   Deploy Script             18    15.0       380.0        348.0
25   Unit Test Run             10    15.0       395.0        358.0
26   Data Cleanup              10    15.0       410.0        368.0
27   Report Generation         15    20.0       430.0        383.0
28   Deploy Script             18    15.0       445.0        401.0
29   DB Sync                   20    25.0       470.0        421.0

Total points: 421.0
Final cumulative time (minutes): 470.0

```

### version 8

```
Gen 000: Gen Best 0.105, Running Best 0.105, Avg 0.054
Gen 100: Gen Best 0.387, Running Best 0.417, Avg 0.335
Gen 200: Gen Best 0.461, Running Best 0.481, Avg 0.386
Gen 300: Gen Best 0.450, Running Best 0.483, Avg 0.345
Gen 400: Gen Best 0.441, Running Best 0.483, Avg 0.355
Gen 500: Gen Best 0.435, Running Best 0.483, Avg 0.356
Gen 600: Gen Best 0.454, Running Best 0.483, Avg 0.335
Gen 700: Gen Best 0.432, Running Best 0.483, Avg 0.344
Gen 800: Gen Best 0.432, Running Best 0.483, Avg 0.345
Gen 900: Gen Best 0.407, Running Best 0.483, Avg 0.328
Gen 999: Gen Best 0.487, Running Best 0.507, Avg 0.384

--- GA Run Specs ---
Population size: 100, Generations: 1000
p_c=0.7, p_m=0.002, p_recomb=0.05, p_transp=0.02, p_locdup=0.02
use_frames=True, check_complement=True, normalized=True

Best after 1000 generations: fitness=0.507
Translated protein: VPSTMPKQCLREFTFYM*GMNIAMFS*D*WHL
Total amino acids in translated protein: 32

Task Schedule:
Idx  Task                      Pts   Time(min)  Cum.Time(min) Cum.Pts
---------------------------------------------------------------------------
1    System Audit              16    20.0       20.0         16.0
2    User Report Gen           14    15.0       35.0         30.0
3    Web Scraping              12    15.0       50.0         42.0
4    DB Sync                   20    25.0       75.0         62.0
5    Model Training            30    25.0       100.0        92.0
6    User Report Gen           14    15.0       115.0        106.0
7    Email Parsing             6     10.0       125.0        112.0
8    Quick Health Check        3     10.0       135.0        115.0
9    Cache Clean               6     10.0       145.0        121.0
10   Deploy Script             18    15.0       160.0        139.0
11   Report Generation         15    20.0       180.0        154.0
12   Email Summary             5     10.0       190.0        159.0
13   Database Migration        25    20.0       210.0        184.0
15   Database Migration        25    20.0       255.0        229.0
16   Data Normalization        11    15.0       270.0        240.0
17   Model Training            30    25.0       295.0        270.0
18   Data Aggregation          12    15.0       310.0        282.0
19   Model Training            30    25.0       335.0        312.0
20   Unit Test Run             10    15.0       350.0        322.0
21   Code Linting              4     10.0       360.0        326.0
22   Log Analysis              9     10.0       370.0        335.0
23   Model Training            30    25.0       395.0        365.0
24   Database Migration        25    20.0       415.0        390.0
25   Web Scraping              12    15.0       430.0        402.0
26   Data Cleanup              10    15.0       445.0        412.0
27   Backup Verification       9     15.0       460.0        421.0
28   API Health Check          8     10.0       470.0        429.0

Total points: 429.0
Final cumulative time (hrs): 7.833333333333333


====
```

### version 9

with prints of duplicates and uniques

```
Gen 000: Gen Best 0.110, Running Best 0.110, Avg 0.053
Gen 100: Gen Best 0.409, Running Best 0.456, Avg 0.328
Gen 200: Gen Best 0.410, Running Best 0.460, Avg 0.320
Gen 300: Gen Best 0.484, Running Best 0.484, Avg 0.336
Gen 400: Gen Best 0.459, Running Best 0.489, Avg 0.353
Gen 500: Gen Best 0.440, Running Best 0.501, Avg 0.344
Gen 600: Gen Best 0.432, Running Best 0.501, Avg 0.333
Gen 700: Gen Best 0.410, Running Best 0.501, Avg 0.336
Gen 800: Gen Best 0.454, Running Best 0.501, Avg 0.373
Gen 900: Gen Best 0.466, Running Best 0.501, Avg 0.357
Gen 999: Gen Best 0.442, Running Best 0.501, Avg 0.359

--- GA Run Specs ---
Population size: 100, Generations: 1000
p_c=0.7, p_m=0.002, p_recomb=0.05, p_transp=0.02, p_locdup=0.02
use_frames=True, check_complement=True, normalized=False

Best after 1000 generations: fitness=0.501
Translated protein: MWHNGVMIMLLSYDQVA**PMFK*TFM*RET
Total amino acids in translated protein: 31

Task Schedule:
Idx  Task                      Pts   Time(min)  Cum.Time(min) Cum.Pts
---------------------------------------------------------------------------
1    Model Training            30    25.0       25.0         30.0
2    Backup Verification       9     15.0       40.0         39.0
3    API Health Check          8     10.0       50.0         47.0
4    Unit Test Run             10    15.0       65.0         57.0
5    Data Aggregation          12    15.0       80.0         69.0
6    System Audit              16    20.0       100.0        85.0
7    Model Training            30    25.0       125.0        115.0
8    Code Linting              4     10.0       135.0        119.0
9    Model Training            30    25.0       160.0        149.0
10   Deploy Script             18    15.0       175.0        167.0
11   Deploy Script             18    15.0       190.0        185.0
12   Web Scraping              12    15.0       205.0        197.0
13   Data Normalization        11    15.0       220.0        208.0
14   Data Cleanup              10    15.0       235.0        218.0
15   Quick Health Check        3     10.0       245.0        221.0
16   System Audit              16    20.0       265.0        237.0
17   Log Analysis              9     10.0       275.0        246.0
18   User Report Gen           14    15.0       290.0        260.0
19   Model Training            30    25.0       315.0        290.0
20   Database Migration        25    20.0       335.0        315.0
21   Email Parsing             6     10.0       345.0        321.0
22   DB Sync                   20    25.0       370.0        341.0
23   Database Migration        25    20.0       390.0        366.0
24   Model Training            30    25.0       415.0        396.0
25   Report Generation         15    20.0       435.0        411.0
26   Email Summary             5     10.0       445.0        416.0
27   DB Sync                   20    25.0       470.0        436.0

Total points: 436.0
Final cumulative time (hrs): 7.833333333333333
Number of unique tasks: 19
Most duplicated task: 'Model Training' appears 5 times
```

# combined

(run_bio_ga.py)

### version 1

en 0: Best 0.417, Avg 0.342, Best Seq: ATGTTAGGATGA
Gen 100: Best 0.625, Avg 0.551, Best Seq: ATGTTTCAATGA
Gen 199: Best 0.792, Avg 0.783, Best Seq: ATGTTTAAATAG
Best after 200 generations: ATGTTTAAATAG (fitness=0.792)

--- GA Result ---
Target DNA sequence: ATGTTTAAAGGG
Best DNA sequence: ATGTTTAAATAG

Target protein: MFKG
Best protein: MFK\*

DNA fitness: 0.833
Protein fitness: 0.750
Combined fitness: 0.792
Gen 0: Best 0.700, Avg 0.425, Best Seq: ATGTCTTAACCCATGCTAACCCAGCCCTAA
Gen 100: Best 0.456, Avg 0.427, Best Seq: ATGAGCCTAGCGAGTTCAGTTGAATAGCAG
Gen 199: Best 0.461, Avg 0.445, Best Seq: ATGAATCCCGGAAGTCAAGTCGAATCTCAA
Best after 200 generations: ATGTCTTAACCCATGCTAACCCAGCCCTAA (fitness=0.700)

--- Automation GA Result ---
Best DNA sequence: ATGTCTTAACCCATGCTAACCCAGCCCTAA
Translated RNA seq: AUGUCUUAACCCAUGCUAACCCAGCCCUAA
Translated protein: MS*PMLTQP*
Task list: [('Model Training', 30, 5.0), ('Web Scraping', 12, 1.0)]  
Automation fitness: 0.700

### version 2

So now your GA is evolving proteins that:
✅ Start with M (start amino acid).
✅ Avoid too many stops.
✅ Avoid redundant repeat tasks.
✅ Still balance total points vs. time.

Gen 0: Best 0.850, Avg 0.366, Best Seq: ATGATAGAGAGCTACTGCTGAACACGTACAGCGATCCTGTATGATCGTAG
Gen 100: Best 0.850, Avg 0.829, Best Seq: ATGATTGAAAGCTACTGCTGAAGTGCACACTCAGCTGAGATCTATGGCAG
Gen 199: Best 0.890, Avg 0.788, Best Seq: ATGATTGAAAATTACTGGTGAACTGCACACTCAACTGAGCTCTACGGCGG
Best after 200 generations: ATGATTGAAAATCACTGGTGAAGTGCACACTCAACTGAGCTCTACGGCGG (fitness=0.910)

--- Automation GA Result ---
Best DNA sequence: ATGATTGAAAATCACTGGTGAAGTGCACACTCAACTGAGCTCTACGGCGG
Translated RNA seq: AUGAUUGAAAAUCACUGGUGAAGUGCACACUCAACUGAGCUCUACGGCGG
Translated protein: MIENHW\*SAHSTELYG
Task list: [('Model Training', 30, 5.0), ('Code Linting', 4, 0.25), ('Email Summary', 5, 0.25), ('Unit Test Run', 10, 0.75), ('API Health Check', 8, 0.5), ('Backup Verification', 9, 0.5)]
Automation fitness: 0.910
