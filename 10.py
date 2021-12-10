from tools import read
from collections import deque
from math import floor

data = read("10.txt")
opening_delim = { ")" : "(", "]" : "[", "}" : "{", ">" : "<",}
error_score = { ")" : 3, "]" : 57, "}" : 1197, ">" : 25137, }
completion_score = { "(" : 1, "[" : 2, "{" : 3, "<" : 4, }

# 1

total = 0
for line in data:
    stack = deque()
    for c in line:
        if c in "([{<":
            stack.append(c)
        if c in "}])>":
            d = stack.pop()
            if not d == opening_delim[c]:
                total = total + error_score[c]
                break

print(total)

# 2

line_scores = []

for line in data:
    stack = deque()
    corrupt = False
    for c in line:
        if c in "([{<":
            stack.append(c)
        if c in "}])>":
            d = stack.pop()
            if not d == opening_delim[c]:
                corrupt = True
                break
    if not corrupt:
        line_score = 0
        while len(stack) != 0:
            line_score = 5*line_score + completion_score[stack.pop()]
        if line_score != 0:
            line_scores.append(line_score)

line_scores.sort()
print(line_scores[ floor(len(line_scores)/2) ])