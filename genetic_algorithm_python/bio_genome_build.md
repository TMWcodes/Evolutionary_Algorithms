# Biology

Biogenome

Dna read from 3 to 5
synthesize rna strand from 5 to 3.

## Use

a biological simulation: generating DNA/RNA strands, checking complementarity, reading frames, translating to amino acids.

experiment with genetic representations.

## Process - dna to rna to protien.

counting dna nucleotides
complementary dna
dna to rna
rna to protein

## transcription

sense transcript and an anti-sense transcript.

## translation

## dna replication

helicase - splits dna
dna polymarase - replicates strand of dna
reads both 3 to five and produces 5 to 3
ligase - glues strands together

## output

#### version 2

Perfect match at generation 63: ATGCGTACGTTAGC
Evolved result: {'dna': 'ATGCGTACGTTAGC', 'fitness': 1.0}

Best after 200 generations: ATGCGTACGTCAAG (fitness=0.79)
Evolved result: {'dna': 'ATGCGTACGTCAAG', 'fitness': 0.7857142857142857}

lost
def check_DNA(self, seq1, seq2):
def six_reading_frames(self, seq1, rseq2):
def translate_with_frame(self, dna, frames=[1,2,3,-1,-2,-3]):

```
   def check_DNA(self, seq1, seq2):
        """Check complementarity"""
        if len(seq1) >= len(seq2):
            strand2 = seq2[::-1]  # reverse
            strand2_check = seq1.translate(str.maketrans("ACTG", "TGAC"))
            return strand2 in strand2_check
        else:
            strand1 = seq1[::-1]
            strand1_check = seq2.translate(str.maketrans("ACTG", "TGAC"))
            return strand1 in strand1_check

    def six_reading_frames(self, seq1, rseq2):
        """Return six reading frames for DNA and its reverse complement"""
        output = []

        # forward frames
        f1 = ' '.join([seq1[i:i+3] for i in range(0, len(seq1), 3)])
        f2 = ' '.join([seq1[i:i+3] for i in range(1, len(seq1)-2, 3)])
        f3 = ' '.join([seq1[i:i+3] for i in range(2, len(seq1)-2, 3)])
        output.append("\n".join([f1, f2, f3]))

        # reverse complement frames
        r1 = ' '.join([rseq2[i:i+3] for i in range(0, len(rseq2), 3)])
        r2 = ' '.join([rseq2[i:i+3] for i in range(1, len(rseq2)-2, 3)])
        r3 = ' '.join([rseq2[i:i+3] for i in range(2, len(rseq2)-2, 3)])
        output.append("\n".join([r1, r2, r3]))

        return output

    def translate_with_frame(self, dna, frames=[1,2,3,-1,-2,-3]):
        """Translate DNA sequence into protein sequences for given frames"""
        if not dna:
            return ["" for _ in frames]

        def to_rna(seq): return seq.replace('T', 'U')

        forward = [to_rna(dna[i:]) for i in range(3)]
        reverse = [to_rna(self.complementary_DNA_strand(dna[::-1])[i:]) for i in range(3)]

        translations = []
        for seq in forward + reverse:
            codons = [seq[i:i+3] for i in range(0, len(seq)-2, 3)]
            aa_seq = ''.join(self.aminoacid_dict.get(c, '') for c in codons)
            translations.append(aa_seq)

        frame_map = {1:0, 2:1, 3:2, -1:3, -2:4, -3:5}
        return [translations[frame_map[f]] for f in frames]


```

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
