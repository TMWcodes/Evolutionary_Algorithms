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