# Import Genome class and fitness functions
import random
from lib.bio_genome import Genome
import lib.genome_fitness as gf
from lib.automation_fitness import AutomationFitness  # your module

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






def run_auto_ga_evolution(amino_task_map=None, generations=500, pop_size=20, verbose=True):
    """
    Runs a GA to evolve DNA sequences that maximize AutomationFitness.
    Schedules tasks to fill up to 8 hours (480 min), avoiding back-to-back repeats.
    """

    genome = Genome()  # Handles DNA <-> RNA <-> protein translation
    auto_fitness = AutomationFitness(amino_task_map=amino_task_map)

    # ------------------------------
    # 1. Create initial population
    # ------------------------------
    population = [genome.generate_ssDNA(length=9) for _ in range(pop_size)]

    # ------------------------------
    # 2. Fitness wrapper
    # ------------------------------
    def fitness_wrapper(dna):
        rna_seq = genome.dna_to_rna(dna)
        protein_seq = genome.protein(rna_seq)
        return auto_fitness.protein_fitness(protein_seq)

    # ------------------------------
    # 3. Run GA
    # ------------------------------
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,
        length=9,
        population_size=pop_size,
        iterations=generations,
        normalized=False,
        verbose=verbose
    )

    # ------------------------------
    # 4. Decode best DNA
    # ------------------------------
    rna_seq = genome.dna_to_rna(result["dna"])
    protein_seq = genome.protein(rna_seq)
    tasks_list = auto_fitness.protein_to_tasks(protein_seq)

    # ------------------------------
    # 5. Filter tasks to 8-hour max and compute cumulative points
    # ------------------------------
    max_minutes = 480.0
    cum_time = 0.0
    cum_points = 0.0
    filtered_tasks = []
    for task, pts, duration in tasks_list:
        if cum_time + duration > max_minutes:
            break
        filtered_tasks.append((task, pts, duration))
        cum_time += duration
        cum_points += pts  # cumulative points

    final_score = auto_fitness.protein_fitness(protein_seq)

    # ------------------------------
    # 6. Print human-readable schedule
    # ------------------------------
    if verbose:
        print("\n--- Automation GA Result ---")
        print(f"Translated protein: {protein_seq}")
        total_aa = len(protein_seq.replace("*", ""))
        print(f"\nTotal amino acids in translated protein: {total_aa}")
        if filtered_tasks:
            print("\nTask Schedule:")
            print(f"{'Idx':<4} {'Task':<25} {'Pts':<5} {'Time(min)':<10} {'Cum.Time(min)':<12} {'Cum.Pts':<8}")
            print("-" * 75)
            cum_time_running = 0.0
            cum_points_running = 0.0
            for i, (task, pts, duration) in enumerate(filtered_tasks, start=1):
                cum_time_running += duration
                cum_points_running += pts
                print(f"{i:<4} {task:<25} {pts:<5} {duration:<10.1f} {cum_time_running:<12.1f} {cum_points_running:<8.1f}")
            print(f"\nTotal points: {cum_points_running}")
            print(f"Final cumulative time (minutes): {cum_time_running}")
        else:
            print("Task list: (none)")

        print(f"\nAutomation fitness: {final_score:.3f}")

    # ------------------------------
    # 7. Return results
    # ------------------------------
    return {
        "protein_seq": protein_seq,
        "tasks_list": filtered_tasks,
        "fitness_score": final_score
    }


# Run as script with default target DNA
if __name__ == "__main__":
    target_caps = "TTTAACAACCTGGTATTACTCTCTCTTATATGCTAAAGTGTGCGACTCGAGGGTACTCGG"
    # target = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatcttgttttgcatgaaaattatgacgaacataataaagttattaaagatgagaaatggagattgaatgagtgttcttttcctcatgctttgtatgaatatatctttttaccatgtagaaagtgtgtaggatgtcgttcagataacgctaaaatgtggtctcttcgtgcatataatgagatgaaattacataaaaagaattgttttataactttgacttatgataatgcttcagatttggtcgtaaaagaccctctatgtattgctagtttaagatataaacattttcaaaattttatgaaaagattacgtaagaaaactggtaaaaaattaggttatcttgtatgtggtgagtatggtttaaaagatggtagagctcattggcatgcaatattatttgattttgattttgaagataaggagttaatctatgttaaaaaaggatataaacactattattcaacactacttcaagagtgttggtcgacgtatgacaaaaaaacagactcgtataatccgattggttttattgaccttgctgattgcgattatgactgttgtagttatgtttctcagtatgtgcttaaaaaattacctgttaatcagaatggcattgctgttggttcctatgttgatgatgtaactggtgaagttaaagatattgagttaactgatgtatgtccacctatggttaggagttctaaaaatcctgctataggttataattggtataagaaatttggagagaatgcatgtgaaaaaggttttatccctattgttacgaatgaaggtaagaaggttcgtaaagttcgtacgcctgcttattactattctaaatttgaagtagataatcctcaaaaatttgaaatattaaaaaatgttaaggaagaaaaaatgagaaaatattacaaggaaaatccaatagatttagataaattgaattcttggagtgaagctcatttatatagaattaaaaaacggatgaaagaggtattgacacattttaaaaaatagtttatattgcttgtataataatttaataatttagtttatttacttttatctatatgcctcaaatgtactcgtagcgagggatacagataatatatattatgtaagaaggaggaaaaaaacatgaacacaacaattattaaccaaacgggagaaaacaacgctacaaacgcaagctgtaaagctgattttagcttggtctttgctgtaaaggatttaaagtctgacaattttggttcccttttagtttgtaatacaagcgacgaggcgattagagctactaaggttagattgatgtatgaccaaggaagtatgatacaacaattccctgctgattttatgctttatcacgttggctattttaacacaaaaactggtgttatggaaagtgtcggaatagctattcctgttaagtcaattttagatgttagcttggaattagaacaagagcgaaaagtgaaagctgttgatattccagaatttatgaaaggagaggaaaatgacaatcgatgtgaagaatcaaattctagtgaatgtgttgaaagtattggataaacttatcgatttcattctagaagtattaaacaaagagaatgcataaatgattgatatttgtaaagattgtacattatacgtcttaaaaaaactaggtaggacaatgctttgtgcggagtcctatcttgcacttttaatttacatctttactcatgttagatttagtgtaactttttgcaagaaatttagtaaacttgtcgaccgatatcgagctagtgaaatatacagtacccctagcccgtccggcgatgaggacaaaataaggagaaacaatgaagataaaagttagatggtgtttaaatactgattttatttgtgataaggagaatgaagataatggctaaattttttacaccttatacaactacaaaaaaagttgttgttgaatttaaagagccaagtcttactgatcaatcttataaagatgagtgcgacttaggttttattattgaaaattatgtaagtaaaggaatacctttgccacaatctactatgaattatcaagactgtactactgtccaagattatcaatctgcaatgatgttagttgcagaagctaagtctaattttgaacaattaccttctaaggctagagatgaatttggaactgttgaaaattatcttgatttcatttctaaaccagagaatttaaaaacatcgtatgaaaaaggttatattgacccttctacagttgatttaatggacgtttatccagaaagataccaaacattatctgaacagatagaaactcctactgtagagcctgtggttaatccctctgaaactccttcaacagaggtgacggcataaagtaaatgcaaatagttctcttgttactatttgcatttactgacaccgttaggtggctaaagggtttgaaggttctaaaaccttcaataccccctaaaaaacagttaaaaagaaattaacccgaagggttgtatatattgaattagaaggagattttttatgtatgagatagatagaatgattgaaggttataaagagagacttaatgaaattatttatgatatcggacaatttcaatatcaattaacagaaaaacttaaagacaaacagaatttagaaaaatttattgaaagattagaaagaaaggatgataaaatatgtcaacagtaatggcacaacacggacatcaaatgcactcatttgaatattatccgtcagcacatatttcaagaagtaaatttaaccgttctcattcattgataacaacaatgaatgcaggttatattgttcctatttggcacgatttagcatatcctggcgatacacttattatgtcagctagaacattaacacgtttagctactcaattagtaccatttatgagtaatgtttatatggatatacatttctggtgtgttccacttcgtttagtatgggaacactggacagctatgaatggagaacaactaaatcctggagatagtacagattatttaactccgcaaataacagcaactccaacagtaggcgatatttatgattatttcaatgtacctataggtgttgaatctaagtttaatgcttttaactttagagcatataacttagtttataacgaatggtatcgagatgaaaacttacaagagagagtacctcaaatagtttcagataatgatacagaaagtaattatacacttttaaaacgtggtaagagaaaagattactttacaggagctttaccatggccacaaaaaggcagtgaagttgatttgcctttaggtatatctgcgccagtttctgtatatggtaatggtatgtctttaggattaacagatggttctatagaaatgggttcaattgtttatggtcaacaatattttgttcgtactgctgcatctggggttgatgttggcacagttgtaagcactgctggtagtactggaaataatgtagtcgttggtgtttctagtaatcctgagacctctggtcttattggtactgctgatttatcagatgctacatctgcaactattaactcattacgtcaagctttcgctattcaaaaaatgttagaaaaagatgctagaggtggtacaagatatatcgaaatgatactttcacatttcggtgttaaatctccagatgcaagattacaacgtccagagttcttaggtggtgctacatttgacttaaatctttctgttgttcctcaaacatcagctacaactgaaacttctacacctttaggtgatttggcttcttatggtgttatcaatggttcatcaaaacgtattgtacactcatttactgagcattgtgtagtatttggtgttgctagtattcgctctgaatattattatcaacaaggcttagaaagagattattcaaaacgttcaagaattgatttttatttgcctgttactgctcacttaggagaacaagctgtatataataaagaaatttatgcacaaggtacagacgaagatgaaaatgtatttggttatcaagaacgttggtctgaaatgagatataagaattcttatattactggtcaaacacgttctactgcaagtcaacctttagattattggcatttaggtcaagagtttgcaagcttgcctgctcttaacgctgagtttattcaagaaaaccctcctattgatagagttattgctcttcaagagtcagaaaatactcctcaatttatttgtaattttttctttgatgagtattgggtaagacctatgcctgtatattctactccaggtatgcaatcacacttttaagttatatcggtacgatagagtgagatttttaatctcgctctattgaaccgaaaggaaggataatattatggcagattggttaagttctttaatttctggtggttttaatatggctggtcaagctattaattataactatcaaaagaggttaatggaaaaacaatatgatttgaatataaaaggtttaaaggaaagtcctttagctattcgtacaggtttggagagtgcaggatataatcctataacttttgcaggtcaaactaacgctagtgctagtgtaggttctgctccttctgtatctgatagtaatttgggtactagtattgttaatgcttatcaacaaaacaaattaaatgaagctaatgttgatgcaacaaatgctcaagcagaattgtctaatgaacaagccaaaactgaacaagcgaaaagaactaatcttgagtttcaaaatcgtatgttagatgttgaaaaacatttaaaacaaaaagatttagatacttatgatagacgtttttatacacaactttatgaacaaatgcagagagcagaaaattatagagctatggcaaatttacaaggttataatgccgagtctcaacgtatagcttctaatgctcaaatgcttggttcacaagctagacaatcagacgctgttactaatagatatttagcaaagtatggtactcctcaacgtagttttttaactttgttaaataagcctaaaactaaaggaaaatattaattccatttttcagcagtttttacacctaaccaaaatataactattatacaaaataattcaaacataaggagattttacaatgaaaagaaaacaactgtcaaggaaagcaggtgctaagatgtttaaacgttctggtcaaatgatgaactctaaaaatcagcctaagatttctagaggtggtattagattttagtactcctatttaacacacatagtccaagaggagtttttactcctctttttttaagagaggaatgtatat".replace("\n", "")  # Example DNA
    # target_caps = target.upper()

    # run_bio_ga_evolution(target_caps)
    run_auto_ga_evolution()
