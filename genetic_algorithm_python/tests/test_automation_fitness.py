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
        ("FML", []),   # doesn't start with M
        ("", []),
        ("M*", ["Model Training"])
    ])
    def test_protein_to_tasks(self, protein, expected_task_names):
        tasks = self.auto_fit.protein_to_tasks(protein)
        names = [t[0] for t in tasks]
        assert names == expected_task_names

    # ------------------------------
    # protein fitness
    # ------------------------------
    def test_protein_fitness_basic(self):
        protein = "MFK"  # Model Training, Email Parsing, Data Cleanup
        score = self.auto_fit.protein_fitness(protein)
        assert 0.0 < score <= 1.0

    def test_protein_fitness_empty(self):
        # Empty or no tasks returns minimum fitness
        protein = "FLL"
        score = self.auto_fit.protein_fitness(protein)
        assert score == 0.01

    def test_protein_fitness_max_hours_penalty(self):
        # Total task time exceeds max_hours → fitness halved
        protein = "MMMM"  # 4 x Model Training, 5*4 = 20 hours > 8
        score = self.auto_fit.protein_fitness(protein, max_hours=8.0)
        assert score < self.auto_fit.protein_fitness("M", max_hours=8.0)

    # ------------------------------
    # Ensure all amino acids are recognized
    # ------------------------------
    def test_all_amino_acids_in_map(self):
        protein = "".join(k for k in AMINO_TASK_MAP if k != "*")
        tasks = self.auto_fit.protein_to_tasks(protein)  # no extra M prepended
        names = [t[0] for t in tasks]
        assert len(names) == len(protein)