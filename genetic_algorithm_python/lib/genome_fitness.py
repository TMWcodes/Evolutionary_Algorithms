# bio_fitness_functions.py
def phenotype_fitness(dna, target_protein, genome):
    """DNA -> RNA -> Protein, then compare to target protein."""
    if not target_protein:  # guard against empty target
        return 0.0

    rna = genome.dna_to_rna(dna)
    protein = genome.protein(rna)
    return sum(a == b for a, b in zip(protein, target_protein)) / len(target_protein)


# genome_fitness.py
def dna_fitness(candidate, target_dna, genome, critical_sites=None, environment=None):
    """
    Evaluate DNA with optional critical residues and environment-aware penalties.
    Returns tuple: (dna_score, protein_score, combined_fitness)
    """

    if not target_dna:
        return (0.0, 0.0, 0.01)

    # --- DNA match score ---
    dna_score = sum(a == b for a, b in zip(candidate, target_dna)) / len(target_dna)

    # --- Protein match score ---
    target_protein = genome.protein(genome.dna_to_rna(target_dna))
    candidate_protein = genome.protein(genome.dna_to_rna(candidate))

    pheno_score = 0.0
    for i, (c, t) in enumerate(zip(candidate_protein, target_protein)):
        weight = 2.0 if critical_sites and i in critical_sites else 1.0
        pheno_score += weight * (c == t)

    max_score = sum(
        2.0 if critical_sites and i in critical_sites else 1.0
        for i in range(len(target_protein))
    )
    protein_score = pheno_score / max_score if max_score > 0 else 0.0

    # --- penalties ---
    length_penalty = abs(len(candidate) - len(target_dna)) / len(target_dna)
    start_penalty = 0 if candidate.startswith("ATG") else 0.1
    stop_codons = {"TAA", "TAG", "TGA"}
    stop_penalty = 0 if candidate[-3:] in stop_codons else 0.1

    combined = 0.5 * dna_score + 0.5 * protein_score
    combined -= (length_penalty + start_penalty + stop_penalty)

    # Environment penalties
    if environment:
        if environment.get("require_stop", False) and candidate[-3:] not in stop_codons:
            combined *= 0.5  # harsh penalty

    return (dna_score, protein_score, max(0.01, combined))
