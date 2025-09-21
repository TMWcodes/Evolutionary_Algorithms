from typing import List, Dict, Tuple, Optional
from collections import Counter
import math

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
        self.min_fitness = 0.01  # Minimum fitness score (1% of max)
        self.max_fitness = 1.0   # Maximum possible fitness score


    def protein_to_tasks(self, protein: str) -> List[Tuple[str, float, float]]:
        """Translate protein sequence → list of tasks, ignoring internal stops"""
        tasks = []
        for aa in protein:
            if aa == "*" or aa not in self.amino_task_map:
                continue
            tasks.append(self.amino_task_map[aa])
        return tasks

    def protein_fitness(self, protein: str) -> float:
        """
        Compute fitness for a protein sequence.
        Encourages:
        - High points/hour
        - Diversity (no back-to-back repeats)
        - Time utilization (close to 8 hrs)
        Penalizes:
        - Back-to-back repeats
        - Overflow beyond 8 hours
        """
        tasks = self.protein_to_tasks(protein)
        if not tasks:
            return 0.01

        total_points = 0.0
        total_time = 0.0
        last_task = None
        unique_tasks = set()
        task_counts = {}

        for name, points, duration in tasks:
            remaining_time = max(self.max_minutes - total_time, 0)
            if remaining_time <= 0:
                break

            task_time = min(duration, remaining_time)
            # Back-to-back penalty
         
              # Add diminishing returns
            task_counts[name] = task_counts.get(name, 0) + 1
            count = task_counts[name]
            diminishing_factor = 0.85 ** (count - 1)

            if name == last_task:
                task_points = points * diminishing_factor * 0.5 * (task_time / duration)
            else:
                task_points = points * diminishing_factor * (task_time / duration)

            total_points += task_points
            total_time += task_time
            last_task = name
            unique_tasks.add(name)

        if total_time == 0:
            return self.min_fitness

        # Keep your efficiency calculation
        efficiency = total_points / total_time

        # CHANGED: Less harsh time utilization (was killing scores)
        time_utilization = min(total_time / self.max_minutes, 1.0)
        time_factor = 0.6 + 0.4 * time_utilization  # Range: 0.6 to 1.0 instead of 0 to 1.0

        # CHANGED: Better diversity calculation
        diversity = 0.7 + 0.3 * (len(unique_tasks) / 20)  # Range: 0.7 to 1.0

        # Keep multiplicative but less harsh
        raw_score = efficiency * time_factor * diversity

         # ADD LENGTH PENALTY - penalize long sequences
        protein_length = len(protein)
        length_penalty = 0.0
        if protein_length > 100:
            # 0.1% penalty per amino acid over 100
            # 447 amino acids would get ~3.5% penalty
            length_penalty = (protein_length - 100) * 0.001

        # Apply length penalty to raw score
        constrained_score = raw_score * (1.0 - length_penalty)

        # CHANGED: Normalize by smaller factor to get better score ranges
        best_efficiency = max(p / t for (_, p, t) in self.amino_task_map.values() if t > 0)
        # Divide by best_efficiency * 0.7 to allow scores above theoretical efficiency
        normalized = constrained_score / (best_efficiency * 0.7)


        return min(max(normalized, self.min_fitness), 1.0)
       


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
        # tasks_sorted = sorted(tasks, key=lambda t: t[1]/t[2], reverse=True)

        for name, points, duration in tasks:
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
