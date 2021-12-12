from tools import read
from collections import defaultdict
from itertools import chain

data = read("12.txt")
edges = [ line.split("-") for line in data]
nodes = ["start"] + list({v for edge in edges for v in edge if v not in ["start", "end"]}) + ["end"]
ni = dict( zip(nodes, range(len(nodes))))
n = len(nodes)

# tools

def issmall(node):
    return node[0].islower()

class poly:
    def __init__(self, values):
        # values should be a defaultdict indexed with frozensets
        self.values = values
    
    def __add__(self, other):
        new_values = defaultdict(int)
        for k in chain(self.values.keys(), other.values.keys()):
            if self.values[k] + other.values[k] != 0:
                new_values[k] = self.values[k] + other.values[k]
        return poly(new_values)
    
    def __mul__(self,other):
        # multiply, discard terms that are not multilinear
        new_values = defaultdict(int)
        for s1, v1 in self.values.items():
            for s2, v2 in other.values.items():
                if s1.isdisjoint(s2) and v1*v2 != 0:
                    new_values[frozenset(s1 | s2)] += v1*v2
        return poly(new_values)
    
    def __eq__(self,other):
        return self.values == other.values
    
    def total(self):
        return sum(self.values.values())
        
    def __str__(self):
        if len(self.values)  == 0:
            return "0"
        else:
            return " + ".join([ str(v) + "·".join(sorted(k)) for k,v in self.values.items()])
    
    @classmethod
    def zero(cls,x):
        values = defaultdict(int)
        values[frozenset()] = x
        return poly(values)
    
    @classmethod
    def mono(cls,variable,x):
        values = defaultdict(int)
        values[frozenset([variable])] = x
        return poly(values)
    
    
    @classmethod
    def from_list(cls,l):
        values = defaultdict(int)
        for k, v in l:
            values[frozenset(k)] = v
        return poly(values)

# matrix operations

class mat:
    def __init__(self, values):
        self.values = values

    def __add__(A,B):
        C = mat.zero()
        for i in range(n):
            for j in range(n):
                C[i,j] = A[i,j] + B[i,j]
        return C

    def __mul__(A,B):
        C = mat.zero()
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i,j] += A[i,k] * B[k,j]
        return C

    def __eq__(A,B):
        for i in range(n):
            for j in range(n):
                if A[i,j] != B[i,j]:
                    return False
        return True
    
    def __getitem__(self, pos):
        i,j = pos
        return self.values[i][j]
    
    def __setitem__(self,pos,key):
        i,j = pos
        self.values[i][j] = key
    
    @classmethod
    def zero(cls):
        return mat([[poly.zero(0) for _ in range(n)] for _ in range(n)])
    
    @classmethod
    def id(cls):
        return mat([[poly.zero(1) if i == j else poly.zero(0) for i in range(n)] for j in range(n)])

# 1

I = mat.id()
A = mat([[poly.zero(0) for _ in range(n)] for _ in range(n)])
A[0,0] = poly.mono("start",1)

B = mat([[poly.zero(0) for _ in range(n)] for _ in range(n)])
for edge in edges:
    v,u = edge
    B[ni[v],ni[u]] = poly.mono(u,1) if issmall(u) else poly.zero(1)
    B[ni[u],ni[v]] = poly.mono(v,1) if issmall(v) else poly.zero(1)

current = A * B 
last = A
power, summed = B, B
while not current == last:
    summed = (power+I) * summed  
    power = power * power
    last = current
    current = A * (summed + I)
  
print(current[0,n-1].total())

