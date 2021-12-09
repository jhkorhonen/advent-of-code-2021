from tools import read
from collections import Counter, deque
from math import prod

# parsing

data = read("09.txt")
heights = [[int(c) for c in line.strip()] for line in data]
lx,ly = len(heights[0]), len(heights)

def map_points(): return ((x,y) for x in range(lx) for y in range(ly))
def on_map(x,y): return x >= 0 and x < lx and y >= 0 and y < ly
def neighbours(x,y): return ( (x+dx,y+dy) for dx,dy in [(0,1), (1,0), (0,-1), (-1,0)] if on_map(x+dx,y+dy))
def is_sink(x,y): return all(heights[x1][y1] > heights[x][y] for (x1,y1) in neighbours(x,y))

# 1

print(sum( heights[x][y] + 1 for x,y in map_points() if is_sink(x,y) ))

# 2

low_points = 0
basin_map = [[0 for x in range(lx) ] for y in range(ly)]
queue = deque()

for (x,y) in map_points():
    if is_sink(x,y):
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




