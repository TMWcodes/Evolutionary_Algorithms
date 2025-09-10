def reverse_complement(dna):
    reverse = []
    for i in dna:
        if i == "1":
            reverse.append('0')
        elif i == "0":
            reverse.append('1')
    return reverse


