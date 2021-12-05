from tools import read
from collections import Counter
from math import copysign
data = read("05.txt")

def sline_to_points(a,b):
    xps = range(min(a[0],b[0]), max(a[0],b[0])+1)
    yps = range(min(a[1],b[1]), max(a[1],b[1])+1)
    return [(x,y) for x in xps for y in yps]

def dline_to_points(a,b):
    xdir = int(copysign(1,b[0]-a[0]))
    ydir = int(copysign(1,b[1]-a[1]))
    return list(zip(range(a[0],b[0]+xdir, xdir), range(a[1],b[1]+ydir, ydir)))
    
# parsing

lines = [line.split("->") for line in data]
lines = [[tuple(map(int,point.split(","))) for point in line ] for line in lines]
slines = [ l for l in lines if l[0][0] == l[1][0] or l[0][1] == l[1][1] ] # filter out diagonal lines 
dlines = [ l for l in lines if not( l[0][0] == l[1][0] or l[0][1] == l[1][1]) ] # diagonal lines

# 1

slines = [ sline_to_points(a,b) for a,b in slines]
counts = Counter([p for l in slines for p in l])
print(len([p for p,c in counts.items() if c >= 2]))

# 2

dlines = [ dline_to_points(a,b) for a,b in dlines]
counts = Counter([p for l in slines for p in l] + [p for l in dlines for p in l])
print(len([p for p,c in counts.items() if c >= 2]))