from tools import read
from collections import defaultdict, Counter
from itertools import chain

data = read("12.txt")
edges = [ line.split("-") for line in data]
nodes = ["start"] + list({v for edge in edges for v in edge if v not in ["start", "end"]}) + ["end"]
ni = dict( zip(nodes, range(len(nodes))))
n = len(nodes)

# tools

def issmall(node):
    return node[0].islower()
    
# matrices

class mat:
    def __init__(self, values, n, ring):
        self.values = values
        self.n = n
        self.ring = ring

    def __add__(A,B):
        C = mat.zero(A.n, A.ring)
        for i in range(A.n):
            for j in range(A.n):
                C[i,j] = A[i,j] + B[i,j]
        return C

    def __mul__(A,B):
        C = mat.zero(A.n,A.ring)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i,j] += A[i,k] * B[k,j]
        return C

    def __eq__(A,B):
        for i in range(A.n):
            for j in range(A.n):
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
    def zero(cls, n, ring):
        return mat([[ring.zero() for _ in range(n)] for _ in range(n)], n, ring)
    
    @classmethod
    def id(cls, n, ring):
        return mat([[ring.one() if i == j else ring.zero() for i in range(n)] for j in range(n)], n, ring)

    
# polynomial ring with non-constant non-multilinear terms discarded

class multilinear:
    def __init__(self, values):
        # values should be a defaultdict indexed with frozensets
        self.values = values
    
    def __add__(self, other):
        new_values = defaultdict(int)
        for k in chain(self.values.keys(), other.values.keys()):
            if self.values[k] + other.values[k] != 0:
                new_values[k] = self.values[k] + other.values[k]
        return self.__class__(new_values)
    
    def __mul__(self,other):
        # multiply, discard terms that are not multilinear
        new_values = defaultdict(int)
        for s1, v1 in self.values.items():
            for s2, v2 in other.values.items():
                if s1.isdisjoint(s2) and v1*v2 != 0:
                    new_values[frozenset(s1 | s2)] += v1*v2
        return self.__class__(new_values)
    
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
    def constant(cls,x):
        values = defaultdict(int)
        values[frozenset()] = x
        return cls(values)
    
    @classmethod
    def mono(cls,variable,x):
        values = defaultdict(int)
        values[frozenset([variable])] = x
        return cls(values)

    @classmethod
    def zero(cls):
        return cls.constant(0)
    
    @classmethod
    def one(cls):
        return cls.constant(1)


# I don't know what to call this
# polynomial ring but terms with at most degree 2 variable allowed

class onedegreetwo(multilinear):
    def __mul__(self,other):
        new_values = defaultdict(int)
        for s1, v1 in self.values.items():
            for s2, v2 in other.values.items():
                s_new = s1 + s2
                
                if s_new.count("start") >= 2 or s_new.count("end") >= 2 or len(s_new) > len(set(s_new)) + 1:
                   pass
                elif v1*v2 != 0:
                    new_values[tuple(sorted(s_new))] += v1*v2
        return onedegreetwo(new_values)

    def __str__(self):
        if len(self.values)  == 0:
            return "0"
        else:
            return " + ".join([ str(v) + "·" + str(k) for k,v in self.values.items()])
                
    @classmethod
    def constant(cls,x):
        values = defaultdict(int)
        values[tuple()] = x
        return cls(values)
    
    @classmethod
    def mono(cls,variable,x):
        values = defaultdict(int)
        values[tuple([variable])] = x
        return cls(values)
    
# matrix operations

# 1,2

for ring in [multilinear, onedegreetwo]:
    I = mat.id(n, ring)
    A = mat.zero(n, ring)
    A[0,0] = ring.mono("start",1)
    
    B = mat.zero(n, ring)
    for edge in edges:
        v,u = edge
        B[ni[v],ni[u]] = ring.mono(u,1) if issmall(u) else ring.one()
        B[ni[u],ni[v]] = ring.mono(v,1) if issmall(v) else ring.one()
    
    current = A * B 
    last = A
    power, summed = B, B
    i = 0
    while not current == last:
        summed = (power+I) * summed  
        power = power * power
        last = current
        current = A * (summed + I)
      
    print(current[0,n-1].total())

