
from tools import read
from math import prod
from itertools import product

class cube:
    def __init__(self, corners):
        self.corners = corners
        
    def __hash__(self):
        return hash(self.corners)
        
    def __eq__(self, other):
        return self.corners == other.corners
    
    def meets(self,point):
        for dim in range(3):
            if point[dim] <= self.corners[0][dim] or self.corners[1][dim] <=  point[dim]:
                return true
        return False
    
    def get_fences(self,dim):
        return (self.corners[0][dim], self.corners[1][dim])
        
    def bisect(self,split_dim,line):
        if line <= self.corners[0][split_dim] or self.corners[1][split_dim] <= line:
            return {self}
        pairs = [[[self.corners[0][dim],self.corners[1][dim]]] for dim in range(3)]
        pairs[split_dim] = [[self.corners[0][split_dim],line], [line, self.corners[1][split_dim]]]
        new_cubes = set()
        for p0 in pairs[0]:
            for p1 in pairs[1]:
                for p2 in pairs[2]:
                    new_cubes.add( cube( ((p0[0], p1[0], p2[0]), (p0[1], p1[1], p2[1])) ))
        return new_cubes
        
    def split(self,other):
        split_cubes = {self}
        for dim in range(3):
            for f in other.get_fences(dim):
                new_splits = set()
                for c in split_cubes:
                    new_splits |= c.bisect(dim,f)
                split_cubes = new_splits
        return split_cubes
        
    def split_and_remove(self,other):
        split_cubes = self.split(other)
        return { c for c in split_cubes if not c.intersects(other) }
    
    def intersects(cube1,cube2):
        for dim in range(3):
            if cube2.corners[1][dim] <= cube1.corners[0][dim] or cube1.corners[1][dim] <= cube2.corners[0][dim]:
                return False
        return True
    
    def is_contained_in(self,other):
        for dim in range(3):
            if self.corners[0][dim] < other.corners[0][dim] or other.corners[1][dim] < self.corners[1][dim]:
                return False
        return True
        
    
    def size(self):
        return prod([ self.corners[1][dim] - self.corners[0][dim] for dim in range(3)])
    
    def __str__(self):
        return str(self.corners)
    
# parsing

data = read("22.input.txt")

cubes = []
for line in data:
    switch, coordinates_text = line.split(" ")
    coordinates = [ [int(p) for p in axis[2:].split("..")] for axis in coordinates_text.split(",")]
    cubes.append([switch, coordinates])
#

# 1, baby solution

init_area = [[[0 for _ in range(101)] for _ in range(101)]  for _ in range(101)]
for c in cubes[:20]:
    switch, coordinates = c
    switch = 1 if switch == "on" else 0
    xs, ys, zs = [l.copy() for l in coordinates]
    xs[1] += 1
    ys[1] += 1
    zs[1] += 1
    for x, y, z in product(range(*xs),range(*ys),range(*zs)):
        init_area[x+50][y+50][z+50] = switch

print(sum(sum(sum(p) for p in l) for l in init_area))

# 2, proper solution

def reformat_input(coordinates):
    return ((coordinates[0][0],coordinates[1][0],coordinates[2][0]), (coordinates[0][1]+1,coordinates[1][1]+1,coordinates[2][1]+1))

cubes = [(c[0],reformat_input(c[1])) for c in cubes]
#
first_cube = cube(cubes[0][1])
processed_cubes = { first_cube }

for line in cubes[1:]:
    switch, coords = line
    added_cube = cube(coords)
    new_processed_cubes = set()
    for c in processed_cubes:
        if not c.is_contained_in(added_cube):
            if c.intersects(added_cube):
                new_processed_cubes |= c.split_and_remove(added_cube)
            else:
                new_processed_cubes |= {c}
    processed_cubes = new_processed_cubes
    if switch == "on":
        processed_cubes.add(added_cube)

print(sum(c.size() for c in processed_cubes))








