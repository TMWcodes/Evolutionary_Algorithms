# run_bio_ga.py
from lib.bio_genome import Genome
from lib import genome_fitness as gf

def run_evolution(target_dna, generations=200, pop_size=20):
    genome = Genome()
    target_protein = genome.protein(genome.dna_to_rna(target_dna))

    def fitness_wrapper(dna):
        dna_score, protein_score, combined = gf.dna_fitness(dna, target_dna, genome)
        return combined  # GA only uses combined for selection

    # run GA
    result = genome.run_evolution(
        fitness_func=fitness_wrapper,
        length=len(target_dna),
        population_size=pop_size,
        iterations=generations,
        normalized=False,
        verbose=True
    )

    # recompute all scores for the best sequence
    dna_score, protein_score, combined = gf.dna_fitness(result["dna"], target_dna, genome)
    best_protein = genome.protein(genome.dna_to_rna(result["dna"]))

    print("\n--- GA Result ---")
    print(f"Target DNA sequence:   {target_dna}")
    print(f"Best DNA sequence:     {result['dna']}\n")
    print(f"Target protein:        {target_protein}")
    print(f"Best protein:          {best_protein}\n")
    print(f"DNA fitness:           {dna_score:.3f}")
    print(f"Protein fitness:       {protein_score:.3f}")
    print(f"Combined fitness:      {combined:.3f}")


if __name__ == "__main__":
    target = "ATGTTTAAAGGG"
    run_evolution(target)

