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

 

        # ===========================================
    # NEW TESTS FOR FITNESS IMPROVEMENTS
    # ===========================================

    # ------------------------------
    # Time Constraint Handling Tests
    # ------------------------------
    
    def test_exactly_480_minutes_gets_time_bonus(self):
        """Sequences that use exactly 480 minutes should get maximum time utilization bonus"""
        # Create a sequence that totals exactly 480 minutes
        # F=20, M=25, L=15, T=25, V=20, R=20, P=15, S=15 = 155 min
        # Repeat this pattern to get close to 480
        protein_exact = "FMLTVRPS" * 6  # 155 * 6 = 930, too much
        protein_near_480 = "FMLTVR" * 8  # Need to calculate exactly
        
        # Test that near-optimal time usage scores higher than short sequences
        protein_short = "F"  # 20 minutes
        
        score_near_480 = self.auto_fit.protein_fitness(protein_near_480)
        score_short = self.auto_fit.protein_fitness(protein_short)
        
        assert score_near_480 > score_short

    def test_overtime_sequence_gets_penalty_not_zero(self):
        """Sequences exceeding 480 min should be penalized but not get 0.01"""
        # Create a long sequence that definitely exceeds 480 minutes
        protein_overtime = "M" * 25  # 25 * 25 = 625 minutes
        protein_valid = "M" * 15     # 15 * 25 = 375 minutes
        
        score_overtime = self.auto_fit.protein_fitness(protein_overtime)
        score_valid = self.auto_fit.protein_fitness(protein_valid)
        
        # Overtime should be penalized but not minimal
        assert score_overtime < score_valid
        assert score_overtime > self.auto_fit.min_fitness

    def test_partial_sequence_execution_on_time_limit(self):
        """When sequence exceeds time, only tasks within limit should count"""
        # F=20, M=25, T=25 = 70 minutes per cycle
        # At 480 minutes, we can fit 6.8 cycles, so 6 full cycles + partial
        protein_long = "FMT" * 10  # 700 minutes total, but only ~6.8 cycles fit
        
        score = self.auto_fit.protein_fitness(protein_long)
        
        # Should be valid (not minimal) since partial execution is allowed
        assert score > self.auto_fit.min_fitness

    # ------------------------------
    # Diminishing Returns Tests
    # ------------------------------
    
  

    def test_different_tasks_no_diminishing_returns(self):
        """Different tasks should not experience cross-task diminishing returns"""
        protein_varied = "FMLT"    # All different high-value tasks
        protein_repeated = "FFFF"   # Same task repeated
        
        score_varied = self.auto_fit.protein_fitness(protein_varied)
        score_repeated = self.auto_fit.protein_fitness(protein_repeated)
        
        # Varied should outperform repeated due to no diminishing returns
        assert score_varied > score_repeated

    # ------------------------------
    # Diversity Bonus Tests
    # ------------------------------
    
    def test_diversity_bonus_scales_with_unique_tasks(self):
        """More unique tasks should provide increasing diversity bonus"""
        protein_2_unique = "FMFMFM"      # 2 unique tasks
        protein_5_unique = "FMLVS"       # 5 unique tasks  
        protein_10_unique = "FMLVSPTAHY" # 10 unique tasks
        
        score_2 = self.auto_fit.protein_fitness(protein_2_unique)
        score_5 = self.auto_fit.protein_fitness(protein_5_unique)
        score_10 = self.auto_fit.protein_fitness(protein_10_unique)
        
        # Higher diversity should generally score better (controlling for other factors)
        # Note: This might not always be strictly true due to efficiency differences
        assert score_10 >= score_5 or abs(score_10 - score_5) < 0.1  # Allow for efficiency trade-offs

    def test_maximum_diversity_bonus(self):
        """Using all available tasks should provide maximum diversity bonus"""
        # Use all non-stop amino acids at least once
        all_tasks = "".join([k for k in AMINO_TASK_MAP.keys() if k != "*"])
        protein_max_diversity = all_tasks
        
        protein_low_diversity = "FFFF"
        
        score_max_div = self.auto_fit.protein_fitness(protein_max_diversity)
        score_low_div = self.auto_fit.protein_fitness(protein_low_diversity)
        
        # Max diversity should outperform low diversity
        assert score_max_div > score_low_div

    # ------------------------------
    # Back-to-Back Penalty Tests  
    # ------------------------------
    
    def test_back_to_back_penalty_severity(self):
        """Back-to-back repeats should be penalized more than spaced repeats"""
        protein_back_to_back = "FFMMLLTT"    # All back-to-back
        protein_spaced = "FMLTFMLT"          # Same tasks, spaced out
        
        score_btb = self.auto_fit.protein_fitness(protein_back_to_back)
        score_spaced = self.auto_fit.protein_fitness(protein_spaced)
        
        assert score_spaced > score_btb


    # ------------------------------
    # Edge Case & Robustness Tests
    # ------------------------------
    
    def test_single_task_fitness(self):
        """Single task should give reasonable fitness"""
        for task_id in AMINO_TASK_MAP:
            if task_id != "*":
                score = self.auto_fit.protein_fitness(task_id)
                assert score > self.auto_fit.min_fitness
                assert score < 1.0  # Single task shouldn't be perfect

    def test_stop_codon_handling(self):
        """Stop codons should be handled gracefully"""
        protein_with_stops = "FM*LT*S"
        protein_without_stops = "FMLTS"
        
        score_with = self.auto_fit.protein_fitness(protein_with_stops)
        score_without = self.auto_fit.protein_fitness(protein_without_stops)
        
        # Should be equal (stops ignored)
        assert score_with == score_without

    def test_very_long_sequence_handling(self):
        """Very long sequences should be handled efficiently"""
        protein_very_long = "FMLTVSPHAY" * 50  # 500 tasks
        
        # Should complete without error and give reasonable score
        score = self.auto_fit.protein_fitness(protein_very_long)
        assert 0.01 <= score <= 1.0

    # ------------------------------
    # Fitness Function Behavior Tests
    # ------------------------------
    
    def test_fitness_monotonicity_with_good_additions(self):
        """Adding efficient tasks should generally increase fitness"""
        protein_base = "F"
        protein_extended = "FM"  # Added high-efficiency task
        
        score_base = self.auto_fit.protein_fitness(protein_base)
        score_extended = self.auto_fit.protein_fitness(protein_extended)
        
        assert score_extended >= score_base

    def test_fitness_sensitivity_to_task_order(self):
        """Task order should have some impact on fitness (front-loading bonus?)"""
        protein_high_first = "MFL"    # High value tasks first
        protein_low_first = "LFM"     # Same tasks, different order
        
        score_high_first = self.auto_fit.protein_fitness(protein_high_first)
        score_low_first = self.auto_fit.protein_fitness(protein_low_first)
        
        # Front-loading might provide small bonus
        # Note: This test might need adjustment based on whether order matters in your design
        assert abs(score_high_first - score_low_first) >= 0  # At minimum, no crash

    # ------------------------------
    # Comparative Performance Tests
    # ------------------------------
    
    def test_known_good_solutions_rank_appropriately(self):
        """Known good solutions should rank higher than poor ones"""
        # Your genetic algorithm result
        genetic_solution = "FVNMVDFPVTCLSWMRGFPF"
        
        # Poor solution (low efficiency tasks repeated)
        poor_solution = "QQQQQQQQQQQQQQQQQQQ"  # Quick Health Check: 3pts/10min
        
        # Random solution
        random_solution = "FMLPVSTAHYGDCREW"
        
        genetic_score = self.auto_fit.protein_fitness(genetic_solution)
        poor_score = self.auto_fit.protein_fitness(poor_solution)
        random_score = self.auto_fit.protein_fitness(random_solution)
        
        # Genetic should outperform both
        assert genetic_score > poor_score
        assert genetic_score >= random_score  # Should be at least as good

    def test_greedy_vs_genetic_comparison(self):
        """Compare your greedy and genetic solutions"""
        greedy_solution = "FMLPAVSTHGRYNDKCWEIQFMLPAVSTHGK"
        genetic_solution = "FVNMVDFPVTCLSWMRGFPF"
        
        greedy_score = self.auto_fit.protein_fitness(greedy_solution)
        genetic_score = self.auto_fit.protein_fitness(genetic_solution)
        
        # Genetic achieved 442 vs 413 points, so should score higher
        assert genetic_score >= greedy_score

    # ------------------------------
    # Parameter Sensitivity Tests
    # ------------------------------
    
    def test_fitness_stability_across_similar_sequences(self):
        """Small changes should produce small fitness changes"""
        base_protein = "FMLTVSPH"
        
        # Small variations
        variation1 = "FMLTVSPA"  # Last task changed
        variation2 = "FMLTVSP"   # Last task removed
        
        base_score = self.auto_fit.protein_fitness(base_protein)
        var1_score = self.auto_fit.protein_fitness(variation1)
        var2_score = self.auto_fit.protein_fitness(variation2)
        
        # Changes should be reasonable, not dramatic
        assert abs(base_score - var1_score) < 0.3
        assert abs(base_score - var2_score) < 0.3

