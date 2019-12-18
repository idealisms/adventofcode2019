lines = open('input').read().split('\n')

# lines = '''#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################'''.split('\n')
# lines = '''########################
# #@..............ac.GI.b#
# ###d#e#f################
# ###A#B#C################
# ###g#h#i################
# ########################'''.split('\n')

grid = []
for line in lines:
  grid.append([c for c in line])

def get_positions(grid, target):
  positions = []
  for r, line in enumerate(grid):
    for c, char in enumerate(line):
      if char == target:
        positions.append((r, c))
  return positions

def get_all_keys(grid):
  all_keys = set()
  for r, line in enumerate(grid):
    for c, char in enumerate(line):
      if char.islower():
        all_keys.add(char)
  return all_keys

key = ''
start = get_positions(grid, '@')[0]
all_keys = get_all_keys(grid)

def reachable_keys(grid, pos, keys):
  reachable = {} # letter -> (pos, steps)
  queue = [(pos[0], pos[1], 0)]
  visited = set()
  while len(queue):
    r, c, d = queue.pop(0)
    if (r, c) in visited:
      continue
    visited.add((r, c))

    target = grid[r][c]
    # If it's a door and we don't have the key, skip.
    if target.isupper() and target.lower() not in keys:
      continue

    if target.islower() and target not in keys:
      if target not in reachable or d < reachable[target][1]:
        reachable[target] = ((r, c), d)

    if grid[r-1][c] != '#' and (r-1, c) not in visited:
      queue.append((r-1, c, d+1))
    if grid[r+1][c] != '#' and (r+1, c) not in visited:
      queue.append((r+1, c, d+1))
    if grid[r][c-1] != '#' and (r, c-1) not in visited:
      queue.append((r, c-1, d+1))
    if grid[r][c+1] != '#' and (r, c+1) not in visited:
      queue.append((r, c+1, d+1))
  return reachable

def has_all_keys(keys):
  return len(keys) == len(all_keys)

mem = {}
def solve_part1(grid, pos, keys, order):
  if has_all_keys(keys):
    return 0

  m = mem.get((pos, ''.join(keys)))
  if m:
    return m

  print len(keys), order
  next_keys = reachable_keys(grid, pos, keys)

  best = 1000000
  for key in next_keys.keys():
    (r, c), s = next_keys[key]
    new_keys = set(keys)
    new_keys.add(key)
    steps = s + solve_part1(grid, (r, c), new_keys, order + key)
    best = min(best, steps)
  mem[(pos, ''.join(keys))] = best
  return best

part1 = solve_part1(grid, start, set(), '')
print 'part1:', part1
# part1: 4406

# real    4m22.711s
# user    4m17.781s
# sys     0m2.781s

# lines = '''#############
# #DcBa.#.GhKl#
# #.###@#@#I###
# #e#d#####j#k#
# ###C#@#@###J#
# #fEbA.#.FgHi#
# #############'''.split('\n')
# lines = '''#############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############'''.split('\n')
# grid = []
# for line in lines:
#   grid.append([c for c in line])

grid[start[0]-1][start[1]-1] = '@'
grid[start[0]-1][start[1]] = '#'
grid[start[0]-1][start[1]+1] = '@'

grid[start[0]][start[1]-1] = '#'
grid[start[0]][start[1]] = '#'
grid[start[0]][start[1]+1] = '#'

grid[start[0]+1][start[1]-1] = '@'
grid[start[0]+1][start[1]] = '#'
grid[start[0]+1][start[1]+1] = '@'

starts = get_positions(grid, '@')
all_keys = get_all_keys(grid)
mem = {}

def solve_part2(positions, keys, order):
  if has_all_keys(keys):
    return 0

  m = mem.get((tuple(positions), ''.join(keys)))
  if m:
    return m

  print len(keys), order
  next_keys = {}
  for bot, pos in enumerate(positions):
    reachable = reachable_keys(grid, pos, keys)
    for key, info in reachable.iteritems():
      next_keys[key] = [bot] + list(info)

  best = 1000000
  for key in next_keys.keys():
    bot, (r, c), s = next_keys[key]
    new_positions = positions[:]
    new_positions[bot] = (r, c)
    new_keys = set(keys)
    new_keys.add(key)
    steps = s + solve_part2(new_positions, new_keys, order + key)
    best = min(best, steps)
  mem[(tuple(positions), ''.join(keys))] = best
  return best

# part2 = solve_part2(starts, set(), '')
# print 'part2:', part2
# part2: 1964

# real    22m35.105s
# user    22m22.406s
# sys     0m9.344s
# Not the most efficient of solutions.
