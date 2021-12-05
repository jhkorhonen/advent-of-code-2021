from tools import read
from collections import Counter
data = read("05.txt")

def line_to_points(l):
    (x1,y1), (x2,y2) = l
    xdist, ydist = x2-x1, y2-y1
    steps = max(abs(xdist),abs(ydist))
    dx,dy = xdist/steps, ydist/steps
    
    x,y = x1,y1
    for i in range(steps+1):
        yield (round(x),round(y))
        x,y = x+dx, y+dy
    
# parsing

lines = [line.split("->") for line in data]
lines = [[tuple(map(int,point.split(","))) for point in line ] for line in lines]

# 1

slines = [ l for l in lines if l[0][0] == l[1][0] or l[0][1] == l[1][1] ] # filter out diagonal lines 
spoints = [ p for l in slines for p in line_to_points(l) ]
counts = Counter(spoints)
print(len([p for p,c in counts.items() if c >= 2]))

# 2

points = [ p for l in lines for p in line_to_points(l) ]
counts = Counter(points)
print(len([p for p,c in counts.items() if c >= 2]))