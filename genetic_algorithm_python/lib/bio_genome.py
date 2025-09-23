import random
import lib.genome_fitness as gf
from typing import Tuple


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
            'UAA':'*','UGA':'*','UAG':'*'
        }

    # ---------------- BIO FUNCTIONS ----------------

    def generate_ssDNA(self, length):
        """Generate random DNA with no enforced start/stop codons."""
        bases = ['A', 'T', 'G', 'C']
        return ''.join(random.choice(bases) for _ in range(length))

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

  
    @staticmethod
    def gene_duplication(dna: str, min_len: int = 30, max_len: int = 200) -> str:
        if len(dna) < min_len:
            return dna
        start = random.randint(0, len(dna) - min_len)
        length = random.randint(min_len, min(max_len, len(dna) - start))
        segment = dna[start:start+length]
        insert_pos = random.randint(0, len(dna))
        return dna[:insert_pos] + segment + dna[insert_pos:]
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

        # Skip crossover with probability 1-p_c
        if random.random() > p_c:
            return [c1, c2]

        max_point = min(len(c1), len(c2))
        if max_point < 6:  # too short to perform codon-aligned crossover
            return [c1, c2]

        min_point = 3
        max_rand = max_point - 3
        if homology_preserve:
            # Try to find a common motif to preserve
            for i in range(len(c1) - 2):
                motif = c1[i:i+3]
                if motif in c2:
                    point = i + 3
                    break
            else:
                # fallback if no motif found
                if min_point >= max_rand:
                    return [c1, c2]
                point = random.randrange(min_point, max_rand, 3)
        else:
            if min_point >= max_rand:
                return [c1, c2]
            point = random.randrange(min_point, max_rand, 3)

        # Perform codon-aligned crossover
        return [c1[:point] + c2[point:], c2[:point] + c1[point:]]
    
    @staticmethod
    def modular_crossover(dna1: str, dna2: str, module_size: int = 90) -> tuple[str, str]:
        # Cut into modules
        chunks1 = [dna1[i:i+module_size] for i in range(0, len(dna1), module_size)]
        chunks2 = [dna2[i:i+module_size] for i in range(0, len(dna2), module_size)]
        # Swap random modules
        if chunks1 and chunks2:
            i, j = random.randint(0, len(chunks1)-1), random.randint(0, len(chunks2)-1)
            chunks1[i], chunks2[j] = chunks2[j], chunks1[i]
        return ''.join(chunks1), ''.join(chunks2)

    @staticmethod
    def recombination(dna1: str, dna2: str, num_points: int = 2) -> tuple[str, str]:
        """Multi-point recombination between two DNA sequences."""
        if len(dna1) < num_points+1 or len(dna2) < num_points+1:
            return dna1, dna2

        cut_points = sorted(random.sample(range(1, min(len(dna1), len(dna2))), num_points))
        offspring1, offspring2 = "", ""
        toggle = True
        last = 0

        for cut in cut_points + [min(len(dna1), len(dna2))]:
            if toggle:
                offspring1 += dna1[last:cut]
                offspring2 += dna2[last:cut]
            else:
                offspring1 += dna2[last:cut]
                offspring2 += dna1[last:cut]
            toggle = not toggle
            last = cut

        return offspring1, offspring2
    
    @staticmethod
    def transposition(dna: str, min_len: int = 10, max_len: int = 100) -> str:
        """Randomly cut a segment and insert it elsewhere."""
        if len(dna) < min_len:
            return dna
        start = random.randint(0, len(dna) - min_len)
        length = random.randint(min_len, min(max_len, len(dna) - start))
        segment = dna[start:start+length]
        dna = dna[:start] + dna[start+length:]  # remove
        insert_pos = random.randint(0, len(dna))
        return dna[:insert_pos] + segment + dna[insert_pos:]
    
    @staticmethod
    def local_duplication(dna: str, min_len: int = 5, max_len: int = 50) -> str:
        """Duplicate a small segment in place."""
        if len(dna) < min_len:
            return dna
        start = random.randint(0, len(dna) - min_len)
        length = random.randint(min_len, min(max_len, len(dna) - start))
        segment = dna[start:start+length]
        return dna[:start+length] + segment + dna[start+length:]

    # ---------------- MODULAR EVOLUTION ----------------
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
        normalized: if True, early stop on perfect fitness
        verbose: print progress
    """

    def run_evolution(
        self,
        fitness_func,
        length,
        population_size=20,
        p_c=0.7,
        p_m=0.002,
        p_recomb=0.05,
        p_transp=0.02,
        p_locdup=0.02,
        iterations=100,
        use_frames=False,
        check_complement=False,
        normalized=False,
        verbose=False
):

    # Generate initial random population
        population = [self.generate_ssDNA(length) for _ in range(population_size)]
        scored = [{"dna": dna, "fitness": fitness_func(dna)} for dna in population]
        best_overall = max(scored, key=lambda x: x["fitness"])

        # History tracking
        history = []

        for gen in range(iterations):
            scored = []

            # Evaluate population
            for dna in population:
                score = fitness_func(dna)
                if use_frames:
                    frames = self.translate_with_frame(dna)
                    score = max(score, max(fitness_func(f) for f in frames))
                if check_complement:
                    score *= 1.05 if self.check_DNA(dna, dna) else 0.95
                scored.append({"dna": dna, "fitness": score})

            # Best in generation
            best_gen = max(scored, key=lambda x: x["fitness"])
            if best_gen["fitness"] > best_overall["fitness"]:
                best_overall = best_gen

            # Track stats
            avg_fit = sum(x["fitness"] for x in scored) / len(scored)
            history.append({
                "gen": gen,
                "gen_best": best_gen["fitness"],
                "running_best": best_overall["fitness"],
                "avg": avg_fit
            })

            # Optional verbose print
            

            # Early stop
            if normalized and best_gen["fitness"] >= 1.0:
                return {
                    "dna": best_overall["dna"],     # keeps backward compatibility
                    "fitness": best_overall["fitness"],
                    "history": history
                }

            # ----------------- SELECTION -----------------
            total_fit = sum(x["fitness"] for x in scored) or 1e-9
            probs = [x["fitness"] / total_fit for x in scored]
            cumulative = []
            cumsum = 0
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

            # ----------------- CROSSOVER & OPERATORS -----------------
            pairs = [selected[i:i+2] for i in range(0, len(selected), 2)]
            offspring = []
            for pair in pairs:
                if len(pair) == 2:
                    offspring.extend(self.crossover(pair, p_c=p_c))
                else:
                    offspring.extend(pair)

            next_gen = []
            for dna in offspring:
                if len(dna) > 60 and random.random() < 0.05:
                    dna = self.gene_duplication(dna)
                if random.random() < p_locdup:
                    dna = self.local_duplication(dna)
                if random.random() < p_transp:
                    dna = self.transposition(dna)
                next_gen.append(dna)

            if len(next_gen) > 1 and random.random() < p_recomb:
                i, j = random.sample(range(len(next_gen)), 2)
                child1, child2 = self.recombination(next_gen[i], next_gen[j])
                next_gen[i], next_gen[j] = child1, child2

            if len(next_gen) > 1 and max(len(d) for d in next_gen) > 90 and random.random() < 0.05:
                i, j = random.sample(range(len(next_gen)), 2)
                child1, child2 = self.modular_crossover(next_gen[i], next_gen[j])
                next_gen[i], next_gen[j] = child1, child2

            # ----------------- MUTATION -----------------
            population = [self.mutate(dna, p_m=p_m) for dna in next_gen]

        # Return best individual + history
        return {
            "dna": best_overall["dna"],     # backward compatible
            "fitness": best_overall["fitness"],
            "history": history
        }

