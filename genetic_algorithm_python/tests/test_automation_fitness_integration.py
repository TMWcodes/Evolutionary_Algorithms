# tests/test_auto_ga_integration.py
import pytest
from lib.automation_fitness import AutomationFitness
from lib.run_bio_ga import run_auto_ga_evolution

class TestAutomationGA:
    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        # Suppress GA print output during tests
        monkeypatch.setattr("builtins.print", lambda *a, **k: None)
        self.auto_fitness = AutomationFitness()

    def test_ga_generates_valid_schedule(self):
        """
        Test that the GA produces a schedule:
        - Total time ≤ 8 hours (480 min)
        - No back-to-back repeated tasks
        - All tasks have positive duration
        - Fitness > 0
        """
        # Run GA with minimal generations/population for speed
        result = run_auto_ga_evolution(
            amino_task_map=None,  # use default map
            generations=10,
            pop_size=5
        )

        protein_seq = result.get("protein_seq")
        tasks_list = result.get("tasks_list")
        fitness_score = result.get("fitness_score")

        # Basic checks
        assert protein_seq and isinstance(protein_seq, str)
        assert fitness_score > 0.01
        assert tasks_list and len(tasks_list) > 0

        total_time = 0
        last_task_name = None

        for task_name, points, duration in tasks_list:
            assert duration > 0
            # Check for no consecutive repeats
            if last_task_name:
                assert task_name != last_task_name
            total_time += duration
            last_task_name = task_name

        # Total schedule must be <= 8 hours
        assert total_time <= 480
