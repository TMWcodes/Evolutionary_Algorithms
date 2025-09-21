from collections import Counter

def print_run_specs(pop_size, generations, p_c, p_m, p_recomb, p_transp, p_locdup,
                    use_frames, check_complement, normalized, final_score, protein_seq):
    print("\n--- GA Run Specs ---")
    print(f"Population size: {pop_size}, Generations: {generations}")
    print(f"p_c={p_c}, p_m={p_m}, p_recomb={p_recomb}, p_transp={p_transp}, p_locdup={p_locdup}")
    print(f"use_frames={use_frames}, check_complement={check_complement}, normalized={normalized}")
    print(f"\nBest after {generations} generations: fitness={final_score:.3f}")
    print(f"Translated protein: {protein_seq}")
    print(f"Total amino acids in translated protein: {len(protein_seq)}\n")


def print_task_schedule(filtered_tasks):
    if not filtered_tasks:
        print("Task list: (none)")
        return

    print("Task Schedule:")
    print(f"{'Idx':<4} {'Task':<25} {'Pts':<5} {'Time(min)':<10} {'Cum.Time(min)':<12} {'Cum.Pts':<8}")
    print("-" * 75)

    cum_time, cum_pts = 0.0, 0.0
    task_names = []

    for i, (task, pts, duration) in enumerate(filtered_tasks, start=1):
        cum_time += duration
        cum_pts += pts
        task_names.append(task)
        print(f"{i:<4} {task:<25} {pts:<5} {duration:<10.1f} {cum_time:<12.1f} {cum_pts:<8.1f}")

    print(f"\nTotal points: {cum_pts}")
    print(f"Final cumulative time (hrs): {cum_time/60:.2f}")

    task_counter = Counter(task_names)
    num_unique_tasks = len(task_counter)
    most_common_task, most_common_count = task_counter.most_common(1)[0]
    print(f"Number of unique tasks: {num_unique_tasks}")
    print(f"Most duplicated task: '{most_common_task}' appears {most_common_count} times")
