from collections import Counter

def print_run_specs(pop_size, generations, p_c, p_m, p_recomb, p_transp, p_locdup,
                    use_frames, check_complement, normalized, final_score, protein_seq,
                    first_best_gen=None):
    print("\n--- GA Run Specs ---")
    if first_best_gen is not None:
        print(f"Best solution first found at generation: {first_best_gen}")
    print(f"\nBest after {generations} generations: fitness={final_score:.3f}")
    print(f"Population size: {pop_size}, Generations: {generations}")
    print(f"p_c={p_c}, p_m={p_m}, p_recomb={p_recomb}, p_transp={p_transp}, p_locdup={p_locdup}")
    print(f"use_frames={use_frames}, check_complement={check_complement}, normalized={normalized}")
    print("\n")
    print(f"Translated protein: {protein_seq}")
    print(f"Total amino acids in translated protein: {len(protein_seq)}\n")

def print_task_schedule(filtered_tasks, max_minutes):
    """Pretty-print the task schedule with summary statistics."""
    if not filtered_tasks:
        print("Task list: (none)")
        return

    print("Task Schedule:")
    print(f"{'Idx':<4} {'Task':<25} {'Pts':<5} {'Time(min)':<10} {'Cum.Time(min)':<12} {'Cum.Pts':<8}")
    print("-" * 75)

    cum_time, cum_pts = 0.0, 0.0
    task_names = []

    for i, (task, pts, duration) in enumerate(filtered_tasks, start=1):
        cum_time += duration
        cum_pts += pts
        task_names.append(task)
        print(f"{i:<4} {task:<25} {pts:<5} {duration:<10.1f} {cum_time:<12.1f} {cum_pts:<8.1f}")

    # Summary
    print(f"\nTotal points: {cum_pts}")
    print(f"Final time / total time: {cum_time / 60:.2f} / {max_minutes / 60:.2f} hrs")

    # Diversity stats
    task_counter = Counter(task_names)
    num_unique_tasks = len(task_counter)
    most_common_task, most_common_count = task_counter.most_common(1)[0]
    print(f"Number of unique tasks: {num_unique_tasks}")
    print(f"Most duplicated task: '{most_common_task}' appears {most_common_count} times")


def print_schedule_result(result, label="Knapsack"):
    """
    Unified summary for deterministic (Knapsack) or GA results.
    Expects dict with:
        schedule, task_string, total_points, total_time, capacity, fitness_score
    """
    print(f"\n--- {label} Result ---")
    print_task_schedule(
        [(name, pts, t) for _, name, pts, t in result["schedule"]],
        result["capacity"]
    )

    print("\nTask string:", result["task_string"])
    print(f"Total points: {result['total_points']}")
    print(f"Time used: {result['total_time']} / {result['capacity']}")
    print(f"Fitness score: {result['fitness_score']:.3f}")

def print_ga_compare_results(results, label="GA Comparison"):
    """
    Nicely print GA comparison results for Bio and Hybrid.
    Includes the generation where the best solution was first found.

    Parameters:
        results: dict with keys "bio" and "hybrid"
                 each contains {"best": str, "fitness": float, "history": list of dicts}
        label: title for the output
    """
    print(f"\n--- {label} ---")
    for model in ["bio", "hybrid"]:
        r = results.get(model, {})
        best = r.get("best", "")
        fitness = r.get("fitness", 0.0)
        history = r.get("history", [])

        # Find first generation where best fitness appeared
        if history:
            try:
                sol_gen = next(
                    h.get("generation", h.get("gen"))  # fallback to 'gen' if 'generation' missing
                    for h in history
                    if h["running_best"] == fitness
                )
            except StopIteration:
                sol_gen = 0
            print(f"{model.capitalize():<10}: {best} (Fitness: {fitness:.3f}, Found at Gen {sol_gen})")


def print_bio_ga_result(result, target_protein, dna_fitness, protein_fitness, combined_fitness, genome, first_best_gen=None):
    best_dna = result["dna"]
    best_protein = genome.protein(genome.dna_to_rna(best_dna))

    print("\n--- BioGA Result ---")
    if first_best_gen is not None:
        print(f"Best solution first found at generation: {first_best_gen}")

    print(f"Target Amino acid length: {len(target_protein)} amino acids")
    print(f"Total amino acids in best protein: {len(best_protein)}")
    print(f"\nTarget protein: {target_protein}")
    print(f"Best protein:   {best_protein}\n")
    print(f"DNA fitness:    {dna_fitness:.3f}")
    print(f"Protein fitness:{protein_fitness:.3f}")
    print(f"Combined fitness:{combined_fitness:.3f}")



def print_knapsack_comparison(comparison):
    """Print a clean summary of Knapsack vs GA results."""
    print(f"Time capacity: {comparison['time_capacity']} min\n")
    for method in ["Knapsack", "GA"]:
        stats = comparison[method]
        print(f"{method}:")
        print(f"  Task string: {stats['task_string']}")
        print(f"  Points: {stats['points']}, Time used: {stats['time_used']}")
        print(f"  Fitness: {stats['fitness']:.3f}\n")

# reporting.py

def print_ga_history(history, label="GA"):
    """
    Print the evolution history for a GA run every 100 generations.

    Parameters:
        history: list of dicts, each with keys 'gen', 'gen_best', 'running_best', 'avg'
        label: string to identify the GA (e.g., "BioGA", "HybridGA")
    """
    if not history:
        print(f"{label} history is empty.")
        return

    print(f"\n=== {label} Evolution History ===")
    for entry in history:
        gen = entry.get("generation", entry.get("gen", 0))
        if gen % 100 != 0 and gen != history[-1].get("generation", history[-1].get("gen", 0)):
            continue  # skip unless multiple of 100 or last generation

        gen_best = entry["gen_best"]
        running_best = entry["running_best"]
        avg = entry["avg"]
        print(f"Gen {gen:03d}: Gen Best {gen_best:.3f}, Running Best {running_best:.3f}, Avg {avg:.3f}")
        