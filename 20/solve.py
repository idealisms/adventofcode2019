grid = open('input').read().split('\n')

#grid = open('test').read().split('\n')

# grid = '''                  #
#          A        #
#          A        #
#   #######.#########
#   #######.........#
#   #######.#######.#
#   #######.#######.#
#   #######.#######.#
#   #####  B    ###.#
# BC...##  C    ###.#
#   ##.##       ###.#
#   ##...DE  F  ###.#
#   #####    G  ###.#
#   #########.#####.#
# DE..#######...###.#
#   #.#########.###.#
# FG..#########.....#
#   ###########.#####
#              Z    #
#              Z    #
# '''.split('\n')

warp_name_to_cells = {}
start = []
for r, row in enumerate(grid):
  if r == 0 or r >= len(grid) - 2:
    continue
  for c, char in enumerate(row):
    if c == 0 or c >= len(row) - 1:
      continue
    if not char.isupper():
      continue
    name = None
    if grid[r-1][c] == '.':
      name = char + grid[r+1][c]
      pos = (r-1, c)
    elif grid[r+1][c] == '.':
      name = grid[r-1][c] + char
      pos = (r+1, c)
    elif grid[r][c-1] == '.':
      name = char + grid[r][c+1]
      pos = (r, c-1)
    elif grid[r][c+1] == '.':
      name = grid[r][c-1] + char
      pos = (r, c+1)
    if name:
      if name not in warp_name_to_cells:
        warp_name_to_cells[name] = []
      warp_name_to_cells[name].append(pos)

start = warp_name_to_cells['AA'][0]
end = warp_name_to_cells['ZZ'][0]
warp_mappings = {}
for cells in warp_name_to_cells.values():
  if len(cells) == 1:
    continue
  warp_mappings[cells[0]] = cells[1]
  warp_mappings[cells[1]] = cells[0]

queue = [(start, 0)]
visited = set()
while True:
  pos, steps = queue.pop(0)
  r, c = pos
  if pos == end:
    print 'part1:', steps
    break
  visited.add(pos)
  if grid[r-1][c] == '.' and (r-1, c) not in visited:
    queue.append(((r-1, c), steps + 1))
  if grid[r+1][c] == '.' and (r+1, c) not in visited:
    queue.append(((r+1, c), steps + 1))
  if grid[r][c-1] == '.' and (r, c-1) not in visited:
    queue.append(((r, c-1), steps + 1))
  if grid[r][c+1] == '.' and (r, c+1) not in visited:
    queue.append(((r, c+1), steps + 1))
  if pos in warp_mappings:
    out = warp_mappings[pos]
    if out not in visited:
      queue.append((out, steps+1))

inner = set()
outer = set()
for cells in warp_name_to_cells.values():
  if len(cells) == 1:
    continue
  r, c = cells[0]
  if r < 4 or r > len(grid) - 4 or c < 4 or c > len(grid[0]) - 4:
    outer.add(cells[0])
    inner.add(cells[1])
  else:
    outer.add(cells[1])
    inner.add(cells[0])

queue = [((start[0], start[1], 0), 0)]
end = (end[0], end[1], 0)
visited = set()
while True:
  pos, steps = queue.pop(0)
  r, c, d = pos
  if pos == end:
    print 'part2:', steps
    break
  visited.add(pos)
  if grid[r-1][c] == '.' and (r-1, c, d) not in visited:
    queue.append(((r-1, c, d), steps + 1))
  if grid[r+1][c] == '.' and (r+1, c, d) not in visited:
    queue.append(((r+1, c, d), steps + 1))
  if grid[r][c-1] == '.' and (r, c-1, d) not in visited:
    queue.append(((r, c-1, d), steps + 1))
  if grid[r][c+1] == '.' and (r, c+1, d) not in visited:
    queue.append(((r, c+1, d), steps + 1))
  if (r, c) in warp_mappings:
    out = warp_mappings[(r, c)]
    if (r, c) in inner and (out[0], out[1], d+1) not in visited:
      #print 'warp at {},{} to level {}'.format(r, c, d+1)
      queue.append(((out[0], out[1], d+1), steps+1))
    elif (r, c) in outer and d != 0 and (out[0], out[1], d-1) not in visited:
      queue.append(((out[0], out[1], d-1), steps+1))
      #print 'warp at {},{} to level {}'.format(r, c, d-1)
