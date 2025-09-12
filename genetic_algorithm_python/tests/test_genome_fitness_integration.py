# tests/test_genome_fitness_integration.py
import pytest
from lib.bio_genome import Genome
from lib.genome_fitness import dna_fitness

class TestGenomeIntegration:
    """Integration tests for the full GA pipeline."""

    @pytest.fixture(autouse=True)
    def setup_genome(self):
        self.g = Genome()
        self.target_dna = "ATGTTTAAAGGG"
        self.critical_sites = [0, 2]
        self.environment = {"require_stop": True}

    def test_small_evolution_run(self):
        """Check GA runs and returns valid output."""
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

    def test_evolution_improves_fitness(self):
        """Check that GA actually improves fitness over generations."""
        def dummy_fitness(dna):
            return sum(1 for b in dna if b == "A") / len(dna)

        best = self.g.run_evolution(
            fitness_func=dummy_fitness,
            length=12,
            population_size=10,
            iterations=20,
            p_m=0.2,
            p_c=0.7,
            verbose=False
        )
        assert best['fitness'] >= 0.5

    def test_evolution_with_critical_sites(self):
        """Check GA respects critical residue weighting."""
        def critical_fitness(dna):
            _, _, combined = dna_fitness(
                dna,
                self.target_dna,
                self.g,
                critical_sites=self.critical_sites
            )
            return combined  # GA expects a float

        best = self.g.run_evolution(
            fitness_func=critical_fitness,
            length=len(self.target_dna),
            population_size=8,
            iterations=10,
            p_m=0.3,
            p_c=0.7,
            verbose=False
        )
        assert best['fitness'] > 0.3

    def test_evolution_environment_aware(self):
        """Check GA adapts to environment constraints (e.g., stop codon)."""
        def env_fitness(dna):
            _, _, combined = dna_fitness(
                dna,
                self.target_dna,
                self.g,
                environment=self.environment
            )
            return combined  # return float for GA

        best = self.g.run_evolution(
            fitness_func=env_fitness,
            length=len(self.target_dna),
            population_size=8,
            iterations=10,
            p_m=0.3,
            p_c=0.7,
            verbose=False
        )
        assert best['dna'][-3:] in {"TAA", "TAG", "TGA"}
