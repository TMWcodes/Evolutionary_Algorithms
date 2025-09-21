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

def greedy_knapsack(amino_task_map, capacity):
    # Sort tasks by points/time
    tasks_sorted = sorted(
        [(k, v) for k, v in amino_task_map.items() if v[2] > 0],
        key=lambda t: t[1][1]/t[1][2],
        reverse=True
    )

    total_time = 0
    total_points = 0
    schedule = []

    # Fill schedule greedily
    while True:
        added = False
        for code, (name, pts, t) in tasks_sorted:
            if total_time + t <= capacity:
                schedule.append((code, name, pts, t))
                total_time += t
                total_points += pts
                added = True
        if not added:
            break  # Stop if no task fits

    return schedule, total_points, total_time

schedule, points, time_used = greedy_knapsack(AMINO_TASK_MAP, 240)  # 4 hours

# Create task string
task_string = ''.join([s[0] for s in schedule])

# Print results
print("Schedule:")
for idx, (code, name, pts, t) in enumerate(schedule, start=1):
    print(f"{idx:2d} | {name:20s} | {pts:3d} | {t:3d}")

auto_fit = af.AutomationFitness(amino_task_map=AMINO_TASK_MAP)
fitness_score = auto_fit.protein_fitness(task_string)

print("Greedy knapsack task string:", task_string)
print("Total points:", points)
print("Time used:", time_used)
print("Fitness score through AutomationFitness:", fitness_score)