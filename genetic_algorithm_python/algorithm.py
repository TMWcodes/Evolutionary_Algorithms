import random
def foo(x,y,z):
    # when x y and z inputs result in 25
    # do this by setting it to zero.
    return 6*x**3 + 9*y**2 + 90*z -25

# print(foo(6,5,3))

# Rank parameters
def fitness(x,y,z):
    # run foo function
    ans = foo(x,y,z)
    # if zero return large number else return abs value.
    if ans == 0:
        return 99999
    else:
        #smaller the result the higher it ranks
        #absolute = regardless of positive or negative.
        return abs(1/ans) 

# print(fitness(6,5,3))

# generate solutions
solutions = []
for s in range(1000):
    #tuple of 3 random answers between zero and ten thousand
    solutions.append( ( random.uniform(0,10000),
                        random.uniform(0,10000),
                        random.uniform(0,10000)))

# print(solutions[:5])

# how many times it will run.
for i in range(10000):
    ranked_solutions = []
    # for every element in solutions
    for s in solutions:
        # add fitness function value and tuple
        # (rank, (v1,v2,v3))
        ranked_solutions.append((fitness(s[0],s[1],s[2]),s))
        
    ranked_solutions.sort()
    # biggest to smallest
    ranked_solutions.reverse()
    
    print(f"=== Gen {i} best solutions ===")
    print(ranked_solutions[0])

    # stop loop if ranked solution (top) is good enough
    if ranked_solutions[0][0] > 999:
        break
    
    # take top 100 ranked solutions into best solutions
    best_solutions = ranked_solutions[:100]
    # elements will hold parameters for best solutions
    elements = []
    for s in best_solutions:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])

    newGen = []
    for _ in range(1000):
        # mutate solutions by 2%
        e1 = random.choice(elements) * random.uniform(0.99,1.01)
        e2 = random.choice(elements) * random.uniform(0.99,1.01)
        e3 = random.choice(elements) * random.uniform(0.99,1.01)

        newGen.append((e1, e2, e3))
    

    solutions = newGen
