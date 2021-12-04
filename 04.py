from tools import read

n = 5 # bingo table size
indices = [(i,j) for i in range(n) for j in range(n)]

def parse_table(table):
    return [[int(x) for x in line.split()] for line in table]

def marking_table():
    return [[ False for i in range(n) ] for j in range(n)]

def check_win(marking_table):
    for i in range(n):
        if sum([marking_table[i][j] for j in range(n)]) == 5:
            return True
    for j in range(n):
        if sum([marking_table[i][j] for i in range(n)]) == 5:
            return True
    return False

def mark(number, table, marking_table):
    for i,j in indices:
        if table[i][j] == number:
            marking_table[i][j] = True

def table_score(table, marking_table):
    return sum([table[i][j] for i,j in indices if not marking_table[i][j]])

# read data

data = read("04.txt")
numbers = [int(x) for x in data[0].split(",")]
tables = [ parse_table(data[i+1:i+n+1]) for i in range(1, len(data), n+1)]
marking_tables = [marking_table() for l in range(len(tables))]

# 1

first_win = False
for number in (x for x in numbers if not first_win):
    for l in range(len(tables)):
        mark(number,tables[l],marking_tables[l])
        if check_win(marking_tables[l]):
            print(table_score(tables[l],marking_tables[l])*number)
            first_win = True

# 2    

wins = [False for l in range(len(tables))]
for number in numbers:
    for l in range(len(tables)):
        mark(number,tables[l],marking_tables[l])
        if check_win(marking_tables[l]) and not wins[l]:
            if sum(wins) == len(wins)-1:
                print(table_score(tables[l],marking_tables[l])*number)
            wins[l] = True

