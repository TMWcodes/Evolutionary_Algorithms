import random
from lib.fitness_wrappers import dna_only_wrapper  # import your wrapper
from lib.bio_genome import Genome

# -----------------------------
# Weasel-style evolution runner
# -----------------------------

ALPHABET = ['A', 'C', 'G', 'T']
L = 78  # length of your DNA string
TARGET_STRING = "atgacatgttatagtcctattcctgcttgctttagtaaatcacaatatgctaagacaggaaagaaaaatatacatgac"
TARGET_STRING = TARGET_STRING.upper()
GENOME = Genome()
ENFORCE_START_STOP = True

# Create DNA-only fitness function
fitness = dna_only_wrapper(target_dna=TARGET_STRING, genome=GENOME, enforce_start_stop=ENFORCE_START_STOP)

def random_string():
    """Generate a random DNA string of length L."""
    return ''.join(random.choice(ALPHABET) for _ in range(L))

def mutate(s, mu):
    """Mutate string s with per-base mutation probability mu."""
    s_list = list(s)
    for i in range(L):
        if random.random() < mu:
            choices = [b for b in ALPHABET if b != s_list[i]]
            s_list[i] = random.choice(choices)
    return ''.join(s_list)

def weasel_run(target_dna, genome, L, mu=0.0128, offspring=100, max_gens=1000, verbose=False):
    """
    Weasel-style evolution: keeps best individual and mutates it each generation.

    Returns a history list compatible with GA comparisons.
    Each item in the list is a dict:
        - generation
        - gen_best
        - running_best
        - avg
        - best_string
    """
    # GA-compatible fitness function (DNA-only)
    fitness_func = dna_only_wrapper(target_dna, genome, enforce_start_stop=False)

    # Initial random string
    best = ''.join(random.choice(['A','C','G','T']) for _ in range(L))
    best_fit = fitness_func(best)
    best_string = best
    running_best = best_fit

    history = []

    for gen in range(1, max_gens + 1):
        # Generate offspring
        kids = []
        kids_fit = []
        for _ in range(offspring):
            s_list = list(best)
            for i in range(L):
                if random.random() < mu:
                    choices = [b for b in ['A','C','G','T'] if b != s_list[i]]
                    s_list[i] = random.choice(choices)
            kid = ''.join(s_list)
            kids.append(kid)
            kids_fit.append(fitness_func(kid))

        # Determine best of this generation
        gen_best_index = max(range(len(kids_fit)), key=lambda i: kids_fit[i])
        gen_best_fit = kids_fit[gen_best_index]
        gen_best_string = kids[gen_best_index]

        # Update running best if improved
        if gen_best_fit >= running_best:
            running_best = gen_best_fit
            best_string = gen_best_string

        # Average fitness
        avg_fit = sum(kids_fit) / len(kids_fit)

        # Append to history
        history.append({
            "generation": gen,
            "gen_best": gen_best_fit,
            "running_best": running_best,
            "avg": avg_fit,
            "best_string": best_string
        })

        if verbose and gen % 100 == 0:
            print(f"Gen {gen}: gen_best={gen_best_fit:.4f}, running_best={running_best:.4f}, avg={avg_fit:.4f}")

        # Stop if perfect match
        if best_string == target_dna:
            if verbose:
                print(f"Target reached at generation {gen}")
            break

    return history

# -----------------------------
# Example usage
# -----------------------------
# if __name__ == "__main__":
#     history = weasel_run(mu=0.0128, offspring=100, max_gens=1000, verbose=True)
#     final = history[-1]
#     print("Weasel run final result:")
#     print(f"Generation: {final['generation']}, Best fitness: {final['running_best']:.4f}")
#     print(f"Best string: {final['best_string']}")
