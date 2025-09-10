
def mutate(chromosome, p):
    import random
    mutated_string = ""
    for i in chromosome:
        if random.random() < p:
            if i == '1':
                mutated_string += "0"
            if i == "0":
                mutated_string += "1"
        else:
            mutated_string += i
    return mutated_string
print(mutate("101010", p=.5))


