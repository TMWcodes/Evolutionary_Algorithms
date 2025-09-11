"""
automation_fitness.py

Fitness functions for automation / productivity optimization.

Two modes are supported:
1. Task-list based (AutomationFitness class)
   - Candidate is a list of task names.
   - Uses productivity points & time from a given dictionary.
2. DNA-based (codon translation)
   - Candidate is a DNA string.
   - Every codon (3 bases) maps to a script/task.
"""

import random

# ------------------------------
# MODE 1: Task-list based fitness
# ------------------------------

class AutomationFitness:
    def __init__(self, tasks):
        """
        tasks: dictionary of available scripts/tasks with productivity & time cost.
        Example:
        {
            "script1": {"points": 50, "time": 2},
            "script2": {"points": 30, "time": 1.5},
            ...
        }
        """
        self.tasks = tasks

    def points_per_hour(self, candidate):
        """
        Fitness = total productivity points / total hours.
        Encourages efficiency (maximizing points per unit time).
        """
        total_points, total_time = self._evaluate(candidate)
        if total_time == 0:
            return 0.01
        return total_points / total_time

    def weighted_balance(self, candidate, alpha=0.5):
        """
        Fitness = alpha * (normalized points) + (1-alpha) * (efficiency).
        Balances absolute productivity with efficiency.
        """
        total_points, total_time = self._evaluate(candidate)
        if total_time == 0:
            return 0.01

        max_points = max(v["points"] for v in self.tasks.values())
        max_eff = max(v["points"]/v["time"] for v in self.tasks.values())

        points_score = total_points / (max_points or 1)
        eff_score = (total_points / total_time) / (max_eff or 1)

        return alpha * points_score + (1 - alpha) * eff_score

    def deadline_penalty(self, candidate, deadline=8):
        """
        Fitness with penalty if total time exceeds deadline (e.g., 8 hrs/day).
        """
        total_points, total_time = self._evaluate(candidate)
        if total_time > deadline:
            penalty = (total_time - deadline) / deadline
            score = total_points * (1 - penalty)
        else:
            score = total_points
        return max(0.01, score)

    def _evaluate(self, candidate):
        """
        Utility: given a list of task names, return (total_points, total_time).
        Example candidate: ["script1", "script3"]
        """
        total_points, total_time = 0, 0
        for task in candidate:
            if task in self.tasks:
                total_points += self.tasks[task]["points"]
                total_time += self.tasks[task]["time"]
        return total_points, total_time


# ------------------------------
# MODE 2: DNA-based fitness
# ------------------------------

CODON_TASK_MAP = {
    # AAA - AAT
    "AAA": ("Data Cleanup", 10, 1.5),
    "AAC": ("File Backup", 7, 0.5),
    "AAG": ("Report Generation", 15, 2.0),
    "AAT": ("Email Summary", 5, 0.25),

    # ACA - ACT
    "ACA": ("Deploy Script", 18, 1.5),
    "ACC": ("Log Analysis", 9, 0.75),
    "ACG": ("Data Aggregation", 12, 1.0),
    "ACT": ("Cache Clean", 6, 0.5),

    # AGA - AGT
    "AGA": ("Database Migration", 25, 3.0),
    "AGC": ("API Health Check", 8, 0.5),
    "AGG": ("Code Linting", 4, 0.25),
    "AGT": ("Unit Test Run", 10, 0.75),

    # ATA - ATT
    "ATA": ("Web Scraping", 12, 1.0),
    "ATC": ("DB Sync", 20, 3.0),
    "ATG": ("Model Training", 30, 5.0),
    "ATT": ("Quick Health Check", 3, 0.1),

    # CAA - CAT
    "CAA": ("Email Parsing", 6, 0.5),
    "CAC": ("User Report Gen", 14, 1.5),
    "CAG": ("System Audit", 16, 2.0),
    "CAT": ("Data Normalization", 11, 1.0),

    # CCA - CCT
    "CCA": ("Backup Verification", 9, 0.5),
    "CCC": ("Error Logging", 5, 0.25),
    "CCG": ("File Compression", 7, 0.75),
    "CCT": ("Folder Cleanup", 8, 1.0),

    # CGA - CGT
    "CGA": ("Deploy Update", 20, 2.0),
    "CGC": ("Server Monitoring", 12, 1.0),
    "CGG": ("Data Import", 15, 1.5),
    "CGT": ("Test Suite Run", 10, 1.0),

    # CTA - CTT
    "CTA": ("Schedule Tasks", 8, 0.5),
    "CTC": ("Merge Branch", 12, 1.0),
    "CTG": ("Code Review", 9, 0.75),
    "CTT": ("Quick Fix Patch", 6, 0.25),

    # GAA - GAT
    "GAA": ("Log Rotation", 5, 0.25),
    "GAC": ("DB Cleanup", 10, 1.0),
    "GAG": ("Security Scan", 18, 2.0),
    "GAT": ("Config Update", 7, 0.5),

    # GCA - GCT
    "GCA": ("Performance Test", 12, 1.5),
    "GCC": ("Dependency Check", 6, 0.5),
    "GCG": ("Script Deployment", 14, 1.5),
    "GCT": ("Code Refactor", 10, 1.0),

    # GGA - GGT
    "GGA": ("Analytics Report", 15, 2.0),
    "GGC": ("Database Backup", 20, 3.0),
    "GGG": ("Model Evaluation", 25, 4.0),
    "GGT": ("Quick Metrics", 8, 0.5),

    # GTA - GTT
    "GTA": ("User Data Sync", 18, 2.0),
    "GTC": ("System Patch", 12, 1.0),
    "GTG": ("Automated Test", 10, 1.0),
    "GTT": ("Email Digest", 5, 0.25),

    # TAA - TAT
    
    "TAC": ("Weekly Summary", 18, 2.0),
    "TAG": ("Monthly Audit", 25, 3.0),
    "TAT": ("Quick Reminder", 3, 0.1),

    # TCA - TCT
    "TCA": ("Clean Logs", 6, 0.5),
    "TCC": ("Backup Files", 10, 1.0),
    "TCG": ("Validate Data", 12, 1.5),
    "TCT": ("Generate CSV", 8, 0.75),

    # TGA - TGT
    "TGA": ("Notify Users", 5, 0.25),
    "TGC": ("System Reboot", 7, 0.5),
    "TGG": ("Script Audit", 15, 2.0),
    "TGT": ("Quick Patch", 6, 0.25),

    # TTA - TTT
    "TTA": ("Log Aggregation", 12, 1.0),
    "TTC": ("Database Check", 14, 1.5),
    "TTG": ("Performance Audit", 18, 2.0),
    "TTT": ("Code Deployment", 20, 3.0),
}



def translate_dna_to_tasks(dna: str):
    """
    Converts a DNA string into a list of tasks (from CODON_TASK_MAP).
    Each codon = one task.
    """
    codons = [dna[i:i+3] for i in range(0, len(dna), 3)]
    tasks = []
    for codon in codons:
        if codon in CODON_TASK_MAP:
            tasks.append(CODON_TASK_MAP[codon])
    return tasks

def automation_fitness(dna: str, max_hours: float = 8.0):
    """
    Fitness function for automation scheduling (DNA mode).
    - Translates DNA into tasks
    - Sums productivity and time
    - Rewards high productivity / unit time
    - Penalizes if time exceeds max_hours
    """
    tasks = translate_dna_to_tasks(dna)
    total_points = sum(t[1] for t in tasks)
    total_time = sum(t[2] for t in tasks)

    if total_time == 0:
        return 0.01

    productivity_rate = total_points / total_time
    if total_time > max_hours:
        productivity_rate *= 0.5  # penalty

    return productivity_rate


# ------------------------------
# Demo
# ------------------------------
if __name__ == "__main__":
    # DNA-based demo
    dna_example = "AAAATGATC"  # Data Cleanup + Model Training + DB Sync
    tasks = translate_dna_to_tasks(dna_example)
    print("DNA:", dna_example)
    print("Decoded tasks:")
    for task in tasks:
        print(f" - {task[0]} ({task[1]} pts, {task[2]} hr)")
    print("Fitness:", automation_fitness(dna_example))

    # Task-list based demo
    task_dict = {
        "script1": {"points": 50, "time": 2},
        "script2": {"points": 30, "time": 1.5},
        "script3": {"points": 10, "time": 0.5},
    }
    af = AutomationFitness(task_dict)
    candidate = ["script1", "script3"]
    print("\nTask list candidate:", candidate)
    print("Points/hr:", af.points_per_hour(candidate))
    print("Weighted balance:", af.weighted_balance(candidate))
    print("Deadline penalty:", af.deadline_penalty(candidate, deadline=3))
