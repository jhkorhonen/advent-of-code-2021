from tools import read
from collections import Counter, deque
from math import prod

# parsing

data = read("09.txt")

heights = [[int(c) for c in line.strip()] for line in data]

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

queue = deque()

# invariant: if (x,y) is or has been in queue, it has non-zero value in basin_map
# -1 is ridge line
# 0 is unvisited

for (x,y) in ((x,y) for x in range(lx) for y in range(ly)):
    if all(heights[x1][y1] > heights[x][y] for (x1,y1) in neighbours(x,y)):
        basin_map[x][y] = low_points + 1
        low_points = low_points + 1
        queue.append((x,y))
    if heights[x][y] == 9:
        basin_map[x][y] = -1

while len(queue) >= 1:
    x,y = queue.popleft()
    for (x1,y1) in neighbours(x,y):
        if basin_map[x1][y1] == 0:
            basin_map[x1][y1] = basin_map[x][y]
            queue.append((x1,y1))

for line in basin_map:
    line = [str(x%10) if x != -1 else "█" for x in line]
    print("".join(line))

counts = Counter(x for line in basin_map for x in line if x != -1)
print(prod( c for n,c in counts.most_common(3) ))




