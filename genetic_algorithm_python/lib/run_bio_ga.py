# Import Genome class and fitness functions
from lib.bio_genome import Genome
import lib.genome_fitness as gf
from lib.automation_fitness import AutomationFitness  # your module
import random
# Wrapper function to run the GA on a target DNA
def run_bio_ga_evolution(target_dna, generations=200, pop_size=20):
    # Initialize genome object
    genome = Genome()

    # Compute target protein from target DNA for reporting
    target_protein = genome.protein(genome.dna_to_rna(target_dna))

    # Fitness wrapper for GA: only returns combined fitness (GA uses this for selection)
    def fitness_wrapper(dna):
        dna_score, protein_score, combined = gf.dna_fitness(dna, target_dna, genome)
        return combined  # GA selection uses combined fitness

    # Run the GA with the wrapper fitness function
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,    # Fitness function to evaluate sequences
        length=len(target_dna),          # Length of DNA sequences
        population_size=pop_size,        # Number of sequences per generation
        iterations=generations,          # Number of generations to evolve
        normalized=False,                # Whether to normalize fitness scores
        verbose=True                     # Print progress per generation
    )

    # After GA finishes, recompute all fitness scores for the best sequence
    dna_score, protein_score, combined = gf.dna_fitness(result["dna"], target_dna, genome)
    best_protein = genome.protein(genome.dna_to_rna(result["dna"]))

    # Print summary of GA results
    print("\n--- GA Result ---")
    print(f"Target DNA sequence:   {target_dna}")
    print(f"Best DNA sequence:     {result['dna']}\n")
    print(f"Target protein:        {target_protein}")
    print(f"Best protein:          {best_protein}\n")
    print(f"DNA fitness:           {dna_score:.3f}")
    print(f"Protein fitness:       {protein_score:.3f}")
    print(f"Combined fitness:      {combined:.3f}")

def run_auto_ga_evolution(amino_task_map=None, generations=200, pop_size=20):
    """
    Run the GA using AutomationFitness (protein-inspired task schedules)
    """
    genome = Genome()
    auto_fitness = AutomationFitness(amino_task_map=amino_task_map)

    # Decide DNA length (number of nucleotides, must be multiple of 3 for codons)
    dna_length = 30  

    bases = ['A', 'T', 'G', 'C']
    # Random initial DNA is not really used as "target"; GA evolves its own population
    target_dna = ''.join(random.choices(bases, k=dna_length))

    # GA wrapper: convert DNA → protein → compute fitness
    def fitness_wrapper(dna):
        rna = dna.replace("T", "U")
        protein_seq = ''.join(genome.aminoacid_dict.get(rna[i:i+3], '') 
                              for i in range(0, len(rna)-2, 3))
        return auto_fitness.protein_fitness(protein_seq)

    # Run GA
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,
        length=dna_length,
        population_size=pop_size,
        iterations=generations,
        normalized=False,
        verbose=True
    )

    # Compute final protein and task list for best sequence
    rna_seq = result["dna"].replace("T", "U")
    protein_seq = ''.join(genome.aminoacid_dict.get(rna_seq[i:i+3], '') 
                          for i in range(0, len(rna_seq)-2, 3))
    tasks_list = auto_fitness.protein_to_tasks(protein_seq)
    final_score = auto_fitness.protein_fitness(protein_seq)

    print("\n--- Automation GA Result ---")
    print(f"Best DNA sequence:     {result['dna']}")
    print(f"Translated RNA seq:    {rna_seq}")
    print(f"Translated protein:    {protein_seq}")
    print(f"Task list:             {tasks_list}")
    print(f"Automation fitness:    {final_score:.3f}")



# Run as script with default target DNA
if __name__ == "__main__":
 
    # run_bio_ga_evolution(target)
    run_auto_ga_evolution()
