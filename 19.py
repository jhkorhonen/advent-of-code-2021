import numpy as np
from tools import read
from itertools import groupby

# rotation matrices

Id = np.identity(3)

Rx = np.array([
    [ 1,  0,  0],
    [ 0,  0, -1],
    [ 0,  1,  0]
])

Ry = np.array([
    [ 0,  0,  1],
    [ 0,  1,  0],
    [-1,  0,  0]
])

Rz = np.array([
    [ 0, -1,  0],
    [ 1,  0,  0],
    [ 0,  0,  1]
])

def repeat(A):
    current = Id
    for i in range(4):
        yield current
        current = A @ current


# all possible combinations of rotations
# surely there is a better way
rotations = []
rotations.extend([ A@B for B in [Id, Ry@Ry] for A in repeat(Rx)  ]) # -> x, -> -x
rotations.extend([ A@B for B in [Rz, Rz@Rz@Rz] for A in repeat(Ry)  ]) # -> y, -> -y
rotations.extend([ A@B for B in [Ry, Ry@Ry@Ry] for A in repeat(Rz)  ]) # -> z, -> -z

# scanner pattern matching stuff

def count_matches(A, B):
    A_points = { tuple(A[:,i]) for i in range(A.shape[1])}
    B_points = { tuple(B[:,i]) for i in range(B.shape[1])}
    
    # A_points = { tuple([int(x) for x in A[:,i]]) for i in range(A.shape[1])}
    # B_points = { tuple([int(x) for x in B[:,i]]) for i in range(B.shape[1])}
    # print(A_points, B_points)
    return len(A_points & B_points)

def try_shifts(A,B):
    for i in range(A.shape[1]):
        for j in range(B.shape[1]):
            shift = A[:,i] - B[:,j]
            if count_matches(A, B + shift[:,None]) >= 12:
                return True, shift
    return False, None

def try_rotations(A,B):
    for rot in rotations:
        C = rot@B
        # print(C)
        matches, shift = try_shifts(A,C)
        if matches:
            return True, rot, shift
    return False, None, None


# processing

data = read("19.input.txt")

scanners = []
scanners_iter = groupby(data, lambda line: line[:3] == "---")
for is_header, points in scanners_iter:
    if not is_header:
        scanners.append(np.swapaxes(np.array([eval("[{}]".format(p)) for p in points if p != ""]),0,1))


aligned_scanners = [scanners[0]]
unaligned_scanners = scanners[1:]

scanner_positions = [(0,0,0)]

while len(unaligned_scanners) > 0:
    unaligned_new = []
    for s in unaligned_scanners:
        matched = False
        for t in aligned_scanners:
            matched, rot, shift = try_rotations(t,s)
            if matched:
                aligned_scanners.append(rot@s + shift[:,None])
                scanner_positions.append(tuple(shift))
                break
        if not matched:
            unaligned_new.append(s)
    unaligned_scanners = unaligned_new

# 1

points = { tuple(s[:,i]) for s in aligned_scanners for i in range(s.shape[1])}
print(len(points))

# 2

max_distance = max(abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) for (x1,y1,z1) in scanner_positions for (x2,y2,z2) in scanner_positions )
print(max_distance)