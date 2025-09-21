def automation_fitness_wrapper(genome, auto_fitness):
    """Return a GA-compatible fitness function for AutomationFitness."""
    def wrapper(dna):
        rna_seq = genome.dna_to_rna(dna)
        protein_seq = genome.protein(rna_seq)
        return auto_fitness.protein_fitness(protein_seq)
    return wrapper

def dna_fitness_wrapper(target_dna, genome, enforce_start_stop=True):
    """Return a GA-compatible fitness function for dna_fitness."""
    from lib import genome_fitness as gf

    def wrapper(dna):
        # Pass the toggle down to dna_fitness
        dna_score, protein_score, combined = gf.dna_fitness(
            candidate=dna,
            target_dna=target_dna,
            genome=genome,
            enforce_start_stop=enforce_start_stop
        )

        # Penalize excessively long sequences
        length_penalty = min(1.0, len(target_dna)/len(dna)) if len(dna) > len(target_dna) else 1.0

        # Small bonus for repeated motifs
        repeat_bonus = 1.0 + 0.05 * (len(dna) - len(set(dna))) / len(dna)

        return combined * length_penalty * repeat_bonus

    return wrapper