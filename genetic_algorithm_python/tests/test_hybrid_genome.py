import pytest
from lib.hybrid_genome import HybridGenome

class TestHybridGenome:
    """Integration and unit tests for HybridGenome GA."""

    @pytest.fixture(autouse=True)
    def setup_hybrid(self):
        self.g = HybridGenome()
        self.target_dna = "ATGCATGC"
        self.fitness = lambda seq: sum(a==b for a,b in zip(seq, self.target_dna)) / len(self.target_dna)

    def test_initial_population_packing(self):
        """Check that population is packed to bytes and can be unpacked correctly."""
        packed = self.g.pack(self.target_dna)
        unpacked = self.g.unpack(packed)
        assert unpacked == self.target_dna, "Packed -> unpacked DNA must match original"

    def test_mutation_changes_sequence(self):
        """Mutation should modify DNA, but length should remain constant."""
        packed = self.g.pack(self.target_dna)
        mutated = self.g.mutate(packed, p_m=1.0)  # force mutation
        unpacked = self.g.unpack(mutated)
        assert unpacked != self.target_dna
        assert len(unpacked) == len(self.target_dna)
        assert all(b in "ATGC" for b in unpacked)

    def test_crossover_produces_two_children(self):
        """Crossover should return two valid DNA sequences of same length."""
        parent1 = self.g.pack(self.target_dna)
        parent2 = self.g.pack(self.target_dna[::-1])
        children = self.g.crossover([parent1, parent2], p_c=1.0)  # force crossover
        assert len(children) == 2
        for c in children:
            seq = self.g.unpack(c)
            assert len(seq) == len(self.target_dna)
            assert all(b in "ATGC" for b in seq)

    def test_run_evolution_returns_correct_format(self):
        """GA should return dict with dna, fitness, and history."""
        result = self.g.run_evolution(
            fitness_func=self.fitness,
            length=len(self.target_dna),
            iterations=10,
            population_size=5,
            verbose=False,
            normalized=False
        )
        assert isinstance(result, dict)
        assert "dna" in result and "fitness" in result and "history" in result
        assert all(b in "ATGC" for b in result["dna"])
        assert isinstance(result["history"], list)
        for entry in result["history"]:
            assert "generation" in entry
            assert "gen_best" in entry
            assert "running_best" in entry
            assert "avg" in entry

    def test_best_solution_reaches_acceptable_match(self):
        """GA should be able to reach perfect match if mutation and iterations are sufficient."""
        result = self.g.run_evolution(
            fitness_func=self.fitness,
            length=len(self.target_dna),
            iterations=100,
            population_size=10,
            p_m=0.5,  # higher mutation for faster exploration
            verbose=False,
            normalized=True
        )
        assert self.fitness(result["dna"]) >= 0.85, f"GA returned low fitness: {self.fitness(result['dna'])}"

    def test_history_generations_increasing(self):
        """History should contain sequential generation numbers."""
        result = self.g.run_evolution(
            fitness_func=self.fitness,
            length=len(self.target_dna),
            iterations=15,
            population_size=5,
            verbose=False
        )
        generations = [h["generation"] for h in result["history"]]
        assert generations == list(range(len(generations)))
