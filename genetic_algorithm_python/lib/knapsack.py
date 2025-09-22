import lib.automation_fitness as af

# Define the tasks: (Code, Name, Points, Time)
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

from lib import automation_fitness as af

def greedy_knapsack(amino_task_map, capacity):
    """
    Deterministic greedy knapsack solver.
    Selects tasks to maximize points within a time budget.

    Returns:
        schedule (list of tuples): (code, name, points, time)
        total_points (int)
        total_time (int)
    """
    # Sort tasks by points/time ratio
    tasks_sorted = sorted(
        [(k, v) for k, v in amino_task_map.items() if v[2] > 0],
        key=lambda t: t[1][1] / t[1][2],
        reverse=True
    )

    total_time = 0
    total_points = 0
    schedule = []

    while True:
        added = False
        for code, (name, pts, t) in tasks_sorted:
            if total_time + t <= capacity:
                schedule.append((code, name, pts, t))
                total_time += t
                total_points += pts
                added = True
        if not added:
            break  # stop if nothing fits

    return schedule, total_points, total_time


def run_greedy_knapsack(amino_task_map, capacity):
    schedule, points, time_used = greedy_knapsack(amino_task_map, capacity)
    task_string = ''.join([s[0] for s in schedule])

    from lib import automation_fitness as af
    auto_fit = af.AutomationFitness(amino_task_map=amino_task_map)
    fitness_score = auto_fit.protein_fitness(task_string)

    return {
        "schedule": schedule,
        "task_string": task_string,
        "total_points": points,
        "total_time": time_used,
        "capacity": capacity,
        "fitness_score": fitness_score,
    }

