# tests/test_genome_edge_cases.py
import pytest
from lib.bio_genome import Genome
from lib import genome_fitness as gf

class TestGenomeEdgeCases:
    @pytest.fixture(autouse=True)
    def setup_genome(self):
        self.g = Genome()
        self.target_dna = "ATGTTTAAAGGG"
        self.target_protein = self.g.protein(self.g.dna_to_rna(self.target_dna))

    # --- Helper wrapper ---
    def fitness_wrapper(self, dna, target_dna=None, **kwargs):
        """Return only combined fitness to be compatible with old tests"""
        if target_dna is None:
            target_dna = self.target_dna
        result = gf.dna_fitness(dna, target_dna, self.g, **kwargs)
        if isinstance(result, tuple):
            return result[2]  # combined fitness
        return result

    # ------------------- DNA length edge cases -------------------
    def test_short_sequence(self):
        short_dna = "ATG"
        score = self.fitness_wrapper(short_dna)
        assert 0.01 <= score <= 1.0

    def test_long_sequence(self):
        long_dna = "ATG" + "A" * 1000 + "TAA"
        score = self.fitness_wrapper(long_dna, target_dna=long_dna)
        assert 0.0 <= score <= 1.0

    # ------------------- Sequence content -------------------
    def test_only_one_base(self):
        dna = "A" * len(self.target_dna)
        score = self.fitness_wrapper(dna)
        assert 0.0 <= score <= 1.0

    def test_missing_start_or_stop(self):
        dna_no_start = "TTTAAAGGG"
        dna_no_stop = "ATGTTTAAA"
        score1 = self.fitness_wrapper(dna_no_start)
        score2 = self.fitness_wrapper(dna_no_stop)
        assert score1 < 1.0
        assert score2 < 1.0

    # ------------------- GA parameters -------------------
    def test_no_mutation(self):
        best = self.g.run_evolution(
            fitness_func=self.fitness_wrapper,
            length=len(self.target_dna),
            population_size=5,
            iterations=10,
            p_m=0.0,
            p_c=0.7,
            verbose=False
        )
        assert isinstance(best, dict)
        assert "dna" in best
        assert "fitness" in best

    def test_no_crossover(self):
        best = self.g.run_evolution(
            fitness_func=self.fitness_wrapper,
            length=len(self.target_dna),
            population_size=5,
            iterations=10,
            p_m=0.1,
            p_c=0.0,
            verbose=False
        )
        assert isinstance(best, dict)
        assert "dna" in best
        assert "fitness" in best

    def test_population_one(self):
        best = self.g.run_evolution(
            fitness_func=self.fitness_wrapper,
            length=len(self.target_dna),
            population_size=1,
            iterations=5,
            verbose=False
        )
        assert isinstance(best, dict)
        assert "dna" in best
        assert "fitness" in best

    def test_zero_iterations(self):
        best = self.g.run_evolution(
            fitness_func=self.fitness_wrapper,
            length=len(self.target_dna),
            population_size=5,
            iterations=0,
            verbose=False
        )
        assert isinstance(best, dict)
        assert "dna" in best
        assert "fitness" in best

    # ------------------- Fitness function edge cases -------------------
    def test_empty_target_dna(self):
        score = self.fitness_wrapper(self.target_dna, target_dna="")
        assert 0.0 <= score <= 1.0

    def test_critical_residues_out_of_bounds(self):
        score = self.fitness_wrapper(
            self.target_dna,
            critical_sites=[100, 101]
        )
        assert 0.0 <= score <= 1.0

    def test_impossible_environment(self):
        score = self.fitness_wrapper(
            self.target_dna,
            environment={"require_stop": True, "must_have_motif": "XXXX"}
        )
        assert 0.0 <= score <= 1.0