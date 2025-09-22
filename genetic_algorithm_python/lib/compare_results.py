# compare_results.py
from lib.knapsack import greedy_knapsack
from lib.automation_fitness import AutomationFitness
from lib.hybrid_genome import HybridGenome
from lib.bio_genome import Genome
from lib.binary_genome import BinaryAlgorithm
#####knapsack###
def compare_knapsack_ga(amino_task_map, capacity, ga_result):
    """
    Compare GA output to greedy knapsack result under the same time capacity.

    Both GA and Knapsack results are truncated/limited to `capacity` minutes.

    Parameters:
        amino_task_map: dict mapping amino codes to (task_name, points, duration)
        capacity: max time in minutes
        ga_result: dict returned by run_auto_ga_evolution

    Returns:
        dict with Knapsack and GA summary
    """
    auto_fitness = AutomationFitness(amino_task_map)

    # --- Knapsack ---
    knapsack_schedule, knapsack_points, knapsack_time = greedy_knapsack(amino_task_map, capacity)
    knapsack_task_string = ''.join([s[0] for s in knapsack_schedule])
    knapsack_fitness = auto_fitness.protein_fitness(knapsack_task_string)

    # --- GA (truncate to same capacity) ---
    task_to_code = {v[0]: k for k, v in amino_task_map.items()}
    cum_time = 0
    filtered_tasks = []
    for t in ga_result["tasks_list"]:
        if cum_time + t[2] > capacity:
            break
        filtered_tasks.append(t)
        cum_time += t[2]

    ga_task_string = ''.join([task_to_code[t[0]] for t in filtered_tasks])
    ga_points = sum(t[1] for t in filtered_tasks)
    ga_time = cum_time
    ga_fitness = auto_fitness.protein_fitness(ga_task_string)

    return {
        "time_capacity": capacity,
        "Knapsack": {
            "task_string": knapsack_task_string,
            "points": knapsack_points,
            "time_used": knapsack_time,
            "fitness": knapsack_fitness
        },
        "GA": {
            "task_string": ga_task_string,
            "points": ga_points,
            "time_used": ga_time,
            "fitness": ga_fitness
        }
    }




####GA#####


def compare_models(fitness_func, target_length, iterations=200, population_size=30, verbose=False):
    """
    Run BioGA, HybridGA, and BinaryGA on the same fitness function.
    Returns a dict with standardized results, including history for reporting.
    """
    results = {}

    # --- BioGA ---
    bio = Genome()
    bio_result = bio.run_evolution(
        fitness_func=fitness_func,
        length=target_length,
        iterations=iterations,
        population_size=population_size,
        verbose=False  # suppress internal prints
    )
    results['bio'] = {
        "best": bio_result['dna'],
        "fitness": bio_result['fitness'],
        "history": bio_result.get('history', [])
    }

    # --- HybridGA ---
    hyb = HybridGenome()
    hyb_result = hyb.run_evolution(
        fitness_func=fitness_func,
        length=target_length,
        iterations=iterations,
        population_size=population_size,
        verbose=False
    )
    # Hybrid result may also be dict with dna/fitness/history
    if isinstance(hyb_result, dict) and 'dna' in hyb_result:
        hyb_best = hyb_result['dna']
        hyb_fitness = hyb_result['fitness']
        hyb_history = hyb_result.get('history', [])
    else:
        hyb_best = hyb_result
        hyb_fitness = fitness_func(hyb_best)
        hyb_history = []
    results['hybrid'] = {
        "best": hyb_best,
        "fitness": hyb_fitness,
        "history": hyb_history
    }

    # --- BinaryGA ---
    # bin_ga = BinaryAlgorithm()
    # bin_best = bin_ga.run(
    #     length=target_length,
    #     iterations=iterations,
    #     p_c=0.7,
    #     p_m=0.01
    # )
    # results['binary'] = {
    #     "best": bin_best,
    #     "fitness": fitness_func(bin_best),
    #     "history": []  # BinaryAlgorithm run returns only the best sequence
    # }

    return results
