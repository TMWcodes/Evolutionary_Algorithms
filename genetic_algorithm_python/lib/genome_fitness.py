# bio_fitness_functions.py
def phenotype_fitness(dna, target_protein, genome):
    """DNA -> RNA -> Protein, then compare to target protein."""
    rna = genome.dna_to_rna(dna)
    protein = genome.protein(rna)
    return sum(a == b for a, b in zip(protein, target_protein)) / max(len(target_protein), 1)


# genome_fitness.py (partial)
def dna_fitness(candidate, target_dna, genome, critical_sites=None, environment=None):
    """Evaluate DNA with optional critical residues and environment-aware penalties."""
    length_penalty = abs(len(candidate) - len(target_dna)) / len(target_dna)
    start_penalty = 0 if candidate.startswith("ATG") else 0.1
    stop_codons = {"TAA", "TAG", "TGA"}
    stop_penalty = 0 if candidate[-3:] in stop_codons else 0.1

    # Sequence match
    match_score = sum(a==b for a,b in zip(candidate, target_dna)) / len(target_dna)

    # Protein match
    target_protein = genome.protein(genome.dna_to_rna(target_dna))
    candidate_protein = genome.protein(genome.dna_to_rna(candidate))
    pheno_score = 0.0

    # Critical residues weighting
    for i, (c, t) in enumerate(zip(candidate_protein, target_protein)):
        weight = 2.0 if critical_sites and i in critical_sites else 1.0
        pheno_score += weight * (c==t)
    max_score = sum([2.0 if critical_sites and i in critical_sites else 1.0 for i in range(len(target_protein))])
    pheno_score /= max_score if max_score>0 else 1

    fitness = 0.5 * match_score + 0.5 * pheno_score
    fitness -= (length_penalty + start_penalty + stop_penalty)

    # Environment penalties
    if environment:
        if environment.get("require_stop", False) and candidate[-3:] not in stop_codons:
            fitness *= 0.5  # harsh penalty

    return max(0.01, fitness)
