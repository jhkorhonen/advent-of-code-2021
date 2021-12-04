
with open("input.txt") as f:
    depths = [int(line) for line in f]

c = 0
for i in range(len(depths)-1):
    if depths[i] < depths[i+1]:
        c = c + 1
print(c)


c = 0
a = depths[0]+depths[1]+depths[2]
for i in range(len(depths)-3):
    b = a + depths[i+3] - depths[i]
    if a < b:
        c = c + 1
print(c)