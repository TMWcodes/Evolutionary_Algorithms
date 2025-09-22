import random
from collections import Counter
from lib.genome_fitness import dna_fitness
from lib.bio_genome import Genome
from lib.automation_fitness import AutomationFitness

from lib.reporting import print_run_specs, print_task_schedule, print_schedule_result
from lib.fitness_wrappers import automation_fitness_wrapper, dna_fitness_wrapper


def run_bio_ga_evolution(target_dna, generations=2000, pop_size=100, enforce_start_stop=False):
    """Run GA on a target DNA sequence using dna_fitness with optional start codon enforcement."""
    genome = Genome()
    target_protein = genome.protein(genome.dna_to_rna(target_dna))

    # Wrap the fitness function with toggle
    fitness_func = dna_fitness_wrapper(target_dna, genome, enforce_start_stop=enforce_start_stop)

    # Run the GA
    result = genome.run_evolution(
        fitness_func=fitness_func,
        length=len(target_dna),
        population_size=pop_size,
        iterations=generations,
        normalized=True,
        verbose=True
    )

    # Compute best sequence stats
    dna_score, protein_score, combined = dna_fitness(
        result["dna"],
        target_dna,
        genome,
        enforce_start_stop=enforce_start_stop
    )
    best_protein = genome.protein(genome.dna_to_rna(result["dna"]))

    print("\n--- GA Result ---")
    print(f"Target protein: {target_protein}")
    print(f"Best protein:   {best_protein}\n")
    print(f"DNA fitness:    {dna_score:.3f}")
    print(f"Protein fitness:{protein_score:.3f}")
    print(f"Combined fitness:{combined:.3f}")


def run_auto_ga_evolution(
    amino_task_map=None,
    generations=500,
    pop_size=100,
    normalized=False,
    verbose=False
):
    """Run GA using AutomationFitness (task-based protein evaluation)."""
    genome = Genome()
    auto_fitness = AutomationFitness(amino_task_map=amino_task_map)

    fitness_func = automation_fitness_wrapper(genome, auto_fitness)

    # Run the GA
    result = genome.run_evolution(
        fitness_func=fitness_func,
        length=9,
        population_size=pop_size,
        iterations=generations,
        normalized=normalized
    )

    # Decode best sequence
    rna_seq = genome.dna_to_rna(result["dna"])
    protein_seq = genome.protein(rna_seq)
    tasks_list = auto_fitness.protein_to_tasks(protein_seq)

    # Filter tasks to max time
    cum_time = 0.0
    filtered_tasks = []
    for task, pts, duration in tasks_list:
        if cum_time + duration > auto_fitness.max_minutes:
            break
        filtered_tasks.append((task, pts, duration))
        cum_time += duration

    final_score = auto_fitness.protein_fitness(protein_seq)

    # Reporting
    if verbose:
        print_run_specs(
            pop_size, generations, 0, 0, 0, 0, 0,  # placeholders for GA params
            True, True, normalized, final_score, protein_seq
        )
        print_task_schedule(filtered_tasks, max_minutes=auto_fitness.max_minutes)


    return {
        "protein_seq": protein_seq,
        "tasks_list": filtered_tasks,
        "fitness_score": final_score
    }

# if __name__ == "__main__":
#     run_auto_ga_evolution()