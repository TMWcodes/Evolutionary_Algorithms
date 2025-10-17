import pytest
import random
from lib.bio_genome import Genome
from lib.fitness_wrappers import dna_only_wrapper
from lib.compare_results import compare_ga_vs_weasel

class TestCompareResults:
    """Test suite for compare_results.py functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Automatically run before each test."""
        random.seed(42)  # deterministic behavior
        self.target_dna = (
            "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
        )
        self.generations = 5
        self.pop_size = 3
        self.mu = 0.05
        self.offspring = 3

    # ------------------- GA vs Weasel tests -------------------
    def test_compare_ga_vs_weasel_output_structure(self):
        """Check that compare_ga_vs_weasel returns expected dict structure."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=5,
            pop_size=5,
            mu=0.05,
            offspring=5
        )

        # Check top-level keys
        assert "ga_history" in results
        assert "weasel_history" in results

        # Check that histories are lists
        assert isinstance(results["ga_history"], list)
        assert isinstance(results["weasel_history"], list)

    def test_ga_history_entries(self):
        """Verify GA history entries have required keys and types."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=3,
            pop_size=3,
            mu=0.05,
            offspring=3
        )

        for entry in results["ga_history"]:
            assert all(k in entry for k in ["generation", "gen_best", "running_best", "avg", "best_string"])
            assert isinstance(entry["generation"], int)
            assert isinstance(entry["gen_best"], float)
            assert isinstance(entry["running_best"], float)
            assert isinstance(entry["avg"], float)
            assert isinstance(entry["best_string"], str)

    def test_weasel_history_entries(self):
        """Verify Weasel history entries have required keys and types."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=3,
            pop_size=3,
            mu=0.05,
            offspring=3
        )

        for entry in results["weasel_history"]:
            assert all(k in entry for k in ["generation", "gen_best", "running_best", "avg", "best_string"])
            assert isinstance(entry["generation"], int)
            assert isinstance(entry["gen_best"], float)
            assert isinstance(entry["running_best"], float)
            assert isinstance(entry["avg"], float)
            assert isinstance(entry["best_string"], str)

    def test_ga_and_weasel_history_not_empty(self):
        """Ensure GA and Weasel histories contain entries after run."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=self.generations,
            pop_size=self.pop_size,
            mu=self.mu,
            offspring=self.offspring
        )
        assert len(results["ga_history"]) > 0
        assert len(results["weasel_history"]) > 0

    def test_ga_best_fitness_increases(self):
        """Check that running_best never decreases in GA history."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=5,
            pop_size=5,
            mu=0.05,
            offspring=5
        )
        running_bests = [entry["running_best"] for entry in results["ga_history"]]
        assert running_bests == sorted(running_bests)  # non-decreasing

    def test_weasel_best_fitness_increases(self):
        """Check that running_best never decreases in Weasel history."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=5,
            pop_size=5,
            mu=0.05,
            offspring=5
        )
        running_bests = [entry["running_best"] for entry in results["weasel_history"]]
        assert running_bests == sorted(running_bests)  # non-decreasing
    def test_best_fitness_increases(self):
        """Ensure running_best never decreases across generations."""
        results = compare_ga_vs_weasel(
            target_dna=self.target_dna,
            generations=self.generations,
            pop_size=self.pop_size,
            mu=self.mu,
            offspring=self.offspring
        )
        # GA running_best
        ga_best_prev = 0.0
        for entry in results["ga_history"]:
            assert entry["running_best"] >= ga_best_prev
            ga_best_prev = entry["running_best"]

        # Weasel running_best
        weasel_best_prev = 0.0
        for entry in results["weasel_history"]:
            assert entry["running_best"] >= weasel_best_prev
            weasel_best_prev = entry["running_best"]

class TestCompareResultsDiagnostic:
    """Diagnostic tests to inspect actual GA and Weasel history structures."""

    def test_inspect_ga_weasel_history(self):
        TARGET_DNA = "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
        results = compare_ga_vs_weasel(
            target_dna=TARGET_DNA,
            generations=5,
            pop_size=5,
            mu=0.05,
            offspring=5
        )

        print("\n=== GA History ===")
        for i, entry in enumerate(results["ga_history"], start=1):
            print(f"Gen {i}: type={type(entry)}, content={entry}")

        print("\n=== Weasel History ===")
        for i, entry in enumerate(results["weasel_history"], start=1):
            print(f"Gen {i}: type={type(entry)}, content={entry}")