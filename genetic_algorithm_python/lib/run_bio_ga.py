import random
from collections import Counter
from lib.genome_fitness import dna_fitness
from lib.bio_genome import Genome
from lib.automation_fitness import AutomationFitness

from lib.reporting import print_run_specs, print_task_schedule, print_ga_history, print_bio_ga_result
from lib.fitness_wrappers import automation_fitness_wrapper, dna_fitness_wrapper


def run_bio_ga_evolution(target_dna, generations=100, pop_size=10, enforce_start_stop=False):
    """
    Run GA on a target DNA sequence using dna_fitness with optional start codon enforcement.
    Outputs detailed GA run info using reporting functions.
    """
    genome = Genome()
    target_dna = target_dna.upper()
    target_protein = genome.protein(genome.dna_to_rna(target_dna))

    # Wrap the fitness function
    fitness_func = dna_fitness_wrapper(target_dna, genome, enforce_start_stop=enforce_start_stop)

    # Run GA
    result = genome.run_evolution(
        fitness_func=fitness_func,
        length=len(target_dna),
        population_size=pop_size,
        iterations=generations,
        normalized=True,
        verbose=False  # suppress internal prints; reporting handles output
    )

    # Compute detailed stats
    dna_score, protein_score, combined_score = dna_fitness(
        result["dna"],
        target_dna,
        genome,
        enforce_start_stop=enforce_start_stop
    )

    # Retrieve GA history
    history = result.get("history", [])

    # Determine first generation where the best solution appeared
    first_best_gen = None
    if history:
        try:
            first_best_gen = next(
                h.get("generation", h.get("gen"))
                for h in history
                if h["running_best"] == result["fitness"]
            )
        except StopIteration:
            first_best_gen = None

    # Print GA evolution history every 100 generations
    print_ga_history(history, label="BioGA Evolution History")

    # Print summary using reporting function
    print_bio_ga_result(
        result,
        target_protein,
        dna_score,
        protein_score,
        combined_score,
        genome,
        first_best_gen
    )
    return {
        "dna": result["dna"],
        "protein_seq": genome.protein(genome.dna_to_rna(result["dna"])),
        "dna_fitness": dna_score,
        "protein_fitness": protein_score,
        "combined_fitness": combined_score,
        "history": history,
        "first_best_gen": first_best_gen,
        "target_protein": target_protein
    }



def run_auto_ga_evolution(
    amino_task_map=None,
    generations=500,
    pop_size=100,
    normalized=False,
    verbose=True
):
    """Run GA using AutomationFitness (task-based protein evaluation)."""
    genome = Genome()
    auto_fitness = AutomationFitness(amino_task_map=amino_task_map)
    fitness_func = automation_fitness_wrapper(genome, auto_fitness)

    result = genome.run_evolution(
        fitness_func=fitness_func,
        length=9,
        population_size=pop_size,
        iterations=generations,
        normalized=normalized,
        verbose=False
    )

    # Decode best sequence
    rna_seq = genome.dna_to_rna(result["dna"])
    protein_seq = genome.protein(rna_seq)
    tasks_list = auto_fitness.protein_to_tasks(protein_seq)

    # Filter by time
    cum_time = 0.0
    filtered_tasks = []
    for task, pts, duration in tasks_list:
        if cum_time + duration > auto_fitness.max_minutes:
            break
        filtered_tasks.append((task, pts, duration))
        cum_time += duration

    final_score = auto_fitness.protein_fitness(protein_seq)

    if verbose:
        print_ga_history(result.get("history", []), label="AutoGA")
        print_run_specs(
            pop_size, generations,
            0, 0, 0, 0, 0,  # placeholders for GA params
            True, True, normalized, final_score, protein_seq
        )
      
        # Print GA history every 100 gens
      
        print_task_schedule(filtered_tasks, max_minutes=auto_fitness.max_minutes)

    return {
        "protein_seq": protein_seq,
        "tasks_list": filtered_tasks,
        "fitness_score": final_score,
        "history": result.get("history", [])
    }
if __name__ == "__main__":
    # run_auto_ga_evolution()
    target = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatcttgttttgcatgaaaattatgacgaacataataaagttattaaagatgagaaatggagattgaatgagtgttcttttcctcatgctttgtatgaatatatctttttaccatgtagaaagtgtgtaggatgtcgttcagataacgctaaaatgtggtctcttcgtgcatataatgagatgaaattacataaaaagaattgttttataactttgacttatgataatgcttcagatttggtcgtaaaagaccctctatgtattgctagtttaagatataaacattttcaaaattttatgaaaagattacgtaagaaaactggtaaaaaattaggttatcttgtatgtggtgagtatggtttaaaagatggtagagctcattggcatgcaatattatttgattttgattttgaagataaggagttaatctatgttaaaaaaggatataaacactattattcaacactacttcaagagtgttggtcgacgtatgacaaaaaaacagactcgtataatccgattggttttattgaccttgctgattgcgattatgactgttgtagttatgtttctcagtatgtgcttaaaaaattacctgttaatcagaatggcattgctgttggttcctatgttgatgatgtaactggtgaagttaaagatattgagttaactgatgtatgtccacctatggttaggagttctaaaaatcctgctataggttataattggtataagaaatttggagagaatgcatgtgaaaaaggttttatccctattgttacgaatgaaggtaagaaggttcgtaaagttcgtacgcctgcttattactattctaaatttgaagtagataatcctcaaaaatttgaaatattaaaaaatgttaaggaagaaaaaatgagaaaatattacaaggaaaatccaatagatttagataaattgaattcttggagtgaagctcatttatatagaattaaaaaacggatgaaagaggtattgacacattttaaaaaatagtttatat"
    run_bio_ga_evolution(target)