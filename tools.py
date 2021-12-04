

def read(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

