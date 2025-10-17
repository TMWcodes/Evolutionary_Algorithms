import pytest
from lib.fitness_wrappers import dna_only_wrapper, dna_fitness_wrapper, automation_fitness_wrapper
from lib.bio_genome import Genome
from lib.automation_fitness import AutomationFitness

class TestFitnessWrappers:
    """Tests for GA fitness wrapper functions."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.genome = Genome()
        self.target_dna = "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
        self.auto_fitness = AutomationFitness({})  # minimal map for automation wrapper

    def test_dna_only_wrapper_perfect_match(self):
        wrapper = dna_only_wrapper(self.target_dna, self.genome)
        score = wrapper(self.target_dna)
        assert isinstance(score, float)
        assert score == 1.0

    def test_dna_only_wrapper_case_insensitive(self):
        wrapper = dna_only_wrapper(self.target_dna, self.genome)
        score = wrapper(self.target_dna.lower())
        assert score == 1.0  # lowercased input should match

    def test_dna_fitness_wrapper_returns_float(self):
        wrapper = dna_fitness_wrapper(self.target_dna, self.genome)
        candidate = self.target_dna
        score = wrapper(candidate)
        assert isinstance(score, float)
        assert 0 <= score <= 1

    def test_automation_fitness_wrapper_returns_float(self):
        wrapper = automation_fitness_wrapper(self.genome, self.auto_fitness)
        candidate = self.target_dna
        score = wrapper(candidate)
        assert isinstance(score, float)
        assert 0 <= score <= 1
class TestDNAWrapperIntegration:
    """Integration tests for dna_only_wrapper with GA evolution."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.genome = Genome()
        self.target_dna = "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
        self.target_dna = self.target_dna.upper()
        self.pop_size = 10
        self.generations = 20

    def test_wrapper_scores_correctly(self):
        """dna_only_wrapper produces scores between 0 and 1."""
        wrapper = dna_only_wrapper(self.target_dna, self.genome, enforce_start_stop=False)
        score = wrapper(self.target_dna)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_ga_evolution_improves_fitness(self):
        """GA using dna_only_wrapper improves running_best fitness over generations."""
        wrapper = dna_only_wrapper(self.target_dna, self.genome, enforce_start_stop=False)
        result = self.genome.run_evolution(
            fitness_func=wrapper,
            length=len(self.target_dna),
            population_size=self.pop_size,
            iterations=self.generations,
            verbose=False
        )

        history = result.get("history", [])
        assert len(history) == self.generations, "GA did not return full history"

        running_best_prev = 0.0
        for gen_entry in history:
            running_best = gen_entry.get("running_best", 0.0)
            assert running_best >= running_best_prev, "Running best decreased"
            running_best_prev = running_best

        # The final DNA sequence should be valid
        final_dna = result.get("dna", "")
        assert final_dna != "", "GA produced empty DNA"
        assert set(final_dna).issubset({"A","T","G","C"}), "GA produced invalid DNA bases"