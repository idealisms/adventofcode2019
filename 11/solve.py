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
        return -1

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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
pos = (0, 0)
# (int, int) -> int
painted = {}

comp = IntCode(mem_orig)
d = UP
for i in xrange(20000):
  before_color = painted.get(pos, 0)
  painted_color = comp.run(before_color)
  if painted_color == -1:
    break
  painted[pos] = painted_color
  turn = comp.run(None)
  print 'painted {} color {}; turn: {}'.format(pos, painted_color, turn)
  d += 1 if turn == 1 else -1
  d = (d + 4) % 4
  if d == UP:
    pos = (pos[0], pos[1] + 1)
  elif d == DOWN:
    pos = (pos[0], pos[1] - 1)
  elif d == LEFT:
    pos = (pos[0] - 1, pos[1])
  elif d == RIGHT:
    pos = (pos[0] + 1, pos[1])

print 'part1:', len(painted)

comp = IntCode(mem_orig)
pos = (0, 0)
# (int, int) -> int
painted = {pos: 1}

comp = IntCode(mem_orig)
d = UP
for i in xrange(500):
  before_color = painted.get(pos, 0)
  painted_color = comp.run(before_color)
  if painted_color == -1:
    break
  painted[pos] = painted_color
  turn = comp.run(None)
  #print 'painted {} color {}; turn: {}'.format(pos, painted_color, turn)
  d += 1 if turn == 1 else -1
  d = (d + 4) % 4
  if d == UP:
    pos = (pos[0], pos[1] + 1)
  elif d == DOWN:
    pos = (pos[0], pos[1] - 1)
  elif d == LEFT:
    pos = (pos[0] - 1, pos[1])
  elif d == RIGHT:
    pos = (pos[0] + 1, pos[1])

points = []
x_min = 0
x_max = 0
y_min = 0
y_max = 0
for pos, color in painted.iteritems():
  if color == 1:
    points.append(pos)
    x_min = min(x_min, pos[0])
    x_max = max(x_max, pos[0])
    y_min = min(y_min, pos[1])
    y_max = max(y_max, pos[1])

print x_min, x_max
print y_min, y_max
output = [[' '] * 40 for _ in xrange(6)]
for pos in points:
  print pos, pos[1] - y_min, pos[0]
  output[pos[1] - y_min][pos[0]] = 'X'

output.reverse()
print 'part2'
for row in output:
  print ''.join(row)
