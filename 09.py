from tools import read
from collections import Counter
from math import prod

# parsing

data = read("09.txt")

heights = [[int(c) for c in line.strip()] for line in data]
print(heights)

lx = len(heights[0])
ly = len(heights)

def neighbours(x,y):
    nbs = []
    if x > 0:
        nbs.append((x-1, y))
    if x < lx-1:
        nbs.append((x+1, y))
    if y > 0:
        nbs.append((x, y-1))
    if y < ly-1:
        nbs.append((x, y+1))
    return nbs

# 1

total_risk = 0
for (x,y) in ((x,y) for x in range(lx) for y in range(ly)):
    if all(heights[x1][y1] > heights[x][y] for (x1,y1) in neighbours(x,y)):
        total_risk = total_risk + heights[x][y] + 1

print(total_risk)

# 2

low_points = 0
basin_map = [[0 for x in range(lx) ] for y in range(ly)]

for (x,y) in ((x,y) for x in range(lx) for y in range(ly)):
    if all(heights[x1][y1] > heights[x][y] for (x1,y1) in neighbours(x,y)):
        basin_map[x][y] = low_points + 1
        print(x,y,basin_map[x][y])
        low_points = low_points + 1

for line in basin_map:
    print("".join(str(x%10) for x in line))

# naive flooding because lazy
for i in range(lx+ly):
    for (x,y) in ((x,y) for x in range(lx) for y in range(ly)):
        if heights[x][y] < 9:
            basin_map[x][y] = max([basin_map[x1][y1] for (x1,y1) in neighbours(x,y) if heights[x1][y1] < 9]+ [basin_map[x][y]])

for line in basin_map:
    print("".join(str(x%10) for x in line))

counts = Counter(x for line in basin_map for x in line if x != 0)
print(prod( c for n,c in counts.most_common(3) ))




