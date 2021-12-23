
from tools import read
from itertools import product
import bisect 

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1

def intersects(cube1, cube2):
    for dim in range(3):
        if cube2[dim][1] < cube1[dim][0] or cube1[dim][0] < cube2[dim][0]:
            return False
    return True


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
            
        i,j,k = indices
        return self.values[(self.fences[0][i], self.fences[1][j], self.fences[2][k])]
        
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
    switch, cube = line.split(" ")
    coordinates = [ [int(p) for p in axis[2:].split("..")] for axis in cube.split(",")]
    cubes.append([switch, coordinates])
    

# 1, baby solution

# init_area = [[[0 for _ in range(101)] for _ in range(101)]  for _ in range(101)]
# for cube in cubes[:20]:
#     switch, coordinates = cube
#     switch = 1 if switch == "on" else 0
#     xs, ys, zs = coordinates
#     xs[1] += 1
#     ys[1] += 1
#     zs[1] += 1
#     for x, y, z in product(range(*xs),range(*ys),range(*zs)):
#         init_area[x+50][y+50][z+50] = switch
#     print(sum(sum(sum(p) for p in l) for l in init_area))
#
# print(sum(sum(sum(p) for p in l) for l in init_area))

# 2, proper solution

current_grid = grid([[0,10],[0,10],[0,10]],1)
i = 0
for cube in cubes:
    # print(current_grid.lit_count())
    switch, coordinates = cube
    switch = 1 if switch == "on" else 0
    current_grid = current_grid.refine(tuple(coordinates[dim][0]-1 for dim in range(3)))
    # print(current_grid.lit_count())
    current_grid = current_grid.refine(tuple(coordinates[dim][1] for dim in range(3)))
    # print(current_grid.lit_count())
    # for k, v in current_grid.values.items():
    #     print(k,v)
    current_grid.apply_cube(coordinates, switch)
    # print(current_grid.fences)
    # for k, v in current_grid.values.items():
    #     print(k,v)
    i += 1
    print(i)

print("done")
print(current_grid.lit_count())
# print(current_grid.lit_count())

# class cube:
#     def __init__(self, coordinates, lit):
#         self.xs, self.ys, self,zs = coordinates
#         self.lit = lit
#
#     def split(self,other):
#         cubes = [self,other]
#
        