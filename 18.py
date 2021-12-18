from tools import read
from math import floor,ceil

class term:
    def __init__(self, is_pair = False):
        self.is_pair = is_pair
        self.value = -1
        self.children = []
    
    def __add__(self, other):
        new_term = term.make_term([ self.to_list(), other.to_list() ])
        return new_term.reduce_term()

    def __str__(self):
        return str(self.to_list())
    
    def print_term(self,prefix = ""):
        if not self.is_pair:
            print(prefix + str(self))
        else:
            print(prefix + str(self))
            for c in self.children:
                c.print_term(prefix + "-")
    
    def to_list(self):
        if self.is_pair:
            return [child.to_list() for child in self.children]
        else:
            return self.value
    
    def split(self):
        if self.is_pair:
            for i in [0,1]:
                did_split, new_term = self.children[i].split()
                if did_split:
                    if new_term is not None:
                        self.children[i] = new_term
                    return True, None
        else:
            if self.value >= 10:
                return True, term.make_term([floor(self.value/2), ceil(self.value/2)])
        return False, None

    def explode(self,nesting_level):
        if self.is_pair and nesting_level < 4:
            # left subtree
            did_explode, new_term, left_number, right_number = self.children[0].explode(nesting_level+1)
            if did_explode:
                if not new_term is None:
                    self.children[0] = new_term
                if not right_number is None:
                    self.children[1].pass_to_right(right_number)
                    right_number = None
                return True, None, left_number, right_number
            # right subtree
            did_explode, new_term, left_number, right_number = self.children[1].explode(nesting_level+1)
            if did_explode:
                if not new_term is None:
                    self.children[1] = new_term
                if not left_number is None:
                    self.children[0].pass_to_left(left_number)
                    left_number = None
                return True, None, left_number, right_number

        if self.is_pair and nesting_level == 4:
            return True, term.number(0), self.children[0].value, self.children[1].value
            
        return False, None, None, None
     
    def reduce_term(self):
        reduced = True
        while reduced:
            reduced, _, _, _ = self.explode(0)
            if not reduced:
                reduced, _ = self.split()
        return self
        
    def pass_to_left(self,value): # actually goes to the right in the tree
        if self.is_pair:
            self.children[1].pass_to_left(value)
        else:
            self.value += value
            
    def pass_to_right(self,value): # actually goes to the left in the tree
        if self.is_pair:
            self.children[0].pass_to_right(value)
        else:
            self.value += value

    def magnitude(self):
        if self.is_pair:
            return 3*self.children[0].magnitude() + 2*self.children[1].magnitude()
        else:
            return self.value
        
    @classmethod
    def make_term(cls, expr):
        if isinstance(expr, list):
            children = [term.make_term(expr[0]), term.make_term(expr[1])]
            return term.pair(children)
        else:
            new_term = term.number(expr)
        return new_term

    @classmethod
    def number(cls, n):
        new_term = term(False)
        new_term.value = n
        return new_term

    @classmethod
    def pair(cls, children):
        new_term = term(True)
        new_term.children = children
        return new_term


# 1

data = read("18.txt")
terms = [term.make_term(eval(line)) for line in data]

result = terms[0]
for t in terms[1:]:
    result = result + t

print(str(result))
print(result.magnitude())

# 2

max_magnitude = 0
for t1 in terms:
    for t2 in terms:
        if t1 != t2:
            max_magnitude = max(max_magnitude, (t1 + t2).magnitude())

print(max_magnitude)