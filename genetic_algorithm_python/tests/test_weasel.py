import pytest
import random
from lib.weasel import weasel_run
from lib.bio_genome import Genome
from lib.fitness_wrappers import dna_only_wrapper

class TestWeaselRun:
    """Test suite for Weasel-style evolution."""

    @pytest.fixture(autouse=True)
    def setup(self):
        random.seed(42)  # deterministic behavior
        self.target_dna = "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
        self.L = len(self.target_dna)
        self.genome = Genome()
        self.mu = 0.05
        self.offspring = 20
        self.max_gens = 50

    def test_history_structure(self):
        """Each history entry should have the expected keys and types."""
        history = weasel_run(
            target_dna=self.target_dna,
            genome=self.genome,
            L=self.L,
            mu=self.mu,
            offspring=self.offspring,
            max_gens=self.max_gens
        )
        assert isinstance(history, list)
        for entry in history:
            assert isinstance(entry, dict)
            for key in ["generation", "gen_best", "running_best", "avg", "best_string"]:
                assert key in entry
            assert isinstance(entry["generation"], int)
            assert isinstance(entry["gen_best"], float)
            assert isinstance(entry["running_best"], float)
            assert isinstance(entry["avg"], float)
            assert isinstance(entry["best_string"], str)

    def test_running_best_never_decreases(self):
        """Running best fitness should be non-decreasing."""
        history = weasel_run(
            target_dna=self.target_dna,
            genome=self.genome,
            L=self.L,
            mu=self.mu,
            offspring=self.offspring,
            max_gens=self.max_gens
        )
        running_best = 0.0
        for entry in history:
            assert entry["running_best"] >= running_best
            running_best = entry["running_best"]

    def test_best_string_length(self):
        """Best string should always match the target length."""
        history = weasel_run(
            target_dna=self.target_dna,
            genome=self.genome,
            L=self.L,
            mu=self.mu,
            offspring=self.offspring,
            max_gens=self.max_gens
        )
        for entry in history:
            assert len(entry["best_string"]) == self.L

    def test_improved_fitness(self):
        """Check that gen_best or running_best is greater than zero if mutation rate > 0."""
        history = weasel_run(
            target_dna=self.target_dna,
            genome=self.genome,
            L=self.L,
            mu=self.mu,
            offspring=self.offspring,
            max_gens=self.max_gens
        )
        assert any(entry["gen_best"] > 0 for entry in history)
        assert history[-1]["running_best"] >= 0
