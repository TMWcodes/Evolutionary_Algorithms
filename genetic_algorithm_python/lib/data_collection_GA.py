import json
import os
from datetime import datetime
from lib.run_bio_ga import run_bio_ga_evolution  # your GA function

def collect_bio_ga_data(target_dna, generations=100, pop_size=1000, filename="bio_ga_data.json"):
    target_dna = target_dna.upper()

    # Run GA
    result = run_bio_ga_evolution(target_dna, generations=generations, pop_size=pop_size)

    # Prepare run data including GA specs
    run_data = {
        "timestamp": datetime.now().isoformat(),
        "target_dna": target_dna,
        "dna": result["dna"],
        "protein_seq": result["protein_seq"],
        "dna_fitness": result["dna_fitness"],
        "protein_fitness": result["protein_fitness"],
        "combined_fitness": result["combined_fitness"],
        "first_best_gen": result["first_best_gen"],
        "history": result["history"],
        # GA run specs
        "pop_size": result.get("pop_size", pop_size),
        "generations": result.get("generations", generations),
        "p_c": result.get("p_c", 0),
        "p_m": result.get("p_m", 0),
        "p_recomb": result.get("p_recomb", 0),
        "p_transp": result.get("p_transp", 0),
        "p_locdup": result.get("p_locdup", 0),
        "use_frames": result.get("use_frames", True),
        "check_complement": result.get("check_complement", True),
        "normalized": result.get("normalized", True)
    }

    # Load existing JSON if it exists
    try:
        with open(filename, "r") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        all_data = {}

    # Determine next run number
    next_run = f"run_{len(all_data) + 1}"
    all_data[next_run] = run_data

    # Save back to JSON
    with open(filename, "w") as f:
        json.dump(all_data, f, indent=4)

    print(f"BioGA run data saved as '{next_run}' in '{filename}'")
    return run_data
# Example usage:
if __name__ == "__main__":
    # target = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatcttgttttgcatgaaaattatgacgaacataataaagttattaaagatgagaaatggagattgaatgagtgttcttttcctcatgctttgtatgaatatatctttttaccatgtagaaagtgtgtaggatgtcgttcagataacgctaaaatgtggtctcttcgtgcatataatgagatgaaattacataaaaagaattgttttataactttgacttatgataatgcttcagatttggtcgtaaaagaccctctatgtattgctagtttaagatataaacattttcaaaattttatgaaaagattacgtaagaaaactggtaaaaaattaggttatcttgtatgtggtgagtatggtttaaaagatggtagagctcattggcatgcaatattatttgattttgattttgaagataaggagttaatctatgttaaaaaaggatataaacactattattcaacactacttcaagagtgttggtcgacgtatgacaaaaaaacagactcgtataatccgattggttttattgaccttgctgattgcgattatgactgttgtagttatgtttctcagtatgtgcttaaaaaattacctgttaatcagaatggcattgctgttggttcctatgttgatgatgtaactggtgaagttaaagatattgagttaactgatgtatgtccacctatggttaggagttctaaaaatcctgctataggttataattggtataagaaatttggagagaatgcatgtgaaaaaggttttatccctattgttacgaatgaaggtaagaaggttcgtaaagttcgtacgcctgcttattactattctaaatttgaagtagataatcctcaaaaatttgaaatattaaaaaatgttaaggaagaaaaaatgagaaaatattacaaggaaaatccaatagatttagataaattgaattcttggagtgaagctcatttatatagaattaaaaaacggatgaaagaggtattgacacattttaaaaaatagtttatat"  # your target DNA sequence
    target = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatgac"
    collect_bio_ga_data(target)
