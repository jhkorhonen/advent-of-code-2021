from collections import deque

input_energy_levels = [
    [2,2,3,8,5,1,8,6,1,4,],
    [4,5,5,2,3,8,8,5,5,3,],
    [2,5,6,2,1,2,1,1,4,3,],
    [2,6,6,6,6,8,5,3,3,7,],
    [7,5,7,5,5,1,8,7,8,4,],
    [3,5,7,2,5,3,4,8,7,1,],
    [8,4,1,1,7,1,8,2,8,3,],
    [7,7,4,2,6,6,8,3,8,5,],
    [1,2,3,5,1,3,3,2,3,1,],
    [2,5,4,6,1,6,5,3,4,5,],
]

lx,ly = len(input_energy_levels[0]), len(input_energy_levels)

def map_points(): return ((x,y) for x in range(lx) for y in range(ly))
def on_map(x,y): return x >= 0 and x < lx and y >= 0 and y < ly
def neighbours(x,y): return ( (x+dx,y+dy) for dx,dy in {(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] } - {(0,0)} if on_map(x+dx,y+dy))

def step(energy_levels):
    new_energy_levels = [[e + 1 for e in row ] for row in energy_levels]
    count_flashes = 0
    flashes = [[False]*lx for _ in range(lx)]
    flash_queue = deque()
    for (x,y) in map_points():
        if new_energy_levels[x][y] > 9:
            flash_queue.appendleft((x,y))
            flashes[x][y] = True
    while len(flash_queue) > 0:
        (x,y) = flash_queue.pop()
        new_energy_levels[x][y] = 0
        count_flashes = count_flashes + 1
        for (x1,y1) in neighbours(x,y):
            if not flashes[x1][y1]:
                new_energy_levels[x1][y1] = new_energy_levels[x1][y1] + 1
                if new_energy_levels[x1][y1] > 9:
                    flashes[x1][y1] = True
                    flash_queue.appendleft((x1,y1))    
    return new_energy_levels, count_flashes

# 1

total_flashes = 0
energy_levels = input_energy_levels
for t in range(0,100):
    energy_levels, flashes = step(energy_levels)
    total_flashes = total_flashes + flashes

print(total_flashes)

# 2

energy_levels = input_energy_levels

t = 0
while True:
    t = t + 1
    energy_levels, flashes = step(energy_levels)
    if flashes == lx*ly:
        print(t)
        break