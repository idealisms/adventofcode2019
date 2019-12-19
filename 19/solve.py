import math
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
          #self.log('Waiting for input')
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

count = 0
grid = []
for y in xrange(50):
  row = []
  for x in xrange(50):
    ic = IntCode(mem_orig)
    ic.run(x)
    out = ic.run(y)
    row.append(out)
    count += out
  grid.append(row)
print 'part1', count

for row in grid:
  print ''.join(map(str, row))

rows = [None] * 5000
rows[9] = (8, 8)
rows[49] = (43, 47)
rows[836] = (734, 812)

def guess_range(y):
  # These constants were found by taking the slope between rows 9 and 836.
  # The rows were found by brute force scanning to 1000x1000 (and me picking
  # randomly).
  return (int(float(y) / 1.14), int(float(y) / 1.03))

def find_range(y, guess_x_start, guess_x_end):
  max_x = 100000
  x_min = max_x
  x_max = -1
  x = guess_x_start
  while True:
    ic = IntCode(mem_orig)
    ic.run(x)
    out = ic.run(y)
    #print 'try {},{} -> {}'.format(x, y, out)
    if out == 1 and x_min == max_x:
      x_min = x
      x = guess_x_end
      #print ' x_min', x
    if x_min != max_x and x_max == -1:
      if out == 0:
        raise Exception('Should have found beam')
      else:
        x_max = x
    elif x_min != max_x and out == 1:
      x_max = x

    if out == 0 and x_min != max_x:
      print 'rows[{}] = ({}, {})'.format(y, x_min, x_max)
      return (x_min, x_max)
    x += 1

for y in range(1980, 2020):
  x_start, x_end = guess_range(y)
  r = find_range(y, x_start, x_end)
  rows[y] = r
for y in range(2080, 2120):
  x_start, x_end = guess_range(y)
  r = find_range(y, x_start, x_end)
  rows[y] = r

for y in range(2080, 2120):
  if rows[y-99][1] - rows[y][0] >= 99:
    ans = 10000 * (rows[y-99][1]-99) + y-99
    print 'part2 (x={},y={}): {}'.format(rows[y-99][1]-99, y-99, ans)
    break
# 18552014 is too high
# 18482006 is too high
# 18261982
