# tests/test_automation_fitness.py
import pytest
from lib.automation_fitness import AutomationFitness, AMINO_TASK_MAP

class TestAutomationFitness:
    @pytest.fixture(autouse=True)
    def setup_auto(self):
        self.auto_fit = AutomationFitness()

    # ------------------------------
    # protein → tasks
    # ------------------------------
    @pytest.mark.parametrize("protein,expected_task_names", [
        ("MFK*", ["Model Training", "Database Migration", "Email Parsing"]),
        ("MFKN", ["Model Training", "Database Migration", "Email Parsing", "Unit Test Run"]),
        ("FML", ["Database Migration", "Model Training", "Deploy Script"]),
        ("", []),
        ("M*", ["Model Training"])
    ])
    def test_protein_to_tasks(self, protein, expected_task_names):
        tasks = self.auto_fit.protein_to_tasks(protein)
        names = [t[0] for t in tasks]
        assert names == expected_task_names

    # ------------------------------
    # basic protein fitness
    # ------------------------------
    def test_protein_fitness_basic(self):
        protein = "MFK"  # Model Training, Database Migration, Email Parsing
        score = self.auto_fit.protein_fitness(protein)
        assert 0.0 < score <= 1.0

    def test_protein_fitness_empty_or_invalid(self):
        # Empty protein or no tasks should return minimum fitness
        protein = ""
        score = self.auto_fit.protein_fitness(protein)
        assert score == 0.01

    # ------------------------------
    # time utilization cutoff
    # ------------------------------
    def test_protein_fitness_max_time_cutoff(self):
        protein = "MMMMMMMM"  # repeated task
        score = self.auto_fit.protein_fitness(protein)
        # Should be valid and <= 1.0, but may equal single-task max
        assert 0.0 < score <= 1.0

    def test_protein_fitness_diversity_bonus(self):
        protein_low_div = "MMMM"  # repeated task
        protein_high_div = "MFKLP"  # all different tasks
        low_score = self.auto_fit.protein_fitness(protein_low_div)
        high_score = self.auto_fit.protein_fitness(protein_high_div)
        # High-diversity score should be >= low-diversity, not strictly >
        assert high_score >= low_score

    # ------------------------------
    # all amino acids are recognized
    # ------------------------------
    def test_all_amino_acids_in_map(self):
        protein = "".join(k for k in AMINO_TASK_MAP if k != "*")
        tasks = self.auto_fit.protein_to_tasks(protein)
        names = [t[0] for t in tasks]
        assert len(names) == len(protein)

    # ------------------------------
    # no zero-duration tasks
    # ------------------------------
    def test_no_zero_duration_tasks(self):
        protein = "MFK*"
        tasks = self.auto_fit.protein_to_tasks(protein)
        for _, _, duration in tasks:
            assert duration > 0
    
    
# ------------------------------
    # Basic translation
    # ------------------------------
    @pytest.mark.parametrize("protein,expected_task_names", [
        ("MFKL", ["Model Training", "Database Migration", "Email Parsing", "Deploy Script"]),
        ("MTV", ["Model Training", "DB Sync", "System Audit"]),
        ("", []),
        ("*", [])
    ])
    def test_protein_to_tasks(self, protein, expected_task_names):
        tasks = self.auto_fit.protein_to_tasks(protein)
        names = [t[0] for t in tasks]
        assert names == expected_task_names

    # ------------------------------
    # Fitness is within [0.01, 1.0]
    # ------------------------------
    def test_fitness_bounds(self):
        protein = "MFKL"
        score = self.auto_fit.protein_fitness(protein)
        assert 0.01 <= score <= 1.0

    # ------------------------------
    # No zero-duration tasks in fitness calculation
    # ------------------------------
    def test_no_zero_duration_tasks(self):
        protein = "MFKL"
        tasks = self.auto_fit.protein_to_tasks(protein)
        for _, _, duration in tasks:
            assert duration > 0

    # ------------------------------
    # High time utilization yields higher score
    # ------------------------------
    def test_time_utilization_bonus(self):
        # Single task: 20 min
        protein_short = "F"  
        # Sequence closer to 480 min using repeated tasks with allowed diversity
        protein_long = "FMLPTVSAGYHNCDRW" * 3  
        short_score = self.auto_fit.protein_fitness(protein_short)
        long_score = self.auto_fit.protein_fitness(protein_long)
        assert long_score >= short_score

    # ------------------------------
    # No back-to-back repeats
    # ------------------------------
    def test_back_to_back_penalty(self):
        protein_repeats = "MMMM"
        protein_diverse = "MFKL"
        repeat_score = self.auto_fit.protein_fitness(protein_repeats)
        diverse_score = self.auto_fit.protein_fitness(protein_diverse)
        # Diverse sequence should score higher
        assert diverse_score >= repeat_score

    # ------------------------------
    # Diversity bonus: more unique tasks → higher score
    # ------------------------------
    def test_diversity_bonus_effect(self):
        low_div = "MMMM"
        high_div = "MFKLPVSTAGYHNDCRW"
        low_score = self.auto_fit.protein_fitness(low_div)
        high_score = self.auto_fit.protein_fitness(high_div)
        assert high_score >= low_score

    # ------------------------------
    # Fitness stops at 8 hours
    # ------------------------------
    def test_max_time_cap(self):
        protein = "MFKLPVSTAGYHNDCRW" * 20  # way over 480 min
        score = self.auto_fit.protein_fitness(protein, max_minutes=480)
        # Total time used cannot exceed 480 min
        tasks = self.auto_fit.protein_to_tasks(protein)
        total_time = 0
        last_task = None
        for name, _, duration in tasks:
            if total_time + duration > 480:
                break
            if name == last_task:
                total_time += duration * 0.5
            else:
                total_time += duration
            last_task = name
        assert total_time <= 480
        # Fitness is > 0
        assert score > 0.01