import random

class Genome:
    def __init__(self):
        self.aminoacid_dict = {
            'UUC':'F','UUU':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L',
            'AUU':'I','AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V','GUA':'V','GUG':'V',
            'UCU':'S','UCC':'S','UCA':'S','UCG':'S','AGU':'S','AGC':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
            'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A',
            'UAU':'Y','UAC':'Y','CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
            'AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D','GAC':'D','GAA':'E','GAG':'E',
            'UGU':'C','UGC':'C','UGG':'W','CGU':'R','CGC':'R','CGA':'R','CGG':'R','AGA':'R','AGG':'R',
            'GGU':'G','GGC':'G','GGA':'G','GGG':'G',
            'UAA':'Stop','UGA':'Stop','UAG':'Stop'
        }

    # ---------------- BIO FUNCTIONS ----------------

    def generate_ssDNA(self, length):
        return ''.join(random.choice("ATGC") for _ in range(length))

    def generate_rna(self, length):
        return ''.join(random.choice("AUGC") for _ in range(length))

    def cDNA(self, dna):
        mapping = str.maketrans("ATGC", "TACG")
        return dna.upper().translate(mapping)

    def dna_to_rna(self, dna):
        return dna.replace("T", "U")

    def protein(self, rna):
        codons = [rna[i:i+3] for i in range(0, len(rna)-2, 3)]
        return ''.join(self.aminoacid_dict.get(c, '') for c in codons)

    def check_DNA(self, seq1, seq2):
        if len(seq1) >= len(seq2):
            strand2 = seq2[::-1]
            strand2_check = seq1.translate(str.maketrans("ACTG", "TGAC"))
            return strand2 in strand2_check
        else:
            strand1 = seq1[::-1]
            strand1_check = seq2.translate(str.maketrans("ACTG", "TGAC"))
            return strand1 in strand1_check

    def six_reading_frames(self, seq1, rseq2):
        output = []
        # forward
        f1 = ' '.join([seq1[i:i+3] for i in range(0, len(seq1), 3)])
        f2 = ' '.join([seq1[i:i+3] for i in range(1, len(seq1)-2, 3)])
        f3 = ' '.join([seq1[i:i+3] for i in range(2, len(seq1)-2, 3)])
        output.append("\n".join([f1, f2, f3]))
        # reverse
        r1 = ' '.join([rseq2[i:i+3] for i in range(0, len(rseq2), 3)])
        r2 = ' '.join([rseq2[i:i+3] for i in range(1, len(rseq2)-2, 3)])
        r3 = ' '.join([rseq2[i:i+3] for i in range(2, len(rseq2)-2, 3)])
        output.append("\n".join([r1, r2, r3]))
        return output

    def translate_with_frame(self, dna, frames=[1,2,3,-1,-2,-3]):
        if not dna:
            return ["" for _ in frames]

        def to_rna(seq): return seq.replace('T', 'U')

        forward = [to_rna(dna[i:]) for i in range(3)]
        reverse = [to_rna(self.cDNA(dna[::-1])[i:]) for i in range(3)]

        translations = []
        for seq in forward + reverse:
            codons = [seq[i:i+3] for i in range(0, len(seq)-2, 3)]
            aa_seq = ''.join(self.aminoacid_dict.get(c, '') for c in codons)
            translations.append(aa_seq)

        frame_map = {1:0, 2:1, 3:2, -1:3, -2:4, -3:5}
        return [translations[frame_map[f]] for f in frames]

    # ---------------- EVOLUTIONARY FUNCTIONS ----------------

    def mutate(self, dna, p_m=0.01):
        """Codon-aware mutation: one base per codon, with transition bias"""
        bases = "ATGC"
        transitions = {"A":"G","G":"A","C":"T","T":"C"}
        dna_list = list(dna)

        for i in range(0, len(dna_list), 3):  # step codon by codon
            if random.random() < p_m:
                codon = dna_list[i:i+3]
                if not codon:
                    continue
                pos = random.randrange(len(codon))  # pick a base inside codon
                base = codon[pos]
                if random.random() < 0.7:  # transition
                    codon[pos] = transitions[base]
                else:  # transversion
                    codon[pos] = random.choice([b for b in bases if b != base and b != transitions[base]])
                dna_list[i:i+3] = codon
        return ''.join(dna_list)

    def crossover(self, pair, p_c=0.7):
        """Codon-aware recombination crossover (splits at multiples of 3)"""
        if len(pair) != 2:
            return pair
        c1, c2 = pair
        if random.random() > p_c:
            return [c1, c2]

        max_point = min(len(c1), len(c2))
        if max_point < 6:  # too short to cross
            return [c1, c2]

        point = random.randrange(3, max_point-3, 3)
        return [c1[:point] + c2[point:], c2[:point] + c1[point:]]

    def phenotype_fitness(self, dna, target_protein):
        """DNA -> RNA -> Protein, then compare to target protein"""
        rna = self.dna_to_rna(dna)
        protein = self.protein(rna)
        return sum(a == b for a, b in zip(protein, target_protein)) / max(len(target_protein), 1)

    def dna_fitness(self, candidate, target_dna):
        """Evaluate DNA with biological constraints, with a fitness floor."""
        length_penalty = abs(len(candidate) - len(target_dna)) / len(target_dna)
        start_penalty = 0 if candidate.startswith("ATG") else 0.3
        stop_codons = {"TAA", "TAG", "TGA"}
        stop_penalty = 0 if candidate[-3:] in stop_codons else 0.3

        match_score = sum(a == b for a, b in zip(candidate, target_dna)) / len(target_dna)
        target_protein = self.protein(self.dna_to_rna(target_dna))
        candidate_protein = self.protein(self.dna_to_rna(candidate))
        pheno_score = sum(a == b for a, b in zip(candidate_protein, target_protein)) / max(len(target_protein), 1)

        fitness = (0.5 * match_score + 0.5 * pheno_score)
        fitness -= (length_penalty + start_penalty + stop_penalty)

        return max(0.01, fitness)  # fitness floor

    def run_evolution(self, target, population_size=10, p_c=0.7, p_m=0.01, iterations=100):
        """
        Evolve a population of DNA sequences toward a target sequence (DNA or protein).

        Parameters:
        - target: str
            Target sequence. If it contains only A/T/G/C, treated as DNA.
            Otherwise, treated as a protein sequence.
        - population_size: int
            Number of sequences per generation.
        - p_c: float
            Probability of performing crossover between pairs.
        - p_m: float
            Probability of mutating a base (codon-aware).
        - iterations: int
            Number of generations to run.

        Notes:
        - Fitness function is either:
            * Fraction of matching nucleotides (DNA target)
            * Fraction of matching amino acids after DNA -> RNA -> Protein (protein target)
        - Mutation is codon-aware with transition bias.
        - Crossover occurs at codon boundaries.
        - Fitness floor ensures population never becomes empty.
        """

        # Determine if target is DNA or protein
        dna_mode = all(base in "ATGC" for base in target)
        if dna_mode:
            target_dna = target
            target_protein = self.protein(self.dna_to_rna(target))  # for phenotype scoring
        else:
            target_dna = None
            target_protein = target

        # Estimate DNA length: if protein target, each amino acid = 3 bases
        length = len(target if dna_mode else target_protein) * 3

        # Generate initial population of random DNA sequences
        population = [self.generate_ssDNA(length) for _ in range(population_size)]

        for generation in range(iterations):
            scored = []  # list of dictionaries: {"dna": ..., "fitness": ...}

            # Evaluate fitness for each individual
            for dna in population:
                if dna_mode:
                    # DNA fitness: nucleotide match + phenotype check
                    fit = self.dna_fitness(dna, target_dna)
                else:
                    # Protein fitness: DNA -> RNA -> Protein -> compare to target protein
                    fit = self.phenotype_fitness(dna, target_protein)
                scored.append({"dna": dna, "fitness": fit})

            # Safety: if population somehow empty, regenerate
            if not scored:
                population = [self.generate_ssDNA(length) for _ in range(population_size)]
                continue

            # Select the best candidate in the current generation
            best = max(scored, key=lambda x: x["fitness"])

            # If perfect match is found, stop evolution early
            if best["fitness"] >= 1.0:
                print(f"Perfect match at generation {generation}: {best['dna']}")
                return best

            # ----------------- SELECTION -----------------
            # Roulette wheel selection based on fitness
            total_fit = sum(x["fitness"] for x in scored) or 1e-9  # avoid division by zero
            probs = [x["fitness"]/total_fit for x in scored]

            # Build cumulative probabilities for selection
            cumulative, cumsum = [], 0
            for p in probs:
                cumsum += p
                cumulative.append(cumsum)

            # Select individuals for next generation
            selected = []
            for _ in range(population_size):
                r = random.random()
                for i, prob in enumerate(cumulative):
                    if r <= prob:
                        selected.append(scored[i]["dna"])
                        break

            # Safety: if selection failed, regenerate population
            if not selected:
                selected = [self.generate_ssDNA(length) for _ in range(population_size)]

            # ----------------- CROSSOVER -----------------
            # Pair up selected sequences and perform codon-aware crossover
            pairs = [selected[i:i+2] for i in range(0, len(selected), 2)]
            offspring = []
            for pair in pairs:
                if len(pair) == 2:
                    offspring.extend(self.crossover(pair, p_c=p_c))
                else:
                    # Odd number of individuals: carry forward without crossover
                    offspring.extend(pair)

            # ----------------- MUTATION -----------------
            # Apply codon-aware mutation to each offspring
            population = [self.mutate(dna, p_m=p_m) for dna in offspring]

            # Optional: log best fitness for monitoring
            # print(f"Generation {generation}: Best fitness = {best['fitness']:.3f}")

        # Return the best sequence after all generations
        print(f"Best after {iterations} generations: {best['dna']} (fitness={best['fitness']:.2f})")
        return best


# ---------------- DEMO ----------------
if __name__ == "__main__":
    g = Genome()

   # DNA target (keep short-ish for demonstration)
target_dna = "ATGCGTACGTTAGC"
g.run_evolution(
    target_dna,
    population_size=50,   # larger population → more diversity
    p_c=0.8,             # crossover probability stays high
    p_m=0.05,            # higher mutation → faster exploration
    iterations=500       # more generations to allow convergence
)

# # Protein target
# target_protein = "MVP"  # (Met-Val-Pro)
# g.run_evolution(
#     target_protein,
#     population_size=60,   # more candidates
#     p_c=0.8,
#     p_m=0.08,             # higher mutation for short protein→DNA mapping
#     iterations=400        # enough iterations to converge on target
# )