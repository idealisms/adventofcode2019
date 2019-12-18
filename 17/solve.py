mem_orig = map(int, open('input').read().split(','))

class IntCode(object):
  def __init__(self, mem, id=None):
    self.id = id
    self.ip = 0
    self.relative_base = 0
    # guess the size for now
    self.mem = mem[:] + [0] * 3000

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
    output = []
    while True:
      opcode, modes = self.get_opcode_and_modes()
      if opcode == 99:
        self.log('Exiting')
        if output[-1] > 255:
          return output[-1]
        return ''.join(map(chr, output))

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
        output.append(p1)
        self.ip += 2
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
view = ic.run(None)
lines = view.split('\n')
total = 0
bot = []
for r in xrange(1, len(lines) - 1):
  line = lines[r]
  for c in xrange(1, len(line) - 1):
    if (line[c] == '#' and line[c-1] == '#' and line[c+1] == '#'
        and lines[r-1][c] == '#' and lines[r+1][c] == '#'):
      total += r * c
    if line[c] == '^':
      bot = [r, c]
print 'part1:', total

# Compute path - I just manually found the path and split it into 3 functions.
#B R,6,L,10,R,8,
#A R,8,R,12,L,8,L,8,
#B R,6,L,10,R,8,
#A R,8,R,12,L,8,L,8,
#C L,10,R,6,R,6,L,8,
#B R,6,L,10,R,8,
#A R,8,R,12,L,8,L,8,
#C L,10,R,6,R,6,L,8,
#B R,6,L,10,R,8,
#C L,10,R,6,R,6,L,8

main = 'B,A,B,A,C,B,A,C,B,C\n'
funcs = [
  'R,8,R,12,L,8,L,8\n',
  'R,6,L,10,R,8\n',
  'L,10,R,6,R,6,L,8\n',
]

def feed_input(ic, s):
  inputs = map(ord, s)
  for inp in inputs:
    out = ic.run(inp)
    if out:
      print 'part2:', out

ic = IntCode(mem_orig[:])
ic.mem[0] = 2
feed_input(ic, main)
for func in funcs:
  feed_input(ic, func)
feed_input(ic, 'n\n')
