
target_x_min = 153
target_x_max = 199

target_y_min = -114
target_y_max = -75

def in_target(x,y):
    return x >= target_x_min and x <= target_x_max and y >= target_y_min and y <= target_y_max
    

def path_points(dx,dy):
    x = 0
    y = 0
    while True:
        yield (x,y)
        x += dx
        y += dy
        dx = max(0, dx-1)
        dy -= 1

# 1

max_y = 0
hits = 0
for dx in range(2*target_x_max):
    for dy in range(2*target_y_min,-2*target_y_max):
        current_max_y = 0
        hit_target = False
        for (x,y) in path_points(dx,dy):
            if x > target_x_max or y < target_y_min:
                break
            current_max_y = max(y,current_max_y)
            if in_target(x,y):
                max_y = max(max_y, current_max_y)
                print(dx,dy)
                hit_target = True
        if hit_target:
            hits += 1

print(max_y)
print(hits)