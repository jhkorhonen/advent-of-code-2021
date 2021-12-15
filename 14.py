from tools import read
from collections import defaultdict

data = read("14.txt")

polymer_template = data[0]
rules = [tuple(line.split(" -> ")) for line in data[2:]]

insertions = { p : [p[0] + c, c + p[1]]   for p, c in rules}
created_element = { p : c for p, c in rules}

def simulate(polymer, steps):
    
    elements = defaultdict(int)
    current_pairs = defaultdict(int)
    
    for c in polymer:
        elements[c] += 1
    
    for i in range(len(polymer) - 1):
        current_pairs[polymer[i:i+2]] += 1

    for _ in range(steps):
        new_pairs = defaultdict(int)
        for p,c in current_pairs.items():
            elements[created_element[p]] += c
            for o in insertions[p]:
                new_pairs[o] += c
        current_pairs = new_pairs
    
    return elements
            

# 1,2

for steps in [10,40]:
    output_elements = simulate(polymer_template, steps)
    print(max(output_elements.values()) - min(output_elements.values()))