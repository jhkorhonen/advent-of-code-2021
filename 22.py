
from tools import read
from math import prod
from itertools import product
import bisect 

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1
    

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
        
    def bisect(self,split_dim,line,split_cube = None):
        if line <= self.corners[0][split_dim] or self.corners[1][split_dim] <= line:
            return {self}
        if not split_cube is None and not self.intersects(split_cube):
            return {self}
        pairs = [[[self.corners[0][dim],self.corners[1][dim]]] for dim in range(3)]
        pairs[split_dim] = [[self.corners[0][split_dim],line], [line, self.corners[1][split_dim]]]
        new_cubes = set()
        for p0 in pairs[0]:
            for p1 in pairs[1]:
                for p2 in pairs[2]:
                    new_cubes.add( cube( ((p0[0], p1[0], p2[0]), (p0[1], p1[1], p2[1])) ))
        return new_cubes
    
    def intersects(cube1,cube2):
        for dim in range(3):
            if cube2.corners[1][dim] <= cube1.corners[0][dim] or cube1.corners[1][dim] <= cube2.corners[0][dim]:
                return False
        return True
    
    def size(self):
        return prod([ self.corners[1][dim] - self.corners[0][dim] for dim in range(3)])
    
    def __str__(self):
        return str(self.corners)

class grid:
    def __init__(self, fences, initial_value):
        self.fences = fences
        corners = { (x,y,z) for x in fences[0][:-1] for y in fences[1][:-1] for z in fences[2][:-1]  } 
        self.values = { p : initial_value for p in corners}
    
    def __getitem__(self,point):
        if point in self.values:
            return self.values[point]
        x, y, z = point
        if x < self.fences[0][0] or y < self.fences[1][0] or z < self.fences[2][0]:
            return 0
        if x >= self.fences[0][-1] or y >= self.fences[1][-1] or z >= self.fences[2][-1]:
            return 0
            
        indices = [0,0,0]
        for dim in range(3):
            indices[dim] = bisect.bisect_right(self.fences[dim], point[dim])-1
        return self.values[tuple(self.fences[dim][indices[dim]] for dim in range(3))]
                    
    def __setitem__(self,point, value):
        self.values[point] = value

    def point_by_index(self,indices):
        i,j,k = indices
        return (self.fences[0][i],self.fences[1][j],self.fences[2][k])

    def refine(self, point):   
        # had_already = [True, True, True]
        new_fences = []
        for dim in range(3):
            if index(self.fences[dim], point[dim]) == -1:
                # had_already[dim] = False
                new_fences.append(sorted(self.fences[dim] + [point[dim]]))
            else:
                new_fences.append(self.fences[dim])
        
        new_values = {}

        x1, y1, z1 = point        
        point_prime = [x1, y1, z1]
        for dim in range(3):
            if point[dim] == new_fences[dim][-1]:
                point_prime[dim] = new_fences[dim][-2]
    
        x1, y1, z1 = point_prime
        new_values[(x1, y1, z1)] = self[(x1, y1, z1)]
        for new_grid_point in { (x1,y,z) for y in self.fences[1][:-1] for z in self.fences[2][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        for new_grid_point in { (x,y1,z) for x in self.fences[0][:-1] for z in self.fences[2][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        for new_grid_point in { (x,y,z1) for x in self.fences[0][:-1] for y in self.fences[1][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        for new_grid_point in { (x1,y1,z) for z in self.fences[2][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        for new_grid_point in { (x,y1,z1) for x in self.fences[0][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        for new_grid_point in { (x1,y,z1) for y in self.fences[1][:-1]  }:
            new_values[new_grid_point] = self[new_grid_point]
        
        
        self.fences = new_fences
        self.values.update(new_values)
        return self
        
    def apply_cube(self,cube,value):
        xs = [x for x in self.fences[0] if cube[0][0]-1 <= x and x < cube[0][1] ]
        ys = [y for y in self.fences[1] if cube[1][0]-1 <= y and y < cube[1][1] ]
        zs = [z for z in self.fences[2] if cube[2][0]-1 <= z and z < cube[2][1] ]
        for p in product(xs,ys,zs):
            self[p] = value
    
    def lit_count(self):
        total = 0
        for (i,j,k) in product(range(len(self.fences[0])-1), range(len(self.fences[1])-1), range(len(self.fences[2])-1) ):
            v = self[self.fences[0][i],self.fences[1][j],self.fences[2][k]]
            lx = self.fences[0][i+1] - self.fences[0][i]
            ly = self.fences[1][j+1] - self.fences[1][j]
            lz = self.fences[2][k+1] - self.fences[2][k]
            total += v*lx*ly*lz
        return total
        
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
baby_solutions = []
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
    baby_solutions.append(sum(sum(sum(p) for p in l) for l in init_area))

print(sum(sum(sum(p) for p in l) for l in init_area))
print("--")

# 2, proper solution

def reformat_input(coordinates):
    return ((coordinates[0][0],coordinates[1][0],coordinates[2][0]), (coordinates[0][1]+1,coordinates[1][1]+1,coordinates[2][1]+1))

def bisect_all(cubes, fences, bisect_cube = None):
    current_cubes = cubes
    for dim in range(3):
        for f in fences[dim]:
            new_cubes = set()
            for c in current_cubes:
                if not bisect_cube is None:
                    new_cubes |= c.bisect(dim,f,bisect_cube)
                else:
                    new_cubes |= c.bisect(dim,f)
            current_cubes = new_cubes
    return current_cubes


# test_cube = cube( ((0,0,0),(10,10,10)) )
# print(sum( c.size() for c in test_cube.bisect(0,5)  ))


cubes = [(c[0],reformat_input(c[1])) for c in cubes]
#
first_cube = cube(cubes[0][1])
processed_cubes = { first_cube }
fences = [first_cube.get_fences(dim) for dim in range(3)]




#
t = 0
print(sum(c.size() for c in processed_cubes))

for line in cubes[1:20]:
    t = t+1
    switch, coords = line
    added_cube = cube(coords)
    added_fences = [added_cube.get_fences(dim) for dim in range(3)]
    processed_cubes = bisect_all(processed_cubes,added_fences,added_cube)
    if switch == "on":
        new_processed_cubes = bisect_all([added_cube], fences)
        processed_cubes = processed_cubes | new_processed_cubes
        fences = [ sorted(list(set().union(fences[dim],added_fences[dim])) )  for dim in range(3) ]
    if switch == "off":
        processed_cubes = { c for c in processed_cubes if not c.intersects(added_cube)}
        fences = [ sorted(list(set().union(fences[dim],added_fences[dim])) )  for dim in range(3) ]
    print(baby_solutions[t] if t < 20 else "-", sum(c.size() for c in processed_cubes), switch, t)
    # print(t, switch, len(processed_cubes))
















