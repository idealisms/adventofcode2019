# I ended up looking up the answer to part 2 on r/adventofcode.
# I was able to figure out how to reverse the operations (without
# using modinv!), but wasn't familiar how to apply it N times.
# I thought maybe it would cycle faster, but after 20mil cycles,
# I realized that it wouldn't (and looked up the solution.)

commands = open('input').read().split('\n')

CUT = 'cut '
DEAL_WITH_INC = 'deal with increment '

# commands = '''deal with increment 7
# deal into new stack
# deal into new stack'''.split('\n')
# commands = '''cut 6
# deal with increment 7
# deal into new stack'''.split('\n')
# commands = '''deal with increment 7
# deal with increment 9
# cut -2'''.split('\n')
# commands = '''deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1'''.split('\n')

cards = 10007
# cards = 10
CMD_DEAL_NEW = 0
CMD_CUT = 1
CMD_DEAL_WITH = 2

cmds = []
for command in commands:
  if command == 'deal into new stack':
    cmds.append([CMD_DEAL_NEW])
  elif command.startswith(CUT):
    cut_depth = int(command[len(CUT):])
    cmds.append([CMD_CUT, cut_depth])
  elif command.startswith(DEAL_WITH_INC):
    inc = int(command[len(DEAL_WITH_INC):])
    cmds.append([CMD_DEAL_WITH, inc])

deck = range(cards)

positions = []
def shuffle(deck, cards):
  for c, cmd in enumerate(cmds):
    #print c, command
    if cmd[0] == CMD_DEAL_NEW:
      deck.reverse()
    elif cmd[0] == CMD_CUT:
      cut_depth = cmd[1]
      deck = deck[cut_depth:] + deck[:cut_depth]
    elif cmd[0] == CMD_DEAL_WITH:
      inc = cmd[1]
      #print '  ', inc
      new_deck = [-1] * cards
      pos = 0
      for i in xrange(cards):
        new_deck[pos] = deck[i]
        pos += inc
        pos = pos % cards
      deck = new_deck
    else:
      raise Exception('unknown command: {}'.format(cmd))
    positions.append(deck.index(2019))
  return deck

deck = shuffle(deck, cards)
print 'part1: {}'.format(deck.index(2019))
# 3074

cmds.reverse()
def track_card_back(cards, position):
  for cmd in cmds:
    if cmd[0] == CMD_DEAL_NEW:
      position = cards - position - 1
    elif cmd[0] == CMD_CUT:
      cut_depth = cmd[1]
      position += cut_depth
      if position < 0:
        position += cards
      position = position % cards
    elif cmd[0] == CMD_DEAL_WITH:
      # I didn't know about mod inv before doing this problem. This was a way to compute
      # it with a small mod value.
      inc = cmd[1]
      offsets = inc_cycle(cards, inc)
      mult = offsets.index(position % inc)
      position = cards * mult + position
      position = position / inc
    # print position,
  return position

cycles = {}
def inc_cycle(cards, inc):
  if inc in cycles:
    return cycles[inc]
  offsets = [0]
  for i in xrange(inc - 1):
    offsets.append(inc - ((cards - offsets[i]) % inc))
  cycles[inc] = offsets
  return offsets

# This should be 2019 (verifies that track_card_back works).
# print track_card_back(cards, 3074)

cards = 119315717514047
shuffles = 101741582076661

# From https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# Using the explanation from u/etotheipi1:
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/
D = cards
X = 2020
Y = track_card_back(cards, X)
Z = track_card_back(cards, Y)
A = (Y-Z) * modinv(X-Y+D, D) % D
B = (Y-A*X) % D

n = shuffles
print 'part2:', (pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D
