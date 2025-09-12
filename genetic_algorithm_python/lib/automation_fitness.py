from typing import List, Dict, Tuple, Optional

# ------------------------------
# Example AMINO ACID → TASK MAP
# ------------------------------
AMINO_TASK_MAP = {
    "M": ("Model Training", 30, 5.0),
    "F": ("Database Migration", 25, 3.0),
    "L": ("Deploy Script", 18, 1.5),
    "I": ("Code Linting", 4, 0.25),
    "V": ("System Audit", 16, 2.0),
    "S": ("Web Scraping", 12, 1.0),
    "P": ("User Report Gen", 14, 1.5),
    "T": ("DB Sync", 20, 3.0),
    "A": ("Log Analysis", 9, 0.75),
    "Y": ("Data Normalization", 11, 1.0),
    "H": ("API Health Check", 8, 0.5),
    "Q": ("Quick Health Check", 3, 0.1),
    "N": ("Unit Test Run", 10, 0.75),
    "K": ("Email Parsing", 6, 0.5),
    "D": ("Data Cleanup", 10, 1.5),
    "E": ("Email Summary", 5, 0.25),
    "C": ("Cache Clean", 6, 0.5),
    "W": ("Backup Verification", 9, 0.5),
    "R": ("Report Generation", 15, 2.0),
    "G": ("Data Aggregation", 12, 1.0),
    "*": ("End Marker", 0, 0),
}


# ------------------------------
# AutomationFitness Class
# ------------------------------
class AutomationFitness:
    """
    Provides GA-friendly fitness for automation tasks:
      - Interprets protein sequences as tasks
      - Computes normalized fitness score
    """

    START_AA = "M"
    STOP_AA = "*"

    def __init__(self, amino_task_map: Optional[Dict[str, Tuple[str, float, float]]] = None):
        self.amino_task_map = amino_task_map or AMINO_TASK_MAP

    def protein_to_tasks(self, protein: str) -> List[Tuple[str, float, float]]:
        """
        Convert a protein sequence to a list of tasks.
        Only valid if the sequence starts with START_AA (M).
        Stops at STOP_AA (*).
        """
        tasks = []
        if not protein or protein[0] != self.START_AA:
            return tasks
        for aa in protein:
            if aa == self.STOP_AA:
                break
            if aa in self.amino_task_map:
                tasks.append(self.amino_task_map[aa])
        return tasks

    def protein_fitness(self, protein: str, max_hours: float = 8.0) -> float:
        """
        Compute normalized fitness [0.01,1.0] based on protein-derived tasks.
        """
        tasks = self.protein_to_tasks(protein)
        total_points = sum(t[1] for t in tasks)
        total_time = sum(t[2] for t in tasks)
        if total_time == 0:
            return 0.01
        fitness = total_points / total_time
        if total_time > max_hours:
            fitness *= 0.5
        return min(max(fitness / 10.0, 0.01), 1.0)
