| Component                    | Description                                                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `generate()`                 | Creates the initial random population of binary chromosomes.                                                           |
| `map_population_fit()`       | Applies a fitness function to each chromosome to evaluate how "fit" (good) it is.                                      |
| `roulette_wheel_selection()` | Selects chromosomes probabilistically based on their fitness scores. Higher fitness = higher chance of selection.      |
| `crossover()`                | Mixes two chromosomes to simulate reproduction (like cutting at a midpoint and swapping halves).                       |
| `mutate()`                   | Randomly flips bits with a small probability to introduce variation.                                                   |
| `run()`                      | Coordinates the entire process: generates, selects, reproduces, mutates, and evaluates the population over iterations. |
