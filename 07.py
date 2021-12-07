from tools import read
from math import floor, ceil
from statistics import mean,median

crabs = [ int(x) for x in read("07.txt")[0].split(",")]

def eval(f,z,l):
    return sum( [ f(abs(x - z)) for x in l] )

# 1

print(eval( lambda n: n, round(median(crabs)), crabs))

# 2

# illegal heuristic solution
print(eval( lambda n: n * (n+1)/2.0, mean(crabs), crabs))         # individual objectives are not actually quadratic, 
print(eval( lambda n: n * (n+1)/2.0, floor(mean(crabs)), crabs))  # so mean is not the optimum
print(eval( lambda n: n * (n+1)/2.0, ceil(mean(crabs)), crabs))   # close enough though  ¯\_(ツ)_/¯

# legal brute-force solution
print(min( [eval( lambda n: n * (n+1)/2.0, i, crabs) for i in range(min(crabs),max(crabs)+1)] ))

