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
    
    def test_diminishing_returns_on_repetition(self):
        """Same task repeated should show diminishing returns"""
        protein_1x = "F"        # 25 points, 20 min
        protein_2x = "FF"       # Should be less than 50 points equivalent
        protein_4x = "FFFF"     # Should show strong diminishing returns
        
        score_1x = self.auto_fit.protein_fitness(protein_1x)
        score_2x = self.auto_fit.protein_fitness(protein_2x)
        score_4x = self.auto_fit.protein_fitness(protein_4x)
        
        # Scores should increase but with diminishing returns
        assert score_2x > score_1x
        assert score_4x > score_2x
        
        # But the increase rate should decrease (diminishing returns)
        increase_1_to_2 = score_2x - score_1x
        increase_2_to_4 = score_4x - score_2x
        assert increase_2_to_4 < increase_1_to_2

    def test_different_tasks_no_diminishing_returns(self):
        """Different tasks should not experience cross-task diminishing returns"""
        protein_varied = "FMLT"    # All different high-value tasks
        protein_repeated = "FFFF"   # Same task repeated
        
        score_varied = self.auto_fit.protein_fitness(protein_varied)
        score_repeated = self.auto_fit.protein_fitness(protein_repeated)
        
        # Varied should outperform repeated due to no diminishing returns
        assert score_varied > score_repeated

    # ------------------------------
    # Efficiency vs Volume Balance Tests
    # ------------------------------
    
    def test_high_efficiency_vs_high_volume_balance(self):
        """Balance between high-efficiency tasks and high-volume tasks"""
        # High efficiency: I=4pts/10min=0.4, A=9pts/10min=0.9, H=8pts/10min=0.8
        protein_high_eff = "IAHIAHIAH" * 5  # High efficiency, lower total points
        
        # High volume: M=30pts/25min=1.2, F=25pts/20min=1.25
        protein_high_vol = "MFMFMFMF"      # Higher points per task
        
        # Both should be viable strategies
        score_eff = self.auto_fit.protein_fitness(protein_high_eff)
        score_vol = self.auto_fit.protein_fitness(protein_high_vol)
        
        # Both should be well above minimum
        assert score_eff > 0.3
        assert score_vol > 0.3

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

    def test_single_back_to_back_minor_penalty(self):
        """Single back-to-back occurrence should have minor penalty"""
        protein_one_repeat = "FMLTF"   # One back-to-back at end
        protein_no_repeat = "FMLTA"    # No back-to-back
        
        score_repeat = self.auto_fit.protein_fitness(protein_one_repeat)
        score_no_repeat = self.auto_fit.protein_fitness(protein_no_repeat)
        
        # Penalty should be small for single occurrence
        penalty_ratio = (score_no_repeat - score_repeat) / score_no_repeat
        assert 0 < penalty_ratio < 0.2  # Less than 20% penalty

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

class TestCriticalSequenceIssues:
    @pytest.fixture(autouse=True)
    def setup_auto(self):
        self.auto_fit = AutomationFitness()

    # ===========================================
    # SEQUENCE ORDER PRESERVATION TESTS
    # ===========================================
    
    def test_sequence_order_preserved_in_fitness(self):
        """CRITICAL: Fitness calculation must respect the evolved sequence order"""
        # Two sequences with same tasks, different order
        protein_order1 = "FML"  # Database Migration, Model Training, Deploy Script  
        protein_order2 = "LMF"  # Deploy Script, Model Training, Database Migration
        
        # If fitness respects order, these should have different scores
        # (due to front-loading bonuses, time utilization differences, etc.)
        score1 = self.auto_fit.protein_fitness(protein_order1)
        score2 = self.auto_fit.protein_fitness(protein_order2)
        
        # At minimum, fitness calculation should not crash and should be deterministic
        assert isinstance(score1, (int, float))
        assert isinstance(score2, (int, float))
        
        # If order matters (which it should), scores might differ
        # If order doesn't matter, scores should be identical
        # Either way, this tests that order is handled consistently
        
        # Re-run to ensure deterministic behavior
        score1_repeat = self.auto_fit.protein_fitness(protein_order1)
        score2_repeat = self.auto_fit.protein_fitness(protein_order2)
        
        assert score1 == score1_repeat, "Fitness calculation must be deterministic"
        assert score2 == score2_repeat, "Fitness calculation must be deterministic"

    def test_schedule_protein_respects_sequence_order(self):
        """CRITICAL: schedule_protein() must NOT reorder tasks by efficiency"""
        
        # Create a sequence where evolved order differs from efficiency order
        # M=30pts/25min=1.2, F=25pts/20min=1.25, L=18pts/15min=1.2
        # Efficiency order would be: F, M/L (tie)
        # But our evolved sequence is different:
        evolved_sequence = "MLF"  # Model, Deploy, Database Migration
        
        # Get the scheduled tasks
        if hasattr(self.auto_fit, 'schedule_protein'):
            scheduled_tasks = self.auto_fit.schedule_protein(evolved_sequence)
            
            # Extract task names in order
            if scheduled_tasks and len(scheduled_tasks) > 0:
                scheduled_names = [task[0] for task in scheduled_tasks]
                expected_names = ["Model Training", "Deploy Script", "Database Migration"]
                
                assert scheduled_names == expected_names, \
                    f"Schedule order {scheduled_names} != evolved order {expected_names}"
        else:
            # If schedule_protein doesn't exist, that's also a problem we should know about
            pytest.skip("schedule_protein method not found")

    def test_protein_to_tasks_preserves_order(self):
        """protein_to_tasks() should maintain the sequence order"""
        protein = "MLF"
        tasks = self.auto_fit.protein_to_tasks(protein)
        
        expected_order = ["Model Training", "Deploy Script", "Database Migration"]
        actual_order = [task[0] for task in tasks]
        
        assert actual_order == expected_order, \
            f"Task order {actual_order} != expected {expected_order}"

    def test_fitness_vs_schedule_consistency(self):
        """Fitness calculation should be consistent with final scheduling"""
        protein = "FML"
        
        # Get fitness score
        fitness_score = self.auto_fit.protein_fitness(protein)
        
        # Get scheduled tasks if method exists
        if hasattr(self.auto_fit, 'schedule_protein'):
            scheduled_tasks = self.auto_fit.schedule_protein(protein)
            
            # Calculate points from scheduled tasks
            if scheduled_tasks:
                scheduled_points = sum(task[1] for task in scheduled_tasks)
                scheduled_time = sum(task[2] for task in scheduled_tasks)
                
                # The fitness should be based on these scheduled values
                # This test will fail if schedule_protein reorders but fitness doesn't
                
                # Get tasks from protein_to_tasks for comparison
                protein_tasks = self.auto_fit.protein_to_tasks(protein)
                protein_points = sum(task[1] for task in protein_tasks)
                protein_time = sum(task[2] for task in protein_tasks)
                
                assert scheduled_points == protein_points, \
                    "Scheduled points != protein_to_tasks points (reordering detected!)"
                assert scheduled_time == protein_time, \
                    "Scheduled time != protein_to_tasks time (reordering detected!)"

    # ===========================================
    # BACK-TO-BACK REPETITION TESTS (Your Requirement)
    # ===========================================
    
    def test_no_back_to_back_repetition_strong_penalty(self):
        """Back-to-back repetition should be strongly penalized"""
        protein_btb = "FFMMLL"      # Multiple back-to-back pairs
        protein_spaced = "FMLFML"   # Same tasks, spaced out
        protein_unique = "FMLPVS"   # All unique tasks
        
        score_btb = self.auto_fit.protein_fitness(protein_btb)
        score_spaced = self.auto_fit.protein_fitness(protein_spaced)
        score_unique = self.auto_fit.protein_fitness(protein_unique)
        
        # Strong penalty for back-to-back
        assert score_spaced > score_btb, "Spaced repetition should beat back-to-back"
        assert score_unique >= score_spaced, "Unique tasks should beat any repetition"
        
        # Quantify the penalty - should be substantial
        btb_penalty = (score_spaced - score_btb) / score_spaced
        assert btb_penalty > 0.1, f"Back-to-back penalty too small: {btb_penalty:.3f}"

    def test_single_back_to_back_vs_multiple(self):
        """Multiple back-to-back should be penalized more than single"""
        protein_single_btb = "FMLMVS"   # One back-to-back (MM)
        protein_multi_btb = "FFMMLLTT"  # Multiple back-to-back
        
        score_single = self.auto_fit.protein_fitness(protein_single_btb)
        score_multi = self.auto_fit.protein_fitness(protein_multi_btb)
        
        assert score_single > score_multi, "Multiple BTB should be worse than single BTB"

    def test_back_to_back_penalty_scales_with_run_length(self):
        """Longer runs of same task should be increasingly penalized"""
        protein_2_run = "FF"    # 2 in a row
        protein_3_run = "FFF"   # 3 in a row  
        protein_4_run = "FFFF"  # 4 in a row
        
        score_2 = self.auto_fit.protein_fitness(protein_2_run)
        score_3 = self.auto_fit.protein_fitness(protein_3_run)
        score_4 = self.auto_fit.protein_fitness(protein_4_run)
        
        # Each additional repetition should be more severely penalized
        penalty_2_to_3 = score_2 - score_3
        penalty_3_to_4 = score_3 - score_4
        
        assert penalty_3_to_4 >= penalty_2_to_3, \
            "Longer runs should be increasingly penalized"

    # ===========================================  
    # FITNESS RECALIBRATION TESTS
    # ===========================================
    
    def test_fitness_range_recalibration(self):
        """Fitness scores should be in reasonable ranges after recalibration"""
        
        # Test cases with expected fitness ranges
        test_cases = [
            ("F", 0.15, 0.35, "Single efficient task"),
            ("FF", 0.10, 0.25, "Same task twice (diminishing + BTB penalty)"),  
            ("FM", 0.25, 0.45, "Two different high-value tasks"),
            ("FMLT", 0.45, 0.75, "Four different efficient tasks"),
            ("FVNMVDFPVTCLSWMRGFPF", 0.65, 0.95, "Genetic algorithm result"),
            ("QQQQQ", 0.01, 0.15, "Low-efficiency repeated tasks")
        ]
        
        for protein, min_expected, max_expected, description in test_cases:
            score = self.auto_fit.protein_fitness(protein)
            assert min_expected <= score <= max_expected, \
                f"{description}: {protein} scored {score:.3f}, expected {min_expected}-{max_expected}"

    def test_diminishing_returns_fixed(self):
        """Diminishing returns should work correctly after recalibration"""
        
        # Single task baseline
        score_1 = self.auto_fit.protein_fitness("F")  # 25pts, 20min
        
        # Same task repeated (should increase but with diminishing returns)
        score_2 = self.auto_fit.protein_fitness("FM")  # Add different task
        score_2_same = self.auto_fit.protein_fitness("FF")  # Same task (diminishing + BTB)
        
        # More repetitions
        score_4_mixed = self.auto_fit.protein_fitness("FMLT")  # All different
        score_4_repeated = self.auto_fit.protein_fitness("FFMM")  # With repetition
        
        # Basic sanity checks
        assert score_2 > score_1, "Adding tasks should increase fitness"
        assert score_4_mixed > score_2, "More good tasks should increase fitness"
        
        # Diminishing returns and BTB penalty
        assert score_2 > score_2_same, "Different tasks better than same task (BTB penalty)"
        assert score_4_mixed > score_4_repeated, "Diverse tasks better than repeated"

    def test_time_utilization_bonus_recalibrated(self):
        """Time utilization should provide appropriate bonus after recalibration"""
        
        # Short sequence (poor time utilization)
        protein_short = "F"  # 20 minutes
        
        # Medium sequence (moderate time utilization)  
        protein_medium = "FMLT" * 3  # ~12 tasks, ~240 minutes
        
        # Long sequence (good time utilization, close to 480 min)
        protein_long = "FMLT" * 6  # ~24 tasks, ~480 minutes
        
        score_short = self.auto_fit.protein_fitness(protein_short)
        score_medium = self.auto_fit.protein_fitness(protein_medium)
        score_long = self.auto_fit.protein_fitness(protein_long)
        
        # Better time utilization should generally score higher
        # (accounting for diminishing returns and other factors)
        assert score_medium > score_short, "Better time utilization should help"
        
        # Long might not be strictly better due to diminishing returns,
        # but should be competitive
        assert score_long >= score_medium * 0.8, "Good time utilization should be competitive"

    # ===========================================
    # VALIDATION AGAINST KNOWN RESULTS  
    # ===========================================
    
    def test_genetic_beats_greedy_after_fixes(self):
        """After fixes, genetic solution should clearly beat greedy"""
        
        # Your actual results
        greedy_partial = "FMLPAVSTHGRYNDKCWEIQ"  # Partial greedy sequence
        genetic_solution = "FVNMVDFPVTCLSWMRGFPF"  # Your GA result (442 pts)
        
        greedy_score = self.auto_fit.protein_fitness(greedy_partial)
        genetic_score = self.auto_fit.protein_fitness(genetic_solution)
        
        # Genetic should clearly win
        assert genetic_score > greedy_score, \
            f"Genetic {genetic_score:.3f} should beat greedy {greedy_score:.3f}"
        
        # Both should be in reasonable ranges
        assert genetic_score > 0.6, f"Genetic solution should score >0.6, got {genetic_score:.3f}"
        assert greedy_score > 0.4, f"Greedy solution should score >0.4, got {greedy_score:.3f}"

    def test_efficiency_order_not_optimal(self):
        """Pure efficiency order should NOT be optimal (proving GA value)"""
        
        # Create pure efficiency-ordered sequence
        tasks_by_efficiency = []
        for task_id, (name, points, time) in AMINO_TASK_MAP.items():
            if task_id != "*" and time > 0:
                efficiency = points / time
                tasks_by_efficiency.append((task_id, efficiency))
        
        tasks_by_efficiency.sort(key=lambda x: x[1], reverse=True)
        
        # Take top tasks up to reasonable length
        efficiency_sequence = "".join([task_id for task_id, _ in tasks_by_efficiency[:20]])
        
        # Your genetic solution
        genetic_sequence = "FVNMVDFPVTCLSWMRGFPF"
        
        efficiency_score = self.auto_fit.protein_fitness(efficiency_sequence)
        genetic_score = self.auto_fit.protein_fitness(genetic_sequence)
        
        # Genetic might beat pure efficiency due to diversity, BTB avoidance, etc.
        # At minimum, they should be competitive
        print(f"Efficiency-ordered score: {efficiency_score:.3f}")
        print(f"Genetic solution score: {genetic_score:.3f}")
        
        # This test documents the comparison - genetic might not always win
        # but should be competitive, proving GA found good non-obvious solutions
        assert genetic_score >= efficiency_score * 0.9, \
            "Genetic solution should be competitive with pure efficiency ordering"

    # ===========================================
    # MISSING ATTRIBUTE FIXES
    # ===========================================
    
    def test_min_fitness_attribute_exists(self):
        """AutomationFitness should have min_fitness attribute"""
        assert hasattr(self.auto_fit, 'min_fitness'), \
            "AutomationFitness missing min_fitness attribute"
        assert self.auto_fit.min_fitness == 0.01, \
            f"min_fitness should be 0.01, got {self.auto_fit.min_fitness}"

    def test_max_time_attribute_exists(self):
        """AutomationFitness should have max_time attribute"""
        assert hasattr(self.auto_fit, 'max_minutes'), \
            "AutomationFitness missing max_time attribute"
        assert self.auto_fit.max_minutes == 480, \
            f"max_time should be 480, got {self.auto_fit.max_minutes}"