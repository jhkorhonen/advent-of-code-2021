from tools import read
from math import floor, ceil
from statistics import mean,median

crabs = [ int(x) for x in read("07.txt")[0].split(",")]

def eval(f,z,l):
    return sum( [ f(abs(x - z)) for x in l] )

# 1

print(eval( lambda n: n, round(median(crabs)), crabs))

# 2

# the objective function fits between two with quadratics same leading coefficient and optimum at mean
# one can choose the additive constants suitably to see that the optimum of objective is within +-1 of
# the mean (though I did not write down the full proof, so check details)
lower = eval( lambda n: n * (n+1)/2.0, floor(mean(crabs)), crabs)
upper = eval( lambda n: n * (n+1)/2.0, ceil(mean(crabs)), crabs)
print(round(min(lower,upper)))