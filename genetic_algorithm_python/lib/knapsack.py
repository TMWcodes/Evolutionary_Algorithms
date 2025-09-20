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

# Total time capacity in minutes (8 hours)
capacity = 240

# Prepare a list of tasks with points per minute
tasks = [(k, v[0], v[1], v[2], v[1]/v[2]) for k, v in AMINO_TASK_MAP.items()]

# Sort tasks by points per minute (descending)
tasks_sorted = sorted(tasks, key=lambda x: x[4], reverse=True)

# Generate schedule
total_time = 0
total_points = 0
schedule = []

while total_time < capacity:
    for code, name, pts, t, ppm in tasks_sorted:
        if total_time + t <= capacity:
            schedule.append((code, name, pts, t))
            total_time += t
            total_points += pts
        if total_time >= capacity:
            break

# Create task string
task_string = ''.join([s[0] for s in schedule])

# Print results
print("Total points:", total_points)
print("Total time (min):", total_time)
print("Task string:", task_string)
print("Schedule:")
for idx, (code, name, pts, t) in enumerate(schedule, start=1):
    print(f"{idx:2d} | {name:20s} | {pts:3d} | {t:3d}")