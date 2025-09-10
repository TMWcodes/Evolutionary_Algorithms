import random

class GeneticAlgorithm:
    def generate(self, length, population_size=10):
        return [''.join(random.choice('01') for _ in range(length)) for _ in range(population_size)]

    def map_population_fit(self, population, fitness):
        return [{"chromosome": c, "fitness": fitness(c)} for c in population]

    def roulette_wheel_selection(self, population, fitness_values, num_selections):
        total_fitness = sum(fitness_values)
        probabilities = [f / total_fitness for f in fitness_values]

        cumulative = []
        cumsum = 0
        for p in probabilities:
            cumsum += p
            cumulative.append(cumsum)

        selected = []
        for _ in range(num_selections):
            r = random.random()
            for i, prob in enumerate(cumulative):
                if r <= prob:
                    selected.append(population[i])
                    break
        return selected

    def mutate(self, chromosome, p_m):
        if any(c.isalpha() for c in chromosome):
            raise ValueError("invalid nucleotide")

        return ''.join(
            '1' if c == '0' and random.random() < p_m else
            '0' if c == '1' and random.random() < p_m else c
            for c in chromosome
        )

    def crossover(self, pair, index=4, p_c=0.7):
        if len(pair) != 2 or None in pair:
            raise ValueError("Both chromosomes in the pair must be non-nil.")

        c1, c2 = pair
        if random.random() > p_c:
            return [c1, c2]  # No crossover
        return [c1[:index] + c2[index:], c2[:index] + c1[index:]]

    def run(self, length, p_c=0.7, p_m=0.01, iterations=100):
        print("----STARTING POPULATION---")
        population = self.generate(length)

        ideal = '10101010'[:length]

        def fitness(chrom):
            return sum(1 for a, b in zip(chrom, ideal) if a == b) / len(ideal)

        for generation in range(iterations):
            fitness_data = self.map_population_fit(population, fitness)
            fitness_values = [d['fitness'] for d in fitness_data]

            selected = self.roulette_wheel_selection(population, fitness_values, len(population))

            pairs = [selected[i:i+2] for i in range(0, len(selected), 2)]

            new_population = []
            for pair in pairs:
                if len(pair) == 2:
                    new_population.extend(self.crossover(pair, index=4, p_c=p_c))
                else:
                    new_population.extend(pair)  # handle odd population

            mutated_population = [self.mutate(ch, p_m=p_m) for ch in new_population]
            population = mutated_population

            best = max(self.map_population_fit(population, fitness), key=lambda x: x['fitness'])

            if best['chromosome'] == ideal:
                print(f"Perfect match at generation {generation}: {best['chromosome']}")
                return best['chromosome']

        print(f"Best result after {iterations} iterations: {best['chromosome']} (Fitness: {best['fitness']})")
        return best['chromosome']

gene = GeneticAlgorithm()
result = gene.run(length=8, p_c=0.8, p_m=0.02, iterations=200)