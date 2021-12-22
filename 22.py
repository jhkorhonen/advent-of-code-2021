
from tools import read
from itertools import product


data = read("22.input.txt")

cubes = []
for line in data:
    switch, cube = line.split(" ")
    coordinates = [ [int(p) for p in axis[2:].split("..")] for axis in cube.split(",")]
    cubes.append([switch, coordinates])
    

# 1, baby solution

init_area = [[[0 for _ in range(101)] for _ in range(101)]  for _ in range(101)]
for cube in cubes[:20]:
    switch, coordinates = cube
    switch = 1 if switch == "on" else 0
    xs, ys, zs = coordinates
    xs[1] += 1
    ys[1] += 1
    zs[1] += 1
    for x, y, z in product(range(*xs),range(*ys),range(*zs)):
        init_area[x+50][y+50][z+50] = switch

print(sum(sum(sum(p) for p in l) for l in init_area))