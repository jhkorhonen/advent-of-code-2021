
from tools import read
from itertools import product

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
        x, y, z = point
        if x < self.fences[0][0] or y < self.fences[1][0] or z < self.fences[2][0]:
            return 0
        if x >= self.fences[0][-1] or y >= self.fences[1][-1] or z >= self.fences[2][-1]:
            return 0
        i, j, k = 0,0,0
        while x >= self.fences[0][i]:
            i += 1
        i -= 1
        while y >= self.fences[1][j]:
            j += 1
        j -= 1
        while z >= self.fences[2][k]:
            k += 1
        k -= 1
        # print(self.fences)
        # print(point)
        return self.values[(self.fences[0][i], self.fences[1][j], self.fences[2][k])]
        
    def __setitem__(self,point, value):
        self.values[point] = value

    # def get_cell(self,point):
    
    def point_by_index(self,indices):
        i,j,k = indices
        return (self.fences[0][i],self.fences[1][j],self.fences[2][k])

    def refine(self, point):
        new_fences = []
        for dim in range(3):
            if point[dim] in self.fences[dim]:
                new_fences.append(self.fences[dim].copy())
            else:
                new_fences.append(sorted(self.fences[dim].copy() + [point[dim]]))
                
        new_grid = grid(new_fences, 0)
        for new_grid_point in new_grid.values.keys():
            new_grid[new_grid_point] = self[new_grid_point]
        
        # for (i, j, k) in product(range(len(new_grid.fences[0])-1), range(len(new_grid.fences[1])-1), range(len(new_grid.fences[2])-1) ):
        #     p = new_grid.point_by_index((i,j,k))
        #     if p in self.values:
        #         new_grid[p] = self[p]
        #     else:
        #         pi, pj, pk = i, j, k
        #         if i == 0 or j == 0 or k == 0:
        #             new_grid[p] = 0
        #         elif i == len(new_grid.fences[0])-1 or j == len(new_grid.fences[1])-1 or k == len(new_grid.fences[2])-1:
        #             new_grid[p] = 0
        #         else:
        #             if not new_grid.fences[0][i] in self.fences[0]:
        #                 pi = i - 1
        #             if not new_grid.fences[1][j] in self.fences[1]:
        #                 pj = j - 1
        #             if not new_grid.fences[2][k] in self.fences[2]:
        #                 pk = k -1
        #             new_grid[p] = self[new_grid.point_by_index((pi,pj,pk))]
        # # for p in new_grid.values.keys():
        # #     if p in self.values.keys():
        # #         new_grid[p] = self[p]
        # #     else:
        # #         done = False
        # #         for dim in range(3):
        # #             if p[dim] < self.fences[dim][0] or p[dim] >= self.fences[dim][-1]:
        # #                 new_grid[p] = 0
        # #                 done = True
        # #                 break
        # #         if not done:
        # #             new_grid[p] = self[self.get_cell(p)]
        return new_grid
        
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
for cube in cubes[:20]:
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
        