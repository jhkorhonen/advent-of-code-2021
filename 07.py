from tools import read

crabs = [ int(x) for x in read("07.txt")[0].split(",")]
min_pos = min(crabs)
max_pos = max(crabs)

# 1

print(min([sum([abs(x-pos) for x in crabs]) for pos in range(min_pos,max_pos+1)]))

# 2

def cost(n):
    return (n * (n + 1)) / 2

print(min([sum([cost(abs(x-pos)) for x in crabs]) for pos in range(min_pos,max_pos+1)]))