import pytest
from lib import automation_fitness as af

def test_knapsack_file_output():
    """Test the greedy knapsack schedule from your knapsack file."""

    # ------------------------
    # 1️⃣ Define tasks and capacity
    # ------------------------
    AMINO_TASK_MAP = {
        "M": ("Model Training", 30, 25),
        "F": ("Database Migration", 25, 20),
        "L": ("Deploy Script", 18, 15),
        "I": ("Code Linting", 4, 10),
        "V": ("System Audit", 16, 20),
        "S": ("Web Scraping", 12, 15),
        "P": ("User Report Gen", 14, 15),
        "T": ("DB Sync", 20, 25),
        "A": ("Log Analysis", 9, 10),
        "Y": ("Data Normalization", 11, 15),
        "H": ("API Health Check", 8, 10),
        "Q": ("Quick Health Check", 3, 10),
        "N": ("Unit Test Run", 10, 15),
        "K": ("Email Parsing", 6, 10),
        "D": ("Data Cleanup", 10, 15),
        "E": ("Email Summary", 5, 10),
        "C": ("Cache Clean", 6, 10),
        "W": ("Backup Verification", 9, 15),
        "R": ("Report Generation", 15, 20),
        "G": ("Data Aggregation", 12, 15),
    }
    capacity = 480

    # ------------------------
    # 2️⃣ Build greedy knapsack schedule
    # ------------------------
    tasks_sorted = sorted(
        [(k, v) for k, v in AMINO_TASK_MAP.items() if v[2] > 0],
        key=lambda t: t[1][1]/t[1][2],
        reverse=True
    )

    total_time = 0
    total_points = 0
    schedule = []

    while total_time < capacity:
        for code, (name, pts, t) in tasks_sorted:
            if total_time + t <= capacity:
                schedule.append((code, name, pts, t))
                total_time += t
                total_points += pts
            if total_time >= capacity:
                break

    task_string = ''.join([s[0] for s in schedule])

    # ------------------------
    # 3️⃣ Test through AutomationFitness
    # ------------------------
    auto_fit = af.AutomationFitness(amino_task_map=AMINO_TASK_MAP)
    fitness_score = auto_fit.protein_fitness(task_string)

    print("\nGreedy Knapsack Test Output")
    print("---------------------------")
    print("Task string:", task_string)
    print("Total points:", total_points)
    print("Total time (min):", total_time)
    print("Fitness score:", fitness_score)

    # ------------------------
    # 4️⃣ Assertions
    # ------------------------
    assert total_time <= capacity, "Knapsack schedule exceeds capacity"
    assert total_points > 0, "Total points should be positive"
    assert 0.0 <= fitness_score <= 1.0, "Fitness score should be within 0-1 range"