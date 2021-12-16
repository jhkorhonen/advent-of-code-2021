from tools import read


data = read("15.txt")
risks = [[int(c) for c in line.strip()] for line in data]
lx,ly = len(risks[0]), len(risks)
risks = [[risks[y][x] for y in range(ly) ] for x in range(lx)] # transpose

big_distance = 25*lx*ly*10

def map_points(): return ((x,y) for x in range(lx) for y in range(ly))
def on_map(x,y): return x >= 0 and x < lx and y >= 0 and y < ly
def neighbours(x,y): return ( (x+dx,y+dy, c) for dx,dy,c in [(0,1, "^"), (1,0,"<"), (0,-1,"v"), (-1,0,">")] if on_map(x+dx,y+dy))


# implement a proper queue inside this thing
class queue_wrapper:
    def __init__(self,queue_items):
        self.queue_items = sorted(queue_items)
    
    def pop(self):
        top = self.queue_items[0]
        self.queue_items = self.queue_items[1:]
        return top
    
    def update(self):
        self.queue_items.sort()
        
    def empty(self):
        return len(self.queue_items) == 0
        


# data format : [current distance, (x,y), visited]

distances = [[ [ big_distance, (x,y), False, " "] for y in range(ly)  ] for x in range(lx)]
distances[0][0][0] = 0

pq = queue_wrapper([ t for line in distances for t in line])

while not pq.empty():
    current = pq.pop()
    d, (x,y), _, _ = current
    current[2] = True
    # print(current)
    for (x1, y1, c) in neighbours(x,y):
        if x1 == lx-1 and y1 == lx-1:
            print(distances[x1][y1], x,y, c)
        nb = distances[x1][y1]
        if not nb[2] and nb[0] > d + risks[x1][y1]:
            nb[0] = d + risks[x1][y1]
            nb[3] = c
    pq.update()

print(distances[lx-1][ly-1])


for y in range(ly):
    line = [distances[x][y][3] for x in range(lx)]
    print("".join(line))