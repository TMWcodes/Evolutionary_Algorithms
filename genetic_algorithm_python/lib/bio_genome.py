import random
import lib.genome_fitness as gf
# from genetic_algorithm_python.lib.automation_fitness import AutomationFitness, AMINO_TASK_MAP
# from bio_auto_fitness import AutomationFitness
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

    def generate_ssDNA(self, length, ensure_start_stop=True):
        """Generate a random DNA sequence. Optionally enforce start/stop codons."""
        if length < 6:  # too short to add both codons
            return ''.join(random.choice("ATGC") for _ in range(length))

        if ensure_start_stop:
            middle_length = length - 6
            middle_seq = ''.join(random.choice("ATGC") for _ in range(middle_length))
            stop_codon = random.choice(["TAA", "TAG", "TGA"])
            return "ATG" + middle_seq + stop_codon
        else:
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
    # bio_genome.py (partial)
    def mutate(self, dna, p_m=0.01, max_mut_per_codon=1, allow_frameshift=False):
        """Codon-aware mutation with optional multiple changes per codon and frameshift."""
        bases = "ATGC"
        transitions = {"A":"G","G":"A","C":"T","T":"C"}
        dna_list = list(dna)
        
        for i in range(0, len(dna_list), 3):
            if random.random() < p_m:
                codon = dna_list[i:i+3]
                if not codon:
                    continue
                num_mut = max_mut_per_codon if max_mut_per_codon <= len(codon) else len(codon)
                for _ in range(num_mut):
                    pos = random.randrange(len(codon))
                    base = codon[pos]
                    if random.random() < 0.7:
                        codon[pos] = transitions[base]
                    else:
                        codon[pos] = random.choice([b for b in bases if b != base and b != transitions[base]])
                dna_list[i:i+3] = codon

        # Optional frameshift: randomly insert/delete 1 base at end with small probability
        if allow_frameshift and random.random() < p_m:
            if random.random() < 0.5 and len(dna_list) > 3:  # deletion
                dna_list.pop(random.randrange(len(dna_list)))
            else:  # insertion
                dna_list.insert(random.randrange(len(dna_list)+1), random.choice(bases))
                
        return ''.join(dna_list)

    # bio_genome.py (partial)
    def crossover(self, pair, p_c=0.7, homology_preserve=False):
        """Codon-aware recombination with optional homology preservation."""
        if len(pair) != 2:
            return pair
        c1, c2 = pair
        if random.random() > p_c:
            return [c1, c2]

        max_point = min(len(c1), len(c2))
        if max_point < 6:
            return [c1, c2]

        # Homology-aware: find a common motif to preserve
        if homology_preserve:
            motif_len = 3
            for i in range(len(c1)-motif_len+1):
                motif = c1[i:i+motif_len]
                if motif in c2:
                    point = i + motif_len
                    break
            else:
                point = random.randrange(3, max_point-3, 3)
        else:
            point = random.randrange(3, max_point-3, 3)

        return [c1[:point] + c2[point:], c2[:point] + c1[point:]]


    # ---------------- MODULAR EVOLUTION ----------------
    def run_evolution(
        self,
        fitness_func,
        length,
        population_size=20,
        p_c=0.7,
        p_m=0.01,
        iterations=100,
        use_frames=False,
        check_complement=False,
        normalized=False,   # <--- NEW FLAG
        verbose=True
    ):
        """
        Run evolution on sequences of given length using a provided fitness function.

        Args:
            fitness_func: function(dna) -> float
            length: length of DNA string
            population_size: number of individuals in population
            p_c: crossover probability
            p_m: mutation probability
            iterations: number of generations
            use_frames: evaluate max fitness across 6 reading frames
            check_complement: apply slight bonus/malus for complementary strand check
            normalized: if True, assumes max fitness = 1.0 and allows early stop
                        if False, runs all iterations and only tracks best-so-far
            verbose: print progress
        """
        population = [self.generate_ssDNA(length) for _ in range(population_size)]
        best_overall = None

        for gen in range(iterations):
            scored = []
            for dna in population:
                score = fitness_func(dna)

                if use_frames:
                    frames = self.translate_with_frame(dna)
                    frame_score = max(fitness_func(f) for f in frames)
                    score = max(score, frame_score)

                if check_complement:
                    score *= 1.05 if self.check_DNA(dna, dna) else 0.95

                scored.append({"dna": dna, "fitness": score})

            best_gen = max(scored, key=lambda x: x["fitness"])
            if not best_overall or best_gen["fitness"] > best_overall["fitness"]:
                best_overall = best_gen

            # ---- Verbose logging every 100 generations ----
            if verbose and (gen % 100 == 0 or gen == iterations - 1):
                avg_fit = sum(x["fitness"] for x in scored) / len(scored)
                print(f"Gen {gen}: Best {best_gen['fitness']:.3f}, Avg {avg_fit:.3f}")

            # ---- EARLY STOP ONLY IF NORMALIZED ----
            if normalized and best_gen["fitness"] >= 1.0:
                if verbose:
                    print(f"Perfect match at generation {gen}: {best_gen['dna']}")
                return best_gen

            # ----------------- SELECTION -----------------
            total_fit = sum(x["fitness"] for x in scored) or 1e-9
            probs = [x["fitness"] / total_fit for x in scored]
            cumulative, cumsum = [], 0
            for p in probs:
                cumsum += p
                cumulative.append(cumsum)

            selected = []
            for _ in range(population_size):
                r = random.random()
                for i, prob in enumerate(cumulative):
                    if r <= prob:
                        selected.append(scored[i]["dna"])
                        break
            if not selected:
                selected = [self.generate_ssDNA(length) for _ in range(population_size)]

            # ----------------- CROSSOVER -----------------
            pairs = [selected[i:i+2] for i in range(0, len(selected), 2)]
            offspring = []
            for pair in pairs:
                if len(pair) == 2:
                    offspring.extend(self.crossover(pair, p_c=p_c))
                else:
                    offspring.extend(pair)

            # ----------------- MUTATION -----------------
            population = [self.mutate(dna, p_m=p_m) for dna in offspring]

        if verbose:
            print(
                f"Best after {iterations} generations: "
                f"{best_overall['dna']} (fitness={best_overall['fitness']:.3f})"
            )
        return best_overall


# ---------------- DEMO ----------------
if __name__ == "__main__":
    genome = Genome()

   

    # target = "ATGCGTACGTTAGC"
    # length = len(target)

    # # DNA fitness run
    # genome.run_evolution(
    #     lambda dna: bf.dna_fitness(dna, target, genome),
    #     length,
    #     population_size=50,
    #     p_c=0.8,
    #     p_m=0.05,
    #     iterations=500
    # )

    # # Protein fitness run
    # target_protein = genome.protein(genome.dna_to_rna(target))
    # genome.run_evolution(
    #     lambda dna: bf.phenotype_fitness(dna, target_protein, genome),
    #     length,
    #     population_size=50,
    #     p_c=0.8,
    #     p_m=0.05,
    #     iterations=500
    # )
##########################

# af = AutomationFitness(amino_task_map=AMINO_TASK_MAP)
#  # -------------------------
# # Define DNA length (number of codons/tasks)
# # -------------------------
# length = 21  # 7 codons/tasks if 3 bases per codon

# # -------------------------
# # Wrap the automation fitness function
# # -------------------------
# automation_dna_fitness = lambda dna: af.automation_fitness(
#     genome.dna_to_rna(dna),  # convert DNA → RNA internally if needed
#     max_hours=8.0
# )

# # -------------------------
# # Run the genetic algorithm
# # -------------------------
# result = genome.run_evolution(
#     fitness_func=automation_dna_fitness,
#     length=length,
#     population_size=50,
#     p_c=0.8,
#     p_m=0.05,
#     iterations=500,
#     verbose=True
# )

# # -------------------------
# # Decode DNA → RNA → Protein → Tasks
# # -------------------------
# best_dna = result['dna']
# best_rna = genome.dna_to_rna(best_dna)
# best_protein = genome.protein(best_rna)
# best_tasks = af.protein_to_tasks(best_protein)

# # -------------------------
# # Print evolved schedule and sequences
# # -------------------------
# print("\nBest evolved schedule:")
# for task in best_tasks:
#     print(f" - {task[0]} ({task[1]} pts, {task[2]} hr)")

# print("\nSequence summary:")
# print(f"DNA sequence:     {best_dna}")
# print(f"RNA sequence:     {best_rna}")
# print(f"Protein sequence: {best_protein}")
# print(f"Fitness:          {result['fitness']:.3f}")
