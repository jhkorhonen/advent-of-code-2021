from tools import read

data = read("08.txt")

# parsing

inputs = [[ll.strip().split(" ")  for ll in line.split("|")] for line in data]


# 1

print(len([num for ex,out in inputs for num in out if len(num) in [2,3,4,7] ]))

# 2
#  0000       aaaa  
# 1    2     b    c 
# 1    2     b    c 
#  3333       dddd  
# 4    5     e    f 
# 4    5     e    f 
#  6666       gggg      

total = 0
for ex,out in inputs:
    ex_nums = [ { c for c in num } for num in ex]
    codes = [""]*10
    codes[1] = next((x for x in ex_nums if len(x) == 2), None)
    codes[4] = next((x for x in ex_nums if len(x) == 4), None)
    codes[7] = next((x for x in ex_nums if len(x) == 3), None)
    codes[8] = next((x for x in ex_nums if len(x) == 7), None)
    
    a =  codes[7] - codes[1]
    bd = codes[4] - codes[1]
    eg = codes[8] - a - codes[4]
    
    codes[0] = next((x for x in ex_nums if len(x) == 6 and eg <= x and not bd <= x), None)
    codes[6] = next((x for x in ex_nums if len(x) == 6 and eg <= x and bd <= x), None)
    codes[9] = next((x for x in ex_nums if len(x) == 6 and not eg <= x and bd <= x), None)
    
    codes[2] = next((x for x in ex_nums if len(x) == 5 and eg <= x and not bd <= x), None)
    codes[3] = next((x for x in ex_nums if len(x) == 5 and not eg <= x and not bd <= x), None)
    codes[5] = next((x for x in ex_nums if len(x) == 5 and not eg <= x and bd <= x), None)
    
    codes = ["".join(sorted(list(x))) for x in codes]
    
    total = total + int( "".join([str(c) for c in [codes.index("".join(sorted(o))) for o in out]]) )

print(total)
