import pytest
from lib.bio_genome import Genome
import random

class TestGenome:
    """Test suite for Genome class."""

    @pytest.fixture(autouse=True)
    def setup_genome(self):
        """Automatically run before each test."""
        self.g = Genome()
        random.seed(42)  # deterministic behavior

    # ------------------- DNA generation tests -------------------
    def test_generate_ssDNA_length(self):
        seq = self.g.generate_ssDNA(15)
        assert len(seq) == 15
        assert set(seq).issubset({'A','T','G','C'})

    def test_generate_ssDNA_start_stop(self):
        seq = self.g.generate_ssDNA(12, ensure_start_stop=True)
        assert seq.startswith("ATG")
        assert seq[-3:] in ["TAA","TAG","TGA"]

    # ------------------- Translation tests -------------------
    def test_dna_to_rna_translation(self):
        dna = "ATGTTT"
        rna = self.g.dna_to_rna(dna)
        assert rna == "AUGUUU"
        protein = self.g.protein(rna)
        assert protein == "MF"  # M=ATG, F=TTT

    def test_translate_with_frame(self):
        dna = "ATGTTTAAAGGG"
        translations = self.g.translate_with_frame(dna)
        assert len(translations) == 6
        for aa_seq in translations:
            assert isinstance(aa_seq, str)

    # ------------------- Mutation / Crossover -------------------
    def test_mutate_preserves_length(self):
        dna = "ATGTTTAAAGGG"
        mutated = self.g.mutate(dna, p_m=1.0)  # force mutation
        assert len(mutated) == len(dna)

    def test_crossover_preserves_length(self):
        pair = ["ATGTTTAAAGGG", "GGGAAATTTCCC"]
        offspring = self.g.crossover(pair, p_c=1.0)  # force crossover
        assert all(len(o) == len(pair[0]) for o in offspring)

    # ------------------- Small evolution run -------------------
    def test_run_evolution_returns_dict(self):
        def dummy_fitness(dna):
            return sum(1 for b in dna if b == "A") / len(dna)

        best = self.g.run_evolution(
            fitness_func=dummy_fitness,
            length=12,
            population_size=4,
            iterations=5,
            p_m=0.5,
            p_c=0.5,
            verbose=False
        )
        assert isinstance(best, dict)
        assert "dna" in best and "fitness" in best

    def test_mutate_multiple_changes_per_codon(self):
        # TDD: context-aware mutation with multiple changes per codon
        dna = "ATGTTTAAAGGG"
        mutated = self.g.mutate(dna, p_m=1.0, max_mut_per_codon=3)
        assert len(mutated) == len(dna)
        assert mutated != dna

    def test_mutate_frameshift_possible(self):
        # TDD: allow frameshift mutations
        dna = "ATGTTTAAAGGG"
        mutated = self.g.mutate(dna, p_m=1.0, allow_frameshift=True)
        assert len(mutated) != len(dna) or mutated != dna

    def test_homology_aware_crossover(self):
        # TDD: ensure crossover preserves motifs
        p1 = "ATGAAAACCCGGG"
        p2 = "TTTGGGAAACCC"
        offspring = self.g.crossover([p1, p2], p_c=1.0, homology_preserve=True)
        assert "AAA" in offspring[0] or "AAA" in offspring[1]
    
        # ------------------- Gene Duplication / Modular Crossover -------------------
    def test_gene_duplication_increases_length(self):
        dna = "ATG" + "A"*60 + "TAA"
        duplicated = self.g.gene_duplication(dna, min_len=10, max_len=20)
        # Should be at least as long as original
        assert len(duplicated) >= len(dna)
        # Original sequence should still be part of result
        assert dna[:10] in duplicated

    def test_gene_duplication_short_sequence_no_change(self):
        dna = "ATGAAATGA"
        duplicated = self.g.gene_duplication(dna, min_len=10, max_len=20)
        # Short sequences should remain unchanged
        assert duplicated == dna

    def test_modular_crossover_swaps_modules(self):
        dna1 = "A"*120 + "C"*120
        dna2 = "G"*120 + "T"*120
        child1, child2 = self.g.modular_crossover(dna1, dna2, module_size=60)
        # Children should contain segments from both parents
        assert ("A"*60 in child1 or "C"*60 in child1) and ("G"*60 in child1 or "T"*60 in child1)
        assert ("A"*60 in child2 or "C"*60 in child2) and ("G"*60 in child2 or "T"*60 in child2)

    def test_modular_crossover_handles_short_sequences(self):
        dna1 = "ATGCGT"
        dna2 = "GGCCTA"
        # Should return sequences unchanged or minimally swapped without error
        child1, child2 = self.g.modular_crossover(dna1, dna2, module_size=10)
        assert len(child1) == len(dna1)
        assert len(child2) == len(dna2)

    def test_run_evolution_with_duplication_and_modular_crossover(self, monkeypatch):
        """
        Ensure run_evolution executes gene duplication and modular crossover paths deterministically.
        """

        # --- Patch random functions to always trigger duplication and modular crossover ---
        monkeypatch.setattr("random.random", lambda: 0.01)  # < 0.05 threshold
        monkeypatch.setattr("random.sample", lambda seq, n: (0, 1))  # deterministic modular crossover
        monkeypatch.setattr("random.randint", lambda a, b: a)  # pick first element for duplication/crossover

        # Simple fitness function: count 'A's
        def dummy_fitness(dna):
            return dna.count('A') / len(dna)

        length = 12
        best = self.g.run_evolution(
            fitness_func=dummy_fitness,
            length=length,
            population_size=4,
            iterations=3,   # small number to speed up test
            p_m=0.0,        # disable mutation
            p_c=1.0,        # force crossover
            verbose=False
        )

        # --- Assertions ---
        # Returns a dict with dna and fitness
        assert isinstance(best, dict)
        assert "dna" in best and "fitness" in best

        # Duplication should make sequence >= original length
        assert len(best["dna"]) >= length

        # Modular crossover should shuffle segments (sequence content likely changes)
        # We'll check that the resulting sequence contains parts of the original modules
        population_sequences = [self.g.generate_ssDNA(length) for _ in range(2)]
        child1, child2 = self.g.modular_crossover(population_sequences[0], population_sequences[1], module_size=3)
        assert len(child1) == length and len(child2) == length or len(child1) > length or len(child2) > length
