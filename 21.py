from itertools import cycle, product

p1_start = 4
p2_start = 2

# p1_start = 4
# p2_start = 8


# 1

pos = [p1_start-1, p2_start-1]
score = [0,0]
die = cycle(range(1,101))

win = False
turns = 0
while not win:
    for player in range(2):
        pos[player] = (pos[player] + next(die) + next(die) + next(die))%10
        score[player] += pos[player] + 1
        turns += 1
        if score[player] >= 1000:
            win = True
            break
print(min(score)*turns*3)

# 2

players = range(0)
positions = range(10)
scores = range(30)
dice_results = [(3,1), (4,3), (5,6), (6,7), (7,6), (8,3), (9,1)]

cache = {}

def winning_branches(player, pos1, pos2, score1, score2):
    if (player,pos1,pos2,score1,score2) in cache:
        return cache[(player,pos1,pos2,score1,score2)]
    if score1 >= 21:
         cache[((player,pos1,pos2,score1,score2))] = (1,0)
         return (1,0)
    if score2 >= 21:
        cache[((player,pos1,pos2,score1,score2))] = (0,1)
        return (0,1)
    wins1, wins2 = 0, 0
    for (value, count) in dice_results:
        if player == 0:
            new_pos = (pos1 + value)%10
            new_score = score1 + new_pos + 1
            wins = winning_branches( 1, new_pos , pos2, new_score, score2)
        if player == 1:
            new_pos = (pos2 + value)%10
            new_score = score2 + new_pos + 1
            wins = winning_branches( 0, pos1, new_pos, score1, new_score)
        wins1 += count*wins[0]
        wins2 += count*wins[1]
    cache[(player,pos1,pos2,score1,score2)] = (wins1,wins2)
    return (wins1,wins2)

total_wins = winning_branches(0,p1_start-1, p2_start-1, 0,0)
print(max(total_wins))