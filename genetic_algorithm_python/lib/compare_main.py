from lib.run_bio_ga import run_auto_ga_evolution
from lib.automation_fitness import AMINO_TASK_MAP
from lib.compare_results import compare_knapsack_ga, compare_models
from lib.reporting import print_comparison, print_ga_results

# ---------- Knapsack comparison ----------
def compare_knapsack(capacity):
    # 1️⃣ Run GA with AutomationFitness
    print("Running GA...")
    ga_result = run_auto_ga_evolution()

    # 2️⃣ Compare GA output to Greedy Knapsack
    comparison = compare_knapsack_ga(AMINO_TASK_MAP, capacity=capacity, ga_result=ga_result)

    # 3️⃣ Print a clean summary
    print("\n=== GA vs Greedy Knapsack Comparison ===")
    print_comparison(comparison)


# ---------- GA comparison ----------
TARGET_SEQ = "ATGCATGC"

def fitness(dna):
    """Simple base-by-base matching fitness."""
    return sum(1 for a, b in zip(dna, TARGET_SEQ) if a == b) / len(TARGET_SEQ)

if __name__ == "__main__":
    # Run GA comparison across all models
    results = compare_models(
        fitness_func=fitness,
        target_length=len(TARGET_SEQ),
        iterations=200,
        population_size=30,
        verbose=False  # suppress internal GA prints; handled centrally
    )

    # Centralized printing
    # print("---- GA Comparison ----")
    print_ga_results(results)