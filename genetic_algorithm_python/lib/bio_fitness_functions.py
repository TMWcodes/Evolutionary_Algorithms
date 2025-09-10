# bio_fitness_functions.py
def phenotype_fitness(dna, target_protein, genome):
    """DNA -> RNA -> Protein, then compare to target protein"""
    rna = genome.dna_to_rna(dna)
    protein = genome.protein(rna)
    return sum(a == b for a, b in zip(protein, target_protein)) / max(len(target_protein), 1)

def phenotype_fitness(dna, target_protein, genome):
    """DNA -> RNA -> Protein, then compare to target protein."""
    rna = genome.dna_to_rna(dna)
    protein = genome.protein(rna)
    return sum(a == b for a, b in zip(protein, target_protein)) / max(len(target_protein), 1)


def dna_fitness(candidate, target_dna, genome):
    """Evaluate DNA with biological constraints, with a fitness floor."""
    length_penalty = abs(len(candidate) - len(target_dna)) / len(target_dna)

    # Penalize missing start codon
    start_penalty = 0 if candidate.startswith("ATG") else 0.1

    # Penalize missing stop codon
    stop_codons = {"TAA", "TAG", "TGA"}
    stop_penalty = 0 if candidate[-3:] in stop_codons else 0.1

    # Sequence match score
    match_score = sum(a == b for a, b in zip(candidate, target_dna)) / len(target_dna)

    # Phenotype (protein-level) match score
    target_protein = genome.protein(genome.dna_to_rna(target_dna))
    candidate_protein = genome.protein(genome.dna_to_rna(candidate))
    pheno_score = sum(a == b for a, b in zip(candidate_protein, target_protein)) / max(len(target_protein), 1)

    # Combine
    fitness = (0.5 * match_score + 0.5 * pheno_score)
    fitness -= (length_penalty + start_penalty + stop_penalty)

    return max(0.01, fitness)  # fitness floor