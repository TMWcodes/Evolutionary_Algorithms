import random

# ------------------------------
# MODE 1: Task-list based fitness
# ------------------------------
class AutomationFitness:
    """
    Provides multiple ways to evaluate automation schedules:
    1. Task-list fitness (traditional)
    2. Protein-inspired task fitness with start/stop codons
    """

    # ------------------------------
    # Constants for DNA/RNA mode
    # ------------------------------
    START_CODON = "AUG"         # RNA start
    STOP_CODONS = {"UAA", "UAG", "UGA"}  # RNA stop
    START_AA = "M"               # Methionine
    STOP_AA = "*"                # stop symbol

    def __init__(self, tasks=None, amino_task_map=None):
        """
        :param tasks: dict of task metadata
        :param amino_task_map: dict amino acid → (task_name, points, time)
        """
        self.tasks = tasks or {}
        self.amino_task_map = amino_task_map or AMINO_TASK_MAP

    # ------------------------------
    # Mode 1: Task-list fitness
    # ------------------------------
    def points_per_hour(self, candidate):
        total_points, total_time = self._evaluate(candidate)
        return total_points / total_time if total_time else 0.01

    def weighted_balance(self, candidate, alpha=0.5):
        total_points, total_time = self._evaluate(candidate)
        if total_time == 0:
            return 0.01
        max_points = max(v["points"] for v in self.tasks.values())
        max_eff = max(v["points"]/v["time"] for v in self.tasks.values())
        points_score = total_points / (max_points or 1)
        eff_score = (total_points/total_time) / (max_eff or 1)
        return alpha * points_score + (1 - alpha) * eff_score

    def deadline_penalty(self, candidate, deadline=8):
        total_points, total_time = self._evaluate(candidate)
        if total_time > deadline:
            penalty = (total_time - deadline) / deadline
            score = total_points * (1 - penalty)
        else:
            score = total_points
        return max(0.01, score)

    def _evaluate(self, candidate):
        total_points, total_time = 0, 0
        for task in candidate:
            if task in self.tasks:
                total_points += self.tasks[task]["points"]
                total_time += self.tasks[task]["time"]
        return total_points, total_time

    # ------------------------------
    # Mode 2: Protein-based automation
    # ------------------------------
    def dna_to_rna(self, dna: str):
        """Convert DNA string to RNA string."""
        return dna.replace("T", "U")

    def rna_to_protein(self, rna: str, aminoacid_dict):
        """Translate RNA sequence to protein sequence using aminoacid_dict."""
        codons = [rna[i:i+3] for i in range(0, len(rna)-2, 3)]
        return ''.join(aminoacid_dict.get(c, '') for c in codons)

    def protein_to_tasks(self, protein: str):
        """
        Translate protein sequence into task list.
        Starts at 'M', stops at '*'.
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

    def translate_dna_to_tasks(self, dna: str, aminoacid_dict):
        """
        Convert DNA → RNA → protein → tasks
        """
        rna = self.dna_to_rna(dna)
        protein_seq = self.rna_to_protein(rna, aminoacid_dict)
        return self.protein_to_tasks(protein_seq), rna, protein_seq

    def automation_fitness(self, protein: str, max_hours: float = 8.0):
        """Compute fitness for protein-based automation schedule."""
        tasks = self.protein_to_tasks(protein)
        total_points = sum(t[1] for t in tasks)
        total_time = sum(t[2] for t in tasks)
        if total_time == 0:
            return 0.01
        productivity_rate = total_points / total_time
        if total_time > max_hours:
            productivity_rate *= 0.5
        return productivity_rate


# ------------------------------
# Example AMINO ACID → TASK MAP
# ------------------------------
AMINO_TASK_MAP = {
    # Start codon
    "M": ("Model Training", 30, 5.0),

    # Common amino acids → tasks
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
    
    # Stop codon
    "*": ("End Marker", 0, 0),
}
