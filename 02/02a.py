with open("input.txt") as f:
    commands = [line.strip() for line in f]

horizontal = sum([int(line[len("forward"):]) for line in commands if "forward" in line])

def to_vertical_command(com):
    if com.startswith("up"):
        return -int(com[len("up"):])
    if com.startswith("down"):
        return int(com[len("down"):])
    else:
        return 0

vertical = sum([to_vertical_command(line) for line in commands])

print(horizontal)
print(vertical)
print(horizontal*vertical)

