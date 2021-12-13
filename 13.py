from tools import read

data = iter(read("13.txt"))
points = set()
line = next(data)
while line != "":
    points.add(tuple(map(int,line.split(","))))
    line = next(data)
    
# fold instructions
folds = [(line[11:12], int(line[13:])) for line in data]

# fold functions

def fold_x(point, line):
    x, y = point
    if x > line: return (line - (x - line), y)
    else: return (x,y)
    
def fold_y(point, line):
    x, y = point
    if y > line: return (x, line - (y - line))
    else: return (x,y)

def print_points(points):
    xmax = max(p[0] for p in current_points)+1
    ymax = max(p[1] for p in current_points)+1
    for y in range(ymax):
        print("".join("█" if (x,y) in current_points else " " for x in range(xmax)))

# 1

line = folds[0][1]
print(len({fold_x(p,line) for p in points}))

# 2

current_points = points
for fold in folds:
    axis, line = fold
    if axis == "x":
        current_points = {fold_x(p,line) for p in current_points}
    if axis == "y":
        current_points = {fold_y(p,line) for p in current_points}

print_points(points)