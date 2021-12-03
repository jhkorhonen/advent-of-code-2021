with open("input.txt") as f:
    bits = [[int(c) for c in line.strip()] for line in f]

#1

b_gamma = [round(sum(l)/len(l)) for l in zip(*bits)]
b_epsilon = [1-x for x in b_gamma]

gamma = int(''.join(str(b) for b in b_gamma),2)
epsilon = int(''.join(str(b) for b in b_epsilon),2)

print(gamma,epsilon,gamma*epsilon)
  
#2  

def ls_rating(cbits,switch):
    if len(cbits) == 1:
        return ''.join(str(b) for b in cbits[0])
    if len(cbits[0]) == 0:
        return ""
    first_bits = [b[0] for b in cbits]
    first_bit = 1-switch if 2*sum(first_bits) >= len(first_bits) else switch
    
    new_bits = [b[1:] for b in cbits if b[0] == first_bit]
    return str(first_bit) + ls_rating(new_bits,switch)
    
oxygen_bits = ls_rating(bits,0)
co2_bits = ls_rating(bits,1)

print(oxygen_bits,co2_bits)

print(int(oxygen_bits,2)*int(co2_bits,2))