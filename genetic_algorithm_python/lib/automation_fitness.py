from typing import List, Dict, Tuple, Optional

# Default amino acid → task map
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
    "*": ("End Marker", 0, 0),
}

class AutomationFitness:
    """
    Converts protein sequences → task schedule.
    Fitness encourages:
      - Max points within 8 hours
      - Diversity (no back-to-back repeats)
      - Filling the schedule (time utilization)
    """

    def __init__(self, amino_task_map: Optional[Dict[str, Tuple[str, float, float]]] = None,
                 max_minutes: float = 480.0):
        self.amino_task_map = amino_task_map or AMINO_TASK_MAP
        self.max_minutes = max_minutes

    def protein_to_tasks(self, protein: str) -> List[Tuple[str, float, float]]:
        """Translate protein sequence → list of tasks, ignoring internal stops"""
        tasks = []
        for aa in protein:
            if aa == "*" or aa not in self.amino_task_map:
                continue
            tasks.append(self.amino_task_map[aa])
        return tasks

    def protein_fitness(self, protein: str) -> float:
        """Compute fitness combining efficiency, diversity, and time utilization"""
        tasks = self.protein_to_tasks(protein)
        if not tasks:
            return 0.01

        scheduled = []
        total_points = 0.0
        total_time = 0.0
        last_task = None
        unique_tasks = set()

        # Sort tasks by points per minute for greedy efficiency
        tasks_sorted = sorted(tasks, key=lambda t: t[1]/t[2], reverse=True)

        for name, points, duration in tasks_sorted:
            if total_time >= self.max_minutes:
                break
            if name == last_task:
                continue  # skip back-to-back repeats
            if total_time + duration > self.max_minutes:
                continue
            scheduled.append((name, points, duration))
            total_points += points
            total_time += duration
            last_task = name
            unique_tasks.add(name)

        if total_time == 0:
            return 0.01

        # Efficiency = points per minute
        efficiency = total_points / total_time

        # Time utilization = reward schedules closer to 8 hours
        time_utilization = total_time / self.max_minutes

        # Diversity = fraction of unique tasks
        diversity = len(unique_tasks) / len(scheduled) if scheduled else 1.0

        # Normalize by best single-task efficiency
        best_efficiency = max(p / t for (_, p, t) in self.amino_task_map.values() if t > 0)

        # Combine all factors
        normalized_score = (efficiency * diversity * time_utilization) / best_efficiency

        return min(max(normalized_score, 0.01), 1.0)

    def schedule_protein(self, protein: str) -> List[Tuple[str, float, float, float, float]]:
        """
        Return scheduled tasks with cumulative points and cumulative time
        Each task is (name, points, duration, cum_points, cum_time)
        """
        tasks = self.protein_to_tasks(protein)
        scheduled = []
        total_time = 0.0
        total_points = 0.0
        last_task = None

        # Sort by points per minute
        tasks_sorted = sorted(tasks, key=lambda t: t[1]/t[2], reverse=True)

        for name, points, duration in tasks_sorted:
            if total_time >= self.max_minutes:
                break
            if name == last_task:
                continue
            if total_time + duration > self.max_minutes:
                continue
            total_time += duration
            total_points += points
            scheduled.append((name, points, duration, total_points, total_time))
            last_task = name

        return scheduled
