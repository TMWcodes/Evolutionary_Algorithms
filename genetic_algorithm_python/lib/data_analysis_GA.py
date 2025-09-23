# data_analysis_GA.py

import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to the JSON data file
DATA_FILE = "bio_ga_data.json"

def load_ga_data(file_path=DATA_FILE):
    """Load BioGA JSON data."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def plot_run_history(run_key, run_data):
    """Plot the GA evolution history for a single run."""
    history = run_data.get("history", [])
    if not history:
        print(f"No history found for {run_key}.")
        return
    
    df = pd.DataFrame(history)
    # Make sure generation column exists
    df["generation"] = df.get("gen", df.get("generation"))
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["generation"], df["gen_best"], label="Gen Best", marker="o")
    plt.plot(df["generation"], df["running_best"], label="Running Best", marker="x")
    plt.plot(df["generation"], df["avg"], label="Average", linestyle="--")
    plt.title(f"{run_key} Evolution")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_running_best_comparison(run_histories, labels=None):
    """
    Compare running_best across multiple GA runs.
    
    Parameters:
        run_histories: list of lists of dicts (each run's history)
        labels: optional list of labels for each run
    """
    plt.figure(figsize=(10, 6))

    for i, history in enumerate(run_histories):
        df = pd.DataFrame(history)
        df["generation"] = df.get("generation", df.get("gen"))
        label = labels[i] if labels else f"Run {i+1}"
        plt.plot(df["generation"], df["running_best"], label=label, marker="o")
    
    plt.xlabel("Generation")
    plt.ylabel("Running Best Fitness")
    plt.title("GA Running Best Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

def summarize_run(run_key, run_data):
    """Return a dict of summary metrics for a run, including GA specs."""
    
    # Build a shorthand label for GA run specs
    specs = (
        f"pop{run_data.get('pop_size', '?')}_"
        f"gen{run_data.get('generations', '?')}_"
        f"pc{run_data.get('p_c', 0)}_"
        f"pm{run_data.get('p_m', 0)}_"
        f"re{run_data.get('p_recomb', 0)}_"
        f"tr{run_data.get('p_transp', 0)}_"
        f"ld{run_data.get('p_locdup', 0)}_"
        f"F{'T' if run_data.get('use_frames', False) else 'F'}_"
        f"C{'T' if run_data.get('check_complement', False) else 'F'}_"
        f"N{'T' if run_data.get('normalized', False) else 'F'}"
    )

    summary = {
        "run": run_key,
        "dna_fitness": run_data.get("dna_fitness"),
        "protein_fitness": run_data.get("protein_fitness"),
        "combined_fitness": run_data.get("combined_fitness"),
        "first_best_gen": run_data.get("first_best_gen"),
        "specs": specs  # new column for GA parameters
    }
    return summary


def main():
    data = load_ga_data()
    summaries = []
    run_histories = []
    labels = []


    for run_key, run_data in data.items():
        print(f"\n--- Plotting {run_key} ---")
        # plot_run_history(run_key, run_data)
        history = run_data.get("history", [])
        if history:
            run_histories.append(history)
            labels.append(run_key)

        summary = summarize_run(run_key, run_data)
        summaries.append(summary)

        # Compare running_best across runs
    if run_histories:
        plot_running_best_comparison(run_histories, labels)

    # Summary table
    df_summary = pd.DataFrame(summaries)
    print("\n=== GA Runs Summary ===")
    print(df_summary)
    # Optionally save summary table
    df_summary.to_csv("bio_ga_summary.csv", index=False)
    print("\nSummary saved to 'bio_ga_summary.csv'")



if __name__ == "__main__":
    main()
