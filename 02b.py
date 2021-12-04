with open("input.txt") as f:
    commands = [line.strip() for line in f]
    

pos = 0    
depth = 0
aim = 0

for com in commands:
    print(com)
    if com.startswith("up"):
        aim = aim - int(com[len("up"):])
    if com.startswith("down"):
        aim = aim + int(com[len("down"):])
    if com.startswith("forward"):
        move = int(com[len("forward"):])
        pos = pos + move
        depth = depth + aim*move
    
print(pos, depth)
print(pos*depth)