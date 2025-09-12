import pytest
from lib.genome_fitness import phenotype_fitness, dna_fitness
from lib.bio_genome import Genome

class TestFitnessFunctions:
    """Test suite for genome_fitness functions."""

    @pytest.fixture(autouse=True)
    def setup_genome(self):
        self.g = Genome()
        self.target_dna = "ATGTTTAAAGGG"
        self.target_protein = self.g.protein(self.g.dna_to_rna(self.target_dna))

    # ------------------- phenotype_fitness -------------------
    def test_phenotype_fitness_returns_float(self):
        score = phenotype_fitness(self.target_dna, self.target_protein, self.g)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_phenotype_fitness_perfect_match(self):
        score = phenotype_fitness(self.target_dna, self.target_protein, self.g)
        assert score == 1.0

    def test_phenotype_fitness_mismatch(self):
        mutated_dna = self.g.mutate(self.target_dna, p_m=1.0)
        score = phenotype_fitness(mutated_dna, self.target_protein, self.g)
        assert 0.0 <= score < 1.0

    # ------------------- dna_fitness -------------------
    def test_dna_fitness_returns_float(self):
        score = dna_fitness(self.target_dna, self.target_dna, self.g)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_dna_fitness_perfect_match(self):
        score = dna_fitness(self.target_dna, self.target_dna, self.g)
        assert score >= 0.5  # should be high for perfect DNA+protein match

    def test_dna_fitness_penalties_applied(self):
        bad_dna = "TTGAAA"  # no start codon, short length
        score = dna_fitness(bad_dna, self.target_dna, self.g)
        assert score < 0.5  # penalties should reduce fitness

    def test_phenotype_fitness_perfect_match(self):
        score = phenotype_fitness(self.target_dna, self.target_protein, self.g)
        assert score == 1.0

    def test_phenotype_fitness_mismatch(self):
        mutated = self.g.mutate(self.target_dna, p_m=1.0)
        score = phenotype_fitness(mutated, self.target_protein, self.g)
        assert 0.0 <= score < 1.0

    # ------------------- dna_fitness -------------------
    def test_dna_fitness_perfect_match(self):
        score = dna_fitness(self.target_dna, self.target_dna, self.g)
        assert score >= 0.5

    def test_dna_fitness_penalties_applied(self):
        bad_dna = "TTGAAA"
        score = dna_fitness(bad_dna, self.target_dna, self.g)
        assert score < 0.5

    # ------------------- TDD placeholders for new features -------------------
    def test_critical_residues_weighted(self):
        # TDD: weight critical amino acids
        critical_sites = [0, 2]
        mutant = "ATGTTTAAAGGA"
        mutant2 = "TTGTTTAAAGGG"
        score1 = dna_fitness(mutant, self.target_dna, self.g, critical_sites=critical_sites)
        score2 = dna_fitness(mutant2, self.target_dna, self.g, critical_sites=critical_sites)
        assert score1 > score2

    def test_dynamic_fitness_environment(self):
        # TDD: environment-aware fitness
        env1 = {"require_stop": True}
        env2 = {"require_stop": False}
        score1 = dna_fitness(self.target_dna, self.target_dna, self.g, environment=env1)
        score2 = dna_fitness(self.target_dna, self.target_dna, self.g, environment=env2)
        assert score1 != score2