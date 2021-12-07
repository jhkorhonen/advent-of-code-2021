from tools import read
from math import floor, ceil
from statistics import mean,median

crabs = [ int(x) for x in read("07.txt")[0].split(",")]

def eval(f,z,l):
    return sum( [ f(abs(x - z)) for x in l] )

# 1

print(eval( lambda n: n, floor(median(crabs)), crabs))
print(eval( lambda n: n, ceil(median(crabs)), crabs))

# 2

print(eval( lambda n: n * (n+1)/2, floor(mean(crabs)), crabs))
print(eval( lambda n: n * (n+1)/2, ceil(mean(crabs)), crabs))