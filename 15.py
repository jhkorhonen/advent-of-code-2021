from tools import read
import heapq

# why does heapq not expose decrease key operation?
class queue_wrapper:
    def __init__(self):
        self.queue = []
        
    def pop(self):
        return heapq.heappop(self.queue)
    
    def push(self,item):
        heapq.heappush(self.queue, item)

    def empty(self):
        return len(self.queue) == 0

def dijkstra(risks):
    lx, ly = len(risks), len(risks[0])
    big_distance = lx*ly*10
    
    def map_points(): return ((x,y) for x in range(lx) for y in range(ly))
    def on_map(x,y): return x >= 0 and x < lx and y >= 0 and y < ly
    def neighbours(x,y): return ( (x+dx,y+dy, c) for dx,dy,c in [(0,1, "^"), (1,0,"<"), (0,-1,"v"), (-1,0,">")] if on_map(x+dx,y+dy))
    
    
    distances = [[ big_distance for y in range(ly)  ] for x in range(lx) ]
    visited = [[ False for y in range(ly)  ] for x in range(lx) ]
    direction = [[ " " for y in range(ly)  ] for x in range(lx) ]
    
    pq = queue_wrapper()
    pq.push( (0, (0,0)) )
    distances[0][0] = 0
    
    while not pq.empty():
        current = pq.pop()
        d, (x,y)= current
        if not visited[x][y]:
            visited[x][y] = True
            for (x1, y1, c) in neighbours(x,y):
                if not visited[x1][y1] and distances[x1][y1] > d + risks[x1][y1]:
                    distances[x1][y1] = d + risks[x1][y1]
                    direction[x1][y1] = c
                    pq.push( (distances[x1][y1], (x1,y1)) ) # can push same item at most 4 times
                                                            # O(1) is O(1)
    
    return distances, direction

def print_directions(direction):
    for y in range(len(direction[0])):
        line = [direction[x][y] for x in range(len(direction))]
        print("".join(line))

# 1 

data = read("15.txt")
risks = [[int(c) for c in line.strip()] for line in data]
risks = [[risks[y][x] for y in range(len(risks)) ] for x in range(len(risks[0]))] # transpose

distances, direction = dijkstra(risks)
print(distances[-1][-1])
print_directions(direction)

# 2

big_risks = [[ (risks[x][y]+i + j - 1)%9 + 1 for i in range(5) for y in range(len(risks[0]))] for j in range(5) for x in range(len(risks))]
distances, direction = dijkstra(big_risks)
print(distances[-1][-1])
