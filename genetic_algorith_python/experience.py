import math

# Function to calculate the experience difference between level L-1 and level L
def experience_difference(L):
    return math.floor((L - 1) + 300 * (2**(L - 1)) / 7)

# Function to calculate cumulative experience required for a given level L
def cumulative_experience(L):
    total_exp = 0
    for level in range(1, L+1):
        total_exp += experience_difference(level)
    return total_exp

# Testing with Level 2 to Level 10 to debug
for L in range(1, 11):
    cumulative_exp = cumulative_experience(L)
    exp_diff = experience_difference(L)
    print(f"Level {L}: Cumulative Experience: {cumulative_exp}, Experience Difference: {exp_diff}")