from lib.bio_genome import Genome
import math
import random

class HybridGenome(Genome):
    """
    Hybrid GA implementation that extends BioGenome but packs DNA into a binary
    representation internally. 

    Motivation:
    - BioGenome works directly with DNA strings ("ATGC...").
    - HybridGenome packs/unpacks these into binary, allowing us to test
      binary-style encodings while still leveraging BioGenome’s operators.

    Core idea:
    - Chromosomes are stored as packed bytes.
    - Before applying genetic operators, sequences are unpacked to strings.
    - After applying operators, results are repacked.
    """

    # Lookup tables: DNA base ↔ 2-bit encoding
    base_to_bits = {'A': 0b00, 'T': 0b01, 'G': 0b10, 'C': 0b11}
    bits_to_base = {v: k for k, v in base_to_bits.items()}

    # -------- PACKING / UNPACKING --------
    def pack(self, dna: str) -> bytes:
        """
        Convert ATGC string into packed binary form with length prefix.

        Format:
        - First 2 bytes: original DNA length (big endian).
        - Following bytes: DNA bases encoded as 2 bits each.
        """
        packed = 0
        for base in dna:
            packed = (packed << 2) | self.base_to_bits[base]
        length = len(dna)
        return length.to_bytes(2, "big") + packed.to_bytes(math.ceil(length / 4), "big")

    def unpack(self, data: bytes) -> str:
        """
        Convert packed binary back into ATGC string.
        Reads length prefix, then reconstructs bases from 2-bit encoding.
        """
        length = int.from_bytes(data[:2], "big")
        num = int.from_bytes(data[2:], "big")
        dna = []
        for _ in range(length):
            dna.append(self.bits_to_base[num & 0b11])
            num >>= 2
        return ''.join(reversed(dna))

    # -------- WRAPPED BIO OPERATORS --------
    # Each operator unpacks → applies BioGenome operator → repacks
    def mutate(self, packed_dna, **kwargs):
        dna = self.unpack(packed_dna)
        mutated = super().mutate(dna, **kwargs)
        return self.pack(mutated)

    def crossover(self, pair, **kwargs):
        d1, d2 = (self.unpack(p) for p in pair)
        offspring = super().crossover([d1, d2], **kwargs)
        return [self.pack(o) for o in offspring]

    def recombination(self, d1, d2, **kwargs):
        u1, u2 = self.unpack(d1), self.unpack(d2)
        o1, o2 = super().recombination(u1, u2, **kwargs)
        return self.pack(o1), self.pack(o2)

    def transposition(self, dna, **kwargs):
        return self.pack(super().transposition(self.unpack(dna), **kwargs))

    def local_duplication(self, dna, **kwargs):
        return self.pack(super().local_duplication(self.unpack(dna), **kwargs))

    def gene_duplication(self, dna, **kwargs):
        return self.pack(super().gene_duplication(self.unpack(dna), **kwargs))

    # -------- OVERRIDDEN RUN EVOLUTION --------
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
        """
        Evolutionary loop for HybridGenome.
        Differences from BioGenome:
        - Population consists of packed DNA sequences.
        - Fitness function is wrapped to unpack before scoring.
        - Operators unpack/repack automatically.

        Returns:
            dict with keys:
                "dna"     → best DNA sequence (string form)
                "fitness" → fitness of best sequence
                "history" → evolution log across generations
        """

        # --- Initial population (packed DNA) ---
        population = [self.pack(self.generate_ssDNA(length)) for _ in range(population_size)]

        # Wrap fitness to handle unpacked DNA
        def wrapped_fitness(packed_dna):
            return fitness_func(self.unpack(packed_dna))

        best_overall = None
        history = []

        for gen in range(iterations):
            # --- Evaluate population ---
            scored = [{"dna": dna, "fitness": wrapped_fitness(dna)} for dna in population]

            # Track best individual
            best_gen = max(scored, key=lambda x: x["fitness"])
            if not best_overall or best_gen["fitness"] > best_overall["fitness"]:
                best_overall = best_gen

            # Record stats
            avg_fit = sum(x["fitness"] for x in scored) / len(scored)
            history.append({
                "generation": gen,
                "gen_best": best_gen["fitness"],
                "running_best": best_overall["fitness"],
                "avg": avg_fit
            })

            # --- Early stop if normalized and perfect ---
            if normalized and best_gen["fitness"] >= 1.0:
                if verbose:
                    print(f"Perfect match at generation {gen}: {self.unpack(best_gen['dna'])}")
                return {
                    "dna": self.unpack(best_gen["dna"]),
                    "fitness": best_gen["fitness"],
                    "history": history
                }

            # --- Selection ---
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

            # --- Crossover ---
            pairs = [selected[i:i + 2] for i in range(0, len(selected), 2)]
            offspring = []
            for pair in pairs:
                if len(pair) == 2:
                    offspring.extend(self.crossover(pair, p_c=p_c))
                else:
                    offspring.extend(pair)

            # --- Structural operators ---
            next_gen = []
            for dna in offspring:
                if len(dna) > 60 and random.random() < 0.05:
                    dna = self.gene_duplication(dna)
                if random.random() < p_locdup:
                    dna = self.local_duplication(dna)
                if random.random() < p_transp:
                    dna = self.transposition(dna)
                next_gen.append(dna)

            # --- Recombination ---
            if len(next_gen) > 1 and random.random() < p_recomb:
                i, j = random.sample(range(len(next_gen)), 2)
                c1, c2 = self.recombination(next_gen[i], next_gen[j])
                next_gen[i], next_gen[j] = c1, c2

            # --- Mutation ---
            population = [self.mutate(dna, p_m=p_m) for dna in next_gen]

        # --- Return final best ---
        return {
            "dna": self.unpack(best_overall["dna"]),
            "fitness": best_overall["fitness"],
            "history": history
        }
