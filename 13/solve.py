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
    #if addr == 2372:
    #  print ' out addr 2372'
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
        return -2

      #self.log('{}: {} -> {} {}'.format(self.ip, self.mem[self.ip], opcode, modes))

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
          #self.log('Waiting for input')
          return -3
        addr = self.get_out_addr(1, modes)
        self.mem[addr] = inp
        inp = None
        self.ip += 2
      elif opcode == 4:
        p1, = self.read_params(1, modes)
        #self.log('Output: {}'.format(p1))
        self.ip += 2
        output = p1
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

ic = IntCode(mem_orig)
tiles = {}
blocks = 0
while True:
  left = ic.run(None)
  if left == -2:
    # exit
    break
  elif left == -3:
    # input
    break
  top = ic.run(None)
  tile = ic.run(None)
  tiles[(left, top)] = tile
  if tile == 2:
    blocks += 1
print 'part1', blocks

print
scores = []

board = [[' ' for x in xrange(36)] for y in xrange(24)]
def draw_board(ic, board, inp):
  for row in board:
    for i, c in enumerate(row):
      if c == 'o':
        row[i] = ' '

  x = None
  while True:
    x = ic.run(inp)
    inp = None
    if x == -2:
      return -2
    if x == -3:
      return -3
    y = ic.run(None)
    tile = ic.run(None)
    if x == -1 and y == 0:
      scores.append(tile)
      for row in board:
        print ''.join(row)
      print 'score:', scores
      print

    elif x == -1:
      print 'unknown command', x, y, tile
    else:
      if tile != 0:
        c = ' '
        if tile == 1:
          c = 'W'
        elif tile == 2:
          c = 'B'
        elif tile == 3:
          c = '-'
        elif tile == 4:
          c = 'o'
        board[y][x] = c
  raise Exception('Unknown state: {}'.format(x))

mem_orig[0] = 2
ic = IntCode(mem_orig)
ret = draw_board(ic, board, None)
# This is the row with the paddle. After we initialized the board,
# fill it with walls so we can't lose.
print ic.mem[1431:1467]
for i, c in enumerate(ic.mem[1431:1467]):
  if c == 0:
    ic.mem[1431 + i] = 1

# Play the game
while True:
  if ret == -2:
    break
  elif ret == -3:
    ret = draw_board(ic, board, 0)
  else:
    raise Exception('Unknown ret: {}'.format(ret))

print 'part2:', scores[-1]
