# compare_results.py
# from lib.binary_genome import BinaryAlgorithm
from lib.knapsack import greedy_knapsack
from lib.automation_fitness import AutomationFitness
from lib.hybrid_genome import HybridGenome
from lib.bio_genome import Genome

import random
from lib.fitness_wrappers import dna_only_wrapper
from lib.run_bio_ga import run_bio_ga_evolution
from lib.weasel import weasel_run
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


    return results

####weasel##

def compare_ga_vs_weasel(target_dna, generations=200, pop_size=100, mu=0.0128, offspring=100):
    """
    Run a GA using DNA-only fitness and a Weasel baseline for comparison.

    Args:
        target_dna (str): DNA target sequence.
        generations (int): Number of generations for both GA and Weasel.
        pop_size (int): Population size for GA.
        mu (float): Mutation probability for Weasel.
        offspring (int): Number of offspring per generation in Weasel.

    Returns:
        dict: {'ga_history': [...], 'weasel_history': [...]}
    """
    # Ensure uppercase DNA
    target_dna = target_dna.upper()
    genome = Genome()

    # --- GA Run ---
    fitness_func = dna_only_wrapper(target_dna, genome, enforce_start_stop=False)

    ga_result = genome.run_evolution(
        fitness_func=fitness_func,
        length=len(target_dna),
        population_size=pop_size,
        iterations=generations,
        normalized=True,
        verbose=False
    )

    # --- Convert GA history to standard format ---
    ga_history = []
    running_best = -1.0
    best_string = ""

    for gen, pop in enumerate(ga_result.get("history", []), start=1):
        if isinstance(pop, dict):
            dna_seq = pop.get("best_string") or pop.get("dna") or ""
            fitness_val = float(pop.get("gen_best", pop.get("fitness", fitness_func(dna_seq))))
        elif isinstance(pop, str):
            dna_seq = pop
            fitness_val = fitness_func(dna_seq)
        else:
            dna_seq = ""
            fitness_val = 0.0

        dna_seq = dna_seq[:len(target_dna)]

        if fitness_val > running_best:
            running_best = fitness_val
            best_string = dna_seq

        ga_history.append({
            "generation": gen,
            "gen_best": fitness_val,
            "running_best": running_best,
            "avg": fitness_val,
            "best_string": best_string,
            "dna": dna_seq
        })

    # --- Override last generation's best_string with GA's actual best ---
    best_dna = ga_result.get("dna")  # best_overall DNA
    if ga_history and best_dna:
        ga_history[-1]["best_string"] = best_dna

    # --- Weasel Run ---
    weasel_history = weasel_run(
        target_dna=target_dna,
        genome=genome,
        L=len(target_dna),
        mu=mu,
        offspring=offspring,
        max_gens=generations,
        verbose=False
    )

    return {
        "ga_history": ga_history,
        "weasel_history": weasel_history
    }

