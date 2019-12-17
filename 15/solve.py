mem_orig = map(int, open('input').read().split(','))

class IntCode(object):
  def __init__(self, mem, id=None):
    self.id = id
    self.ip = 0
    self.relative_base = 0
    # guess the size for now
    self.mem = mem[:] + [0] * 1000

  def get_opcode_and_modes(self):
    n = self.mem[self.ip]
    modes = n / 100
    opcode = n % 100
    # Return 3 modes (up to 3 params).
    return opcode, [modes % 10, (modes / 10) % 10, (modes / 100) % 10]

  def read_params(self, num_params, modes):
    params = []
    for offset in xrange(1, num_params + 1):
      p = 0
      mode = modes[offset-1]
      if mode == 0:
        p = self.mem[self.mem[self.ip+offset]]
      elif mode == 1:
        p = self.mem[self.ip+offset]
      elif mode == 2:
        p = self.mem[self.relative_base + self.mem[self.ip+offset]]
        #self.log(' relative base {}, param {}, value {}'.format(self.relative_base, self.mem[self.ip+offset], p))
      else:
        raise Exception('Unknown mode: {}'.format(modes[offset-1]))
      params.append(p)
    return params

  def get_out_addr(self, param, modes):
    addr = self.mem[self.ip+param]
    if modes[param-1] == 2:
      addr += self.relative_base
    elif modes[param-1] != 0:
      raise Exception('Unknown mode for out addr: {}'.format(modes[param-1]))
    return addr

  def log(self, msg):
    out = ''
    if self.id:
      out += '[{}]'.format(self.id)
    print('{} {}'.format(out, msg))

  def run(self, inp):
    while True:
      opcode, modes = self.get_opcode_and_modes()
      if opcode == 99:
        self.log('Exiting')
        return

      #self.log('{} -> {} {}'.format(self.mem[self.ip], opcode, modes))

      if opcode == 1:
        p1, p2 = self.read_params(2, modes)
        addr = self.get_out_addr(3, modes)
        #self.log(' mem[{}] = {} + {}'.format(addr, p1, p2))
        self.mem[addr] = p1 + p2
        self.ip += 4
      elif opcode == 2:
        p1, p2 = self.read_params(2, modes)
        addr = self.get_out_addr(3, modes)
        #self.log(' mem[{}] = {} * {}'.format(addr, p1, p2))
        self.mem[addr] = p1 * p2
        self.ip += 4
      elif opcode == 3:
        if inp is None:
          self.log('Waiting for input')
          return
        addr = self.get_out_addr(1, modes)
        self.mem[addr] = inp
        inp = None
        self.ip += 2
      elif opcode == 4:
        p1, = self.read_params(1, modes)
        #self.log('Output: {}'.format(p1))
        output = p1
        self.ip += 2
        return output
      elif opcode == 5:
        p1, p2 = self.read_params(2, modes)
        #self.log(' ip = {} != 0 ? {} : {}'.format(p1, p2, self.ip+3))
        self.ip = p2 if p1 != 0 else self.ip+3
      elif opcode == 6:
        p1, p2 = self.read_params(2, modes)
        self.ip = p2 if p1 == 0 else self.ip+3
      elif opcode == 7:
        p1, p2 = self.read_params(2, modes)
        addr = self.get_out_addr(3, modes)
        #self.log(' mem[{}] = {} < {}'.format(addr, p1, p2))
        self.mem[addr] = 1 if p1 < p2 else 0
        self.ip += 4
      elif opcode == 8:
        p1, p2 = self.read_params(2, modes)
        addr = self.get_out_addr(3, modes)
        #self.log(' mem[{}] = {} == {}'.format(addr, p1, p2))
        self.mem[addr] = 1 if p1 == p2 else 0
        self.ip += 4
      elif opcode == 9:
        p1, = self.read_params(1, modes)
        #self.log(' adjust relative base by {} to {}'.format(p1, self.relative_base + p1))
        self.relative_base += p1
        self.ip += 2
      else:
        raise Exception('Unexpected opcode: {}'.format(opcode))

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

def explore(ic, droid):
  '''Return -1 if all adjacent spaces have been explored.'''
  if grid[droid[0]-1][droid[1]] == -1:
    #print 'N'
    out = ic.run(NORTH)
    grid[droid[0]-1][droid[1]] = out
    if out != 0:
      droid[0] -= 1
    return out
  if grid[droid[0]+1][droid[1]] == -1:
    #print 'S'
    out = ic.run(SOUTH)
    grid[droid[0]+1][droid[1]] = out
    if out != 0:
      droid[0] += 1
    return out
  if grid[droid[0]][droid[1]-1] == -1:
    #print 'W'
    out = ic.run(WEST)
    grid[droid[0]][droid[1]-1] = out
    if out != 0:
      droid[1] -= 1
    return out
  if grid[droid[0]][droid[1]+1] == -1:
    #print 'E'
    out = ic.run(EAST)
    grid[droid[0]][droid[1]+1] = out
    if out != 0:
      droid[1] += 1
    return out
  return -1

GRID_LETTER = {
  -1: ' ',
  0: '#',
  1: '.',
  2: 'X',
  3: 'D',
}

def draw_grid():
  for row in grid:
    if row.count(-1) != len(row):
      print ''.join([GRID_LETTER[r] for r in row])

def find_unexplored():
  unexplored = []
  for r, row in enumerate(grid):
    for c, col in enumerate(row):
      if col in (1, 2):
        if -1 in (grid[r-1][c], grid[r+1][c], grid[r][c-1], grid[r][c+1]):
          #print '   {} {}: {}, {}, {}, {}'.format((r, c), col, grid[r-1][c], grid[r+1][c], grid[r][c-1], grid[r][c+1])
          unexplored.append((r, c))
  return unexplored

def path(a, b):
  b = tuple(b)
  queue = [(a[0], a[1], [])]
  visited = set()
  while True:
    r, c, p = queue.pop(0)
    if (r, c) == b:
      return p
    visited.add((r, c))
    if grid[r-1][c] in (1, 2) and (r-1, c) not in visited:
      p_ = p[:]
      p_.append(NORTH)
      queue.append((r-1, c, p_))
    if grid[r+1][c] in (1, 2) and (r+1, c) not in visited:
      p_ = p[:]
      p_.append(SOUTH)
      queue.append((r+1, c, p_))
    if grid[r][c-1] in (1, 2) and (r, c-1) not in visited:
      p_ = p[:]
      p_.append(WEST)
      queue.append((r, c-1, p_))
    if grid[r][c+1] in (1, 2) and (r, c+1) not in visited:
      p_ = p[:]
      p_.append(EAST)
      queue.append((r, c+1, p_))

def move_to(ic, droid, target):
  print 'moving from {} to {}'.format(droid, target)
  instructions = path(droid, target)
  #print ' ', instructions
  for i in instructions:
    ret = ic.run(i)
    if ret == 0:
      raise Exception('Unexpected wall')
  droid[0] = target[0]
  droid[1] = target[1]

ic = IntCode(mem_orig)
size = 100
grid = [[-1 for _ in xrange(size)] for __ in xrange(size)]
start = (size/2, size/2)
droid = list(start[:])
grid[droid[0]][droid[1]] = 0
while True:
  ret = explore(ic, droid)
  if ret == 2:
    print 'found!'
  if ret == -1:
    draw_grid()
    print
    unexplored = find_unexplored()
    if len(unexplored) == 0:
      break
    #print droid, unexplored[-1]
    move_to(ic, droid, unexplored[-1])

for r, row in enumerate(grid):
  for c, cell in enumerate(row):
    if cell == 2:
      oxygen = (r, c)
      print 'part1:', len(path(start, (r, c)))
      break

queue = [(oxygen[0], oxygen[1], 0)]
visited = set()
max_time = 0
while True:
  if len(queue) == 0:
    break
  r, c, t = queue.pop(0)
  max_time = max(max_time, t)
  visited.add((r, c))
  if grid[r-1][c] in (1, 2) and (r-1, c) not in visited:
    queue.append((r-1, c, t+1))
  if grid[r+1][c] in (1, 2) and (r+1, c) not in visited:
    queue.append((r+1, c, t+1))
  if grid[r][c-1] in (1, 2) and (r, c-1) not in visited:
    queue.append((r, c-1, t+1))
  if grid[r][c+1] in (1, 2) and (r, c+1) not in visited:
    queue.append((r, c+1, t+1))

print 'part2:', max_time
