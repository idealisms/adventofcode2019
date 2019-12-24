lines = open('input').read().split('\n')

# lines = '''....#
# #..#.
# #..##
# ..#..
# #....'''.split('\n')

# lines = '''.....
# .....
# .....
# #....
# .#...'''.split('\n')

def print_grid(grid):
  for row in grid:
    print ''.join(row)
  print

def part1():
  grid = [[c for c in line] for line in lines]

  def compute_biodiversity(grid):
    i = 0
    total = 0
    for row in grid:
      for c in row:
        if c == '#':
          total += pow(2, i)
        i += 1
    return total

  def next_step(grid):
    new_grid = []
    for r, row in enumerate(grid):
      new_row = []
      for c, char in enumerate(row):
        adj = 0
        if r > 0 and grid[r-1][c] == '#':
          adj += 1
        if r < len(grid) - 1 and grid[r+1][c] == '#':
          adj += 1
        if c > 0 and grid[r][c-1] == '#':
          adj += 1
        if c < len(row) - 1 and grid[r][c+1] == '#':
          adj += 1
        if char == '#':
          if adj == 1:
            new_row.append('#')
          else:
            new_row.append('.')
        else:
          if adj in (1, 2):
            new_row.append('#')
          else:
            new_row.append('.')
      new_grid.append(new_row)
    return new_grid

  seen = set()
  seen.add(compute_biodiversity(grid))
  while True:
    new_grid = next_step(grid)
    score = compute_biodiversity(new_grid)
    #print score
    if score in seen:
      print 'part1:', score
      break
    seen.add(score)
    grid = new_grid

part1()

def part2():
  grids = {}
  grids[0] = [[c for c in line] for line in lines]

  def make_empty_grid():
    return [['.' for c in xrange(5)] for r in xrange(5)]

  def count_adjacent(d, r, c):
    adj = 0
    # up
    if r == 0:
      if d - 1 not in grids:
        grids[d-1] = make_empty_grid()
      adj += 1 if grids[d-1][1][2] == '#' else 0
    elif r == 3 and c == 2:
      if d + 1 not in grids:
        grids[d+1] = make_empty_grid()
      for i in xrange(5):
        adj += 1 if grids[d+1][4][i] == '#' else 0
    else:
      adj += 1 if grids[d][r-1][c] == '#' else 0

    # down
    if r == 4:
      if d - 1 not in grids:
        grids[d-1] = make_empty_grid()
      adj += 1 if grids[d-1][3][2] == '#' else 0
    elif r == 1 and c == 2:
      if d + 1 not in grids:
        grids[d+1] = make_empty_grid()
      for i in xrange(5):
        adj += 1 if grids[d+1][0][i] == '#' else 0
    else:
      adj += 1 if grids[d][r+1][c] == '#' else 0

    # left
    if c == 0:
      if d - 1 not in grids:
        grids[d-1] = make_empty_grid()
      adj += 1 if grids[d-1][2][1] == '#' else 0
    elif c == 3 and r == 2:
      if d + 1 not in grids:
        grids[d+1] = make_empty_grid()
      for i in xrange(5):
        adj += 1 if grids[d+1][i][4] == '#' else 0
    else:
      adj += 1 if grids[d][r][c-1] == '#' else 0

    # right
    if c == 4:
      if d - 1 not in grids:
        grids[d-1] = make_empty_grid()
      adj += 1 if grids[d-1][2][3] == '#' else 0
    elif c == 1 and r == 2:
      if d + 1 not in grids:
        grids[d+1] = make_empty_grid()
      for i in xrange(5):
        adj += 1 if grids[d+1][i][0] == '#' else 0
    else:
      adj += 1 if grids[d][r][c+1] == '#' else 0
    return adj

  def next_step():
    new_grids = {}
    max_depth = max(grids.keys())
    grid = grids[max_depth]
    if '#' in (grid[1][1], grid[1][2], grid[1][3],
               grid[2][1],             grid[2][3],
               grid[3][1], grid[3][2], grid[3][3]):
      grids[max_depth+1] = make_empty_grid()

    min_depth = min(grids.keys())
    grid = grids[min_depth]
    edges = []
    for i in xrange(5):
      edges.append(grid[0][i])
      edges.append(grid[i][0])
      edges.append(grid[4][i])
      edges.append(grid[i][4])
    if '#' in edges:
      grids[min_depth-1] = make_empty_grid()

    for d in list(grids.keys()):
      grid = grids[d]
      if d not in new_grids:
        new_grids[d] = make_empty_grid()
      for r, row in enumerate(grid):
        for c, char in enumerate(row):
          if r == 2 and c == 2:
            continue
          adj = count_adjacent(d, r, c)
          if grids[d][r][c] == '#':
            new_grids[d][r][c] = '#' if adj == 1 else '.'
          else:
            new_grids[d][r][c] = '#' if adj in (1, 2) else '.'
    return new_grids

  def print_grids():
    bugs = 0
    for d in sorted(grids.keys()):
      grid = grids[d]
      print 'Depth {}:'.format(d)
      print_grid(grid)
      for row in grid:
        bugs += row.count('#')
    return bugs

  # print_grids()
  # print '-' * 10
  # print
  # grids = next_step()
  # print_grids()
  # print '-' * 10
  # print
  # grids = next_step()
  # print_grids()

  for _ in xrange(200):
    grids = next_step()
  bugs = print_grids()
  print 'part2:', bugs

part2()
