from lib.bio_genome import Genome
import lib.genome_fitness as gf

def main():
    g = Genome()
    target_dna = "ATGTTTAAAGGG"
    
    def fitness(dna):
        return gf.dna_fitness(dna, target_dna, g)
    
    best = g.run_evolution(
        fitness_func=fitness,
        length=len(target_dna),
        population_size=50,
        iterations=200,
        p_m=0.1,
        p_c=0.7,
        verbose=True
    )
    print("Best sequence:", best["dna"])
    print("Fitness:", best["fitness"])

if __name__ == "__main__":
    main()