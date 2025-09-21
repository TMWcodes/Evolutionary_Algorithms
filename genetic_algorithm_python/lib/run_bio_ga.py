# Import Genome class and fitness functions
import random
from lib.bio_genome import Genome
import lib.genome_fitness as gf
from lib.automation_fitness import AutomationFitness  # your module
from collections import Counter

# Wrapper function to run the GA on a target DNA
def run_bio_ga_evolution(target_dna, generations=2000, pop_size=100):
    # Initialize genome object
    genome = Genome()

    # Compute target protein from target DNA for reporting
    target_protein = genome.protein(genome.dna_to_rna(target_dna))

    # Fitness wrapper for GA: only returns combined fitness (GA uses this for selection)
    def fitness_wrapper(dna):
        """
        Wrapper to evaluate DNA fitness for GA.
        Adds small length normalization to prevent very long sequences from dominating.
        """
        dna_score, protein_score, combined = gf.dna_fitness(dna, target_dna, genome)

        # Penalize sequences that are excessively longer than target
        length_penalty = min(1.0, len(target_dna)/len(dna)) if len(dna) > len(target_dna) else 1.0

        # Slight bonus for sequences containing repeated motifs (to encourage modular assembly)
        repeat_bonus = 1.0 + 0.05 * (len(dna) - len(set(dna))) / len(dna)

        # Combine modifiers with the GA fitness
        combined_adj = combined * length_penalty * repeat_bonus

        return combined_adj #Run the GA with the wrapper fitness function
        
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,    # Fitness function to evaluate sequences
        length=len(target_dna),          # Length of DNA sequences
        population_size=pop_size,        # Number of sequences per generation
        iterations=generations,          # Number of generations to evolve
        normalized=True,                # Whether to normalize fitness scores
        verbose=True                    # Print progress per generation
    )

    # After GA finishes, recompute all fitness scores for the best sequence
    dna_score, protein_score, combined = gf.dna_fitness(result["dna"], target_dna, genome)
    best_protein = genome.protein(genome.dna_to_rna(result["dna"]))

    # Print summary of GA results
    print("\n--- GA Result ---")
    # print(f"Target DNA sequence:   {target_dna}")
    # print(f"Best DNA sequence:     {result['dna']}\n")
    print(f"Target protein:        {target_protein}")
    print(f"Best protein:          {best_protein}\n")
    print(f"DNA fitness:           {dna_score:.3f}")
    print(f"Protein fitness:       {protein_score:.3f}")
    print(f"Combined fitness:      {combined:.3f}")



def print_run_specs(pop_size, generations, p_c, p_m, p_recomb, p_transp, p_locdup,
                    use_frames, check_complement, normalized, final_score, protein_seq):
    """Pretty-print GA configuration and high-level results."""
    print("\n--- GA Run Specs ---")
    print(f"Population size: {pop_size}, Generations: {generations}")
    print(f"p_c={p_c}, p_m={p_m}, p_recomb={p_recomb}, p_transp={p_transp}, p_locdup={p_locdup}")
    print(f"use_frames={use_frames}, check_complement={check_complement}, normalized={normalized}")

    print(f"\nBest after {generations} generations: fitness={final_score:.3f}")
    print(f"Translated protein: {protein_seq}")
    print(f"Total amino acids in translated protein: {len(protein_seq)}\n")


def print_task_schedule(filtered_tasks):
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
    print(f"Final cumulative time (hrs): {cum_time / 60:.2f}")

    # Diversity stats
    task_counter = Counter(task_names)
    num_unique_tasks = len(task_counter)
    most_common_task, most_common_count = task_counter.most_common(1)[0]
    print(f"Number of unique tasks: {num_unique_tasks}")
    print(f"Most duplicated task: '{most_common_task}' appears {most_common_count} times")


def run_auto_ga_evolution(
    amino_task_map=None,
    generations=500,
    pop_size=100,
    p_c=0.7,
    p_m=0.002,
    p_recomb=0.05,
    p_transp=0.02,
    p_locdup=0.02,
    use_frames=True,
    check_complement=True,
    normalized=False,
    verbose=True
):
    genome = Genome()
    auto_fitness = AutomationFitness(amino_task_map=amino_task_map)

    # 2. Fitness wrapper
    def fitness_wrapper(dna):
        rna_seq = genome.dna_to_rna(dna)
        protein_seq = genome.protein(rna_seq)
        return auto_fitness.protein_fitness(protein_seq)

    # 3. Run GA
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,
        length=9,
        population_size=pop_size,
        iterations=generations,
        normalized=normalized
    )

    # 4. Decode best DNA
    rna_seq = genome.dna_to_rna(result["dna"])
    protein_seq = genome.protein(rna_seq)
    tasks_list = auto_fitness.protein_to_tasks(protein_seq)

    # Filter tasks to 8 hours max
    cum_time = 0.0
    filtered_tasks = []
    for task, pts, duration in tasks_list:
        if cum_time + duration > auto_fitness.max_minutes:
            break
        filtered_tasks.append((task, pts, duration))
        cum_time += duration

    final_score = auto_fitness.protein_fitness(protein_seq)

    # 5. Human-readable output
    if verbose:
        print_run_specs(
            pop_size, generations, p_c, p_m, p_recomb, p_transp, p_locdup,
            use_frames, check_complement, normalized, final_score, protein_seq
        )
        print_task_schedule(filtered_tasks)

    # 6. Return results for further processing
    return {
        "protein_seq": protein_seq,
        "tasks_list": filtered_tasks,
        "fitness_score": final_score
    }


# Run as script with default target DNA
if __name__ == "__main__":
    run_auto_ga_evolution()

   
   
    target_caps = "TTTAACAACCTGGTATTACTCTCTCTTATATGCTAAAGTGTGCGACTCGAGGGTACTCGG"
    # target = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatcttgttttgcatgaaaattatgacgaacataataaagttattaaagatgagaaatggagattgaatgagtgttcttttcctcatgctttgtatgaatatatctttttaccatgtagaaagtgtgtaggatgtcgttcagataacgctaaaatgtggtctcttcgtgcatataatgagatgaaattacataaaaagaattgttttataactttgacttatgataatgcttcagatttggtcgtaaaagaccctctatgtattgctagtttaagatataaacattttcaaaattttatgaaaagattacgtaagaaaactggtaaaaaattaggttatcttgtatgtggtgagtatggtttaaaagatggtagagctcattggcatgcaatattatttgattttgattttgaagataaggagttaatctatgttaaaaaaggatataaacactattattcaacactacttcaagagtgttggtcgacgtatgacaaaaaaacagactcgtataatccgattggttttattgaccttgctgattgcgattatgactgttgtagttatgtttctcagtatgtgcttaaaaaattacctgttaatcagaatggcattgctgttggttcctatgttgatgatgtaactggtgaagttaaagatattgagttaactgatgtatgtccacctatggttaggagttctaaaaatcctgctataggttataattggtataagaaatttggagagaatgcatgtgaaaaaggttttatccctattgttacgaatgaaggtaagaaggttcgtaaagttcgtacgcctgcttattactattctaaatttgaagtagataatcctcaaaaatttgaaatattaaaaaatgttaaggaagaaaaaatgagaaaatattacaaggaaaatccaatagatttagataaattgaattcttggagtgaagctcatttatatagaattaaaaaacggatgaaagaggtattgacacattttaaaaaatagtttatattgcttgtataataatttaataatttagtttatttacttttatctatatgcctcaaatgtactcgtagcgagggatacagataatatatattatgtaagaaggaggaaaaaaacatgaacacaacaattattaaccaaacgggagaaaacaacgctacaaacgcaagctgtaaagctgattttagcttggtctttgctgtaaaggatttaaagtctgacaattttggttcccttttagtttgtaatacaagcgacgaggcgattagagctactaaggttagattgatgtatgaccaaggaagtatgatacaacaattccctgctgattttatgctttatcacgttggctattttaacacaaaaactggtgttatggaaagtgtcggaatagctattcctgttaagtcaattttagatgttagcttggaattagaacaagagcgaaaagtgaaagctgttgatattccagaatttatgaaaggagaggaaaatgacaatcgatgtgaagaatcaaattctagtgaatgtgttgaaagtattggataaacttatcgatttcattctagaagtattaaacaaagagaatgcataaatgattgatatttgtaaagattgtacattatacgtcttaaaaaaactaggtaggacaatgctttgtgcggagtcctatcttgcacttttaatttacatctttactcatgttagatttagtgtaactttttgcaagaaatttagtaaacttgtcgaccgatatcgagctagtgaaatatacagtacccctagcccgtccggcgatgaggacaaaataaggagaaacaatgaagataaaagttagatggtgtttaaatactgattttatttgtgataaggagaatgaagataatggctaaattttttacaccttatacaactacaaaaaaagttgttgttgaatttaaagagccaagtcttactgatcaatcttataaagatgagtgcgacttaggttttattattgaaaattatgtaagtaaaggaatacctttgccacaatctactatgaattatcaagactgtactactgtccaagattatcaatctgcaatgatgttagttgcagaagctaagtctaattttgaacaattaccttctaaggctagagatgaatttggaactgttgaaaattatcttgatttcatttctaaaccagagaatttaaaaacatcgtatgaaaaaggttatattgacccttctacagttgatttaatggacgtttatccagaaagataccaaacattatctgaacagatagaaactcctactgtagagcctgtggttaatccctctgaaactccttcaacagaggtgacggcataaagtaaatgcaaatagttctcttgttactatttgcatttactgacaccgttaggtggctaaagggtttgaaggttctaaaaccttcaataccccctaaaaaacagttaaaaagaaattaacccgaagggttgtatatattgaattagaaggagattttttatgtatgagatagatagaatgattgaaggttataaagagagacttaatgaaattatttatgatatcggacaatttcaatatcaattaacagaaaaacttaaagacaaacagaatttagaaaaatttattgaaagattagaaagaaaggatgataaaatatgtcaacagtaatggcacaacacggacatcaaatgcactcatttgaatattatccgtcagcacatatttcaagaagtaaatttaaccgttctcattcattgataacaacaatgaatgcaggttatattgttcctatttggcacgatttagcatatcctggcgatacacttattatgtcagctagaacattaacacgtttagctactcaattagtaccatttatgagtaatgtttatatggatatacatttctggtgtgttccacttcgtttagtatgggaacactggacagctatgaatggagaacaactaaatcctggagatagtacagattatttaactccgcaaataacagcaactccaacagtaggcgatatttatgattatttcaatgtacctataggtgttgaatctaagtttaatgcttttaactttagagcatataacttagtttataacgaatggtatcgagatgaaaacttacaagagagagtacctcaaatagtttcagataatgatacagaaagtaattatacacttttaaaacgtggtaagagaaaagattactttacaggagctttaccatggccacaaaaaggcagtgaagttgatttgcctttaggtatatctgcgccagtttctgtatatggtaatggtatgtctttaggattaacagatggttctatagaaatgggttcaattgtttatggtcaacaatattttgttcgtactgctgcatctggggttgatgttggcacagttgtaagcactgctggtagtactggaaataatgtagtcgttggtgtttctagtaatcctgagacctctggtcttattggtactgctgatttatcagatgctacatctgcaactattaactcattacgtcaagctttcgctattcaaaaaatgttagaaaaagatgctagaggtggtacaagatatatcgaaatgatactttcacatttcggtgttaaatctccagatgcaagattacaacgtccagagttcttaggtggtgctacatttgacttaaatctttctgttgttcctcaaacatcagctacaactgaaacttctacacctttaggtgatttggcttcttatggtgttatcaatggttcatcaaaacgtattgtacactcatttactgagcattgtgtagtatttggtgttgctagtattcgctctgaatattattatcaacaaggcttagaaagagattattcaaaacgttcaagaattgatttttatttgcctgttactgctcacttaggagaacaagctgtatataataaagaaatttatgcacaaggtacagacgaagatgaaaatgtatttggttatcaagaacgttggtctgaaatgagatataagaattcttatattactggtcaaacacgttctactgcaagtcaacctttagattattggcatttaggtcaagagtttgcaagcttgcctgctcttaacgctgagtttattcaagaaaaccctcctattgatagagttattgctcttcaagagtcagaaaatactcctcaatttatttgtaattttttctttgatgagtattgggtaagacctatgcctgtatattctactccaggtatgcaatcacacttttaagttatatcggtacgatagagtgagatttttaatctcgctctattgaaccgaaaggaaggataatattatggcagattggttaagttctttaatttctggtggttttaatatggctggtcaagctattaattataactatcaaaagaggttaatggaaaaacaatatgatttgaatataaaaggtttaaaggaaagtcctttagctattcgtacaggtttggagagtgcaggatataatcctataacttttgcaggtcaaactaacgctagtgctagtgtaggttctgctccttctgtatctgatagtaatttgggtactagtattgttaatgcttatcaacaaaacaaattaaatgaagctaatgttgatgcaacaaatgctcaagcagaattgtctaatgaacaagccaaaactgaacaagcgaaaagaactaatcttgagtttcaaaatcgtatgttagatgttgaaaaacatttaaaacaaaaagatttagatacttatgatagacgtttttatacacaactttatgaacaaatgcagagagcagaaaattatagagctatggcaaatttacaaggttataatgccgagtctcaacgtatagcttctaatgctcaaatgcttggttcacaagctagacaatcagacgctgttactaatagatatttagcaaagtatggtactcctcaacgtagttttttaactttgttaaataagcctaaaactaaaggaaaatattaattccatttttcagcagtttttacacctaaccaaaatataactattatacaaaataattcaaacataaggagattttacaatgaaaagaaaacaactgtcaaggaaagcaggtgctaagatgtttaaacgttctggtcaaatgatgaactctaaaaatcagcctaagatttctagaggtggtattagattttagtactcctatttaacacacatagtccaagaggagtttttactcctctttttttaagagaggaatgtatat".replace("\n", "")  # Example DNA
    # target_caps = target.upper()

    # run_bio_ga_evolution(target_caps)
  
