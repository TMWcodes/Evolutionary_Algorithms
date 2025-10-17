from lib.run_bio_ga import run_auto_ga_evolution
from lib.automation_fitness import AMINO_TASK_MAP
from lib.compare_results import compare_knapsack_ga, compare_models, compare_ga_vs_weasel
# from lib.reporting import print_comparison, print_ga_results

# ---------- Knapsack comparison ----------
# -----------------------------
# Configuration
# -----------------------------
# Knapsack
KNAPSACK_CAPACITY = 120  # minutes

# GA vs Weasel
TARGET_DNA = "ATGACATGTTATAGTCCTATTCCTGCTTGCTTTAGTAAATCACAATATGCTAAGACAGGAAAGAAAAATATACATGAC"
GENERATIONS = 200
POP_SIZE = 100
MU = 0.0128
OFFSPRING = 100

CSV_EXPORT = True
CSV_FILE = "ga_vs_weasel_comparison.csv"


# -----------------------------
# Functions for each comparison
# -----------------------------
def run_knapsack_comparison():
    print("=== Knapsack Comparison ===")
    # Run GA and compare to Greedy Knapsack
    ga_result = None  # Replace with actual GA run if needed
    comparison = compare_knapsack_ga({}, capacity=KNAPSACK_CAPACITY, ga_result=ga_result)
    print(comparison)


def run_ga_model_comparison():
    print("=== GA Model Comparison ===")
    # Simple base-by-base fitness for demonstration
    TARGET_SEQ = "ATGCATGC"
    def fitness(dna):
        return sum(1 for a, b in zip(dna, TARGET_SEQ) if a == b) / len(TARGET_SEQ)

    results = compare_models(
        fitness_func=fitness,
        target_length=len(TARGET_SEQ),
        iterations=200,
        population_size=30,
        verbose=False
    )

    for model_name, model_result in results.items():
        print(f"{model_name} Best Fitness: {model_result['fitness']}, Best DNA: {model_result['best']}")


def run_ga_vs_weasel_comparison():
    results = compare_ga_vs_weasel(
        target_dna=TARGET_DNA,
        generations=GENERATIONS,
        pop_size=POP_SIZE,
        mu=MU,
        offspring=OFFSPRING
    )

    ga_history = results["ga_history"]
    weasel_history = results["weasel_history"]

    final_ga = ga_history[-1]
    final_weasel = weasel_history[-1]

    print("=== GA vs Weasel Comparison ===")
    print(f"Target DNA: {TARGET_DNA}\n")  # <-- Add this line

    print(f"GA Final - Generation {final_ga['generation']}, Best Fitness {final_ga['running_best']:.4f}")
    print(f"Best String: {final_ga['best_string']}\n")
    print(f"Weasel Final - Generation {final_weasel['generation']}, Best Fitness {final_weasel['running_best']:.4f}")
    print(f"Best String: {final_weasel['best_string']}")

    return results
    

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    # Run comparisons in order
    # run_knapsack_comparison()    # Uncomment if you have GA for Knapsack
    # run_ga_model_comparison()    # Uncomment to compare BioGA, HybridGA, BinaryGA
    run_ga_vs_weasel_comparison()  # Currently active comparison