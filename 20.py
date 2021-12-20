from tools import read
from collections import defaultdict

class image:
    def __init__(self,im, lx,ly,default):
        self.im = im
        self.lx = lx
        self.ly = ly
        self.default = default

def b_to_int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out
    
def apply_iea(iea, bits):
    return iea[b_to_int(bits)]

def update(im,iea):
    lx, ly = im.lx + 2, im.ly + 2
    default = iea[0] - im.default
    new_im = defaultdict(lambda:default)
    for x in range(lx):
        for y in range(ly):
            new_im[(x,y)] = apply_iea(iea, [im.im[(x+dx-1,y+dy-1)] for dy in [-1,0,1] for dx in [-1,0,1] ] )
    return image(new_im,lx,ly, default)

def repeat_update(im,iea,n):
    for _ in range(n):
        im = update(im,iea)
    return im

def print_image(im):
    for y in range(im.ly):
        print("".join("." if im.im[(x,y)] == 0 else "#" for x in range(im.lx)))


# parsing

data = read("20.input.txt")
iea, data = [0 if p == "." else 1 for p in data[0]] , data[2:]
im_bits = defaultdict(int)
for x in range(len(data[0])):
    for y in range(len(data)):
        im_bits[(x,y)] = 1 if data[y][x] == "#" else 0
orig_im = image(im_bits,len(data[0]),len(data),0)

# 1
im = repeat_update(orig_im,iea,2)
print(sum(x for x in im.im.values()), im.lx, im.ly)

# 2
im = repeat_update(orig_im,iea,50)
print(sum(x for x in im.im.values()), im.lx, im.ly)