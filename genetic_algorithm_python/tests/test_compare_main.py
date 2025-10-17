import pytest
from lib.compare_main import run_ga_vs_weasel_comparison, TARGET_DNA, GENERATIONS, POP_SIZE, MU, OFFSPRING

class TestCompareMain:
    """Test suite for compare_main GA vs Weasel comparison."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup parameters for tests."""
        self.target_dna = TARGET_DNA
        self.generations = 5  # keep small for fast tests
        self.pop_size = 5
        self.mu = MU
        self.offspring = OFFSPRING

    # ------------------- Basic execution -------------------
    def test_ga_vs_weasel_runs(self):
        """Ensure the comparison function runs without errors."""
        results = run_ga_vs_weasel_comparison()
        assert results is not None

    # ------------------- Output structure -------------------
    def test_output_structure(self):
        """Ensure returned results contain GA and Weasel histories."""
        results = run_ga_vs_weasel_comparison()
        assert "ga_history" in results
        assert "weasel_history" in results
        assert isinstance(results["ga_history"], list)
        assert isinstance(results["weasel_history"], list)

    # ------------------- History entries -------------------
    def test_history_entries_keys(self):
        """Ensure each history entry contains expected keys."""
        results = run_ga_vs_weasel_comparison()
        for entry in results["ga_history"]:
            assert all(k in entry for k in ["generation", "gen_best", "running_best", "avg", "best_string"])
        for entry in results["weasel_history"]:
            assert all(k in entry for k in ["generation", "gen_best", "running_best", "avg", "best_string"])

    # ------------------- Fitness values -------------------
    def test_fitness_values(self):
        """Ensure fitness values are floats between 0 and 1."""
        results = run_ga_vs_weasel_comparison()
        for entry in results["ga_history"]:
            assert 0.0 <= entry["gen_best"] <= 1.0
            assert 0.0 <= entry["running_best"] <= 1.0
            assert 0.0 <= entry["avg"] <= 1.0
        for entry in results["weasel_history"]:
            assert 0.0 <= entry["gen_best"] <= 1.0
            assert 0.0 <= entry["running_best"] <= 1.0
            assert 0.0 <= entry["avg"] <= 1.0

    # ------------------- Best string is non-empty -------------------
    def test_best_string_not_empty(self):
        """Ensure the best string is non-empty for GA and Weasel."""
        results = run_ga_vs_weasel_comparison()
        assert results["ga_history"][-1]["best_string"] != ""
        assert results["weasel_history"][-1]["best_string"] != ""


    def test_running_best_monotonic(self):
        """Ensure running_best never decreases across generations."""
        results = run_ga_vs_weasel_comparison()
        for history in [results["ga_history"], results["weasel_history"]]:
            last_best = 0
            for entry in history:
                assert entry["running_best"] >= last_best
                last_best = entry["running_best"]
    
    def test_histories_not_empty(self):
        """Ensure GA and Weasel histories contain entries after run."""
        results = run_ga_vs_weasel_comparison()
        assert len(results["ga_history"]) > 0
        assert len(results["weasel_history"]) > 0
   
    def test_ga_final_fitness_not_empty(self):
            """Ensure GA final fitness is non-zero."""
            results = run_ga_vs_weasel_comparison()  # Must return a dict!
            final_ga = results["ga_history"][-1]
            final_fitness = final_ga.get("running_best") or final_ga.get("gen_best")

            assert final_fitness is not None, "GA final fitness should not be None"
            assert final_fitness > 0, f"GA final fitness should be positive, got {final_fitness}"

    def test_weasel_final_fitness_not_empty(self):
        """Ensure Weasel final fitness is non-zero."""
        results = run_ga_vs_weasel_comparison()
        final_weasel = results["weasel_history"][-1]
        final_fitness = final_weasel.get("running_best") or final_weasel.get("gen_best")

        assert final_fitness is not None, "Weasel final fitness should not be None"
        assert final_fitness > 0, f"Weasel final fitness should be positive, got {final_fitness}"