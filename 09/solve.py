mem_orig = map(int, open('input').read().split(','))

class Amplifier(object):
  def __init__(self, phase, mem):
    self.phase = phase
    self.ip = 0
    self.relative_base = 0
    # guess the size for now
    self.mem = mem[:] + [0] * 1000
    self.run(phase)

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
        print 'relative base', self.relative_base, 'param', self.mem[self.ip+offset], 'value', p
      else:
        raise Exception('Unknown mode: {}'.format(modes[offset-1]))
      params.append(p)
    return params

  def run(self, inp):
    while True:
      opcode, modes = self.get_opcode_and_modes()
      if opcode == 99:
        print '[Phase {}] Exiting'.format(self.phase)
        raise StopIteration()

      print self.mem[self.ip], opcode, modes

      if opcode == 1:
        p1, p2 = self.read_params(2, modes)
        print 'mem[{}] = {} + {}'.format(self.mem[self.ip+3], p1, p2)
        addr = self.mem[self.ip+3]
        if modes[2] == 2:
          addr += self.relative_base
        self.mem[addr] = p1 + p2
        self.ip += 4
      elif opcode == 2:
        p1, p2 = self.read_params(2, modes)
        print 'mem[{}] = {} * {}'.format(self.mem[self.ip+3], p1, p2)
        addr = self.mem[self.ip+3]
        if modes[2] == 2:
          addr += self.relative_base
        self.mem[addr] = p1 * p2
        self.ip += 4
      elif opcode == 3:
        if inp is None:
          print '[Phase {}] Waiting for input'.format(self.phase)
          return
        addr = self.mem[self.ip+1]
        if modes[0] == 2:
          addr += self.relative_base
        self.mem[addr] = inp
        inp = None
        self.ip += 2
      elif opcode == 4:
        p1, = self.read_params(1, modes)
        print '[Phase {}] Output:'.format(self.phase), p1
        output = p1
        self.ip += 2
        #return output
      elif opcode == 5:
        p1, p2 = self.read_params(2, modes)
        print 'ip = {} != 0 ? {} : {}'.format(p1, p2, self.ip+3)
        self.ip = p2 if p1 != 0 else self.ip+3
      elif opcode == 6:
        p1, p2 = self.read_params(2, modes)
        self.ip = p2 if p1 == 0 else self.ip+3
      elif opcode == 7:
        p1, p2 = self.read_params(2, modes)
        addr = self.mem[self.ip+3]
        if modes[2] == 2:
          addr += self.relative_base
        print 'mem[{}] = {} < {}'.format(addr, p1, p2)
        self.mem[addr] = 1 if p1 < p2 else 0
        self.ip += 4
      elif opcode == 8:
        p1, p2 = self.read_params(2, modes)
        addr = self.mem[self.ip+3]
        if modes[2] == 2:
          addr += self.relative_base
        print 'mem[{}] = {} == {}'.format(addr, p1, p2)
        self.mem[addr] = 1 if p1 == p2 else 0
        self.ip += 4
      elif opcode == 9:
        p1, = self.read_params(1, modes)
        print 'adjust relative base by', p1, 'to', self.relative_base + p1
        self.relative_base += p1
        self.ip += 2
      else:
        raise Exception('Unexpected opcode: {}'.format(opcode))

#mem_orig = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#mem_orig = [1102,34915192,34915192,7,4,7,99,0]
#mem_orig = [104,1125899906842624,99]
try:
  print 'part1'
  a = Amplifier(1, mem_orig)
except StopIteration:
  pass

try:
  print 'part2'
  a = Amplifier(2, mem_orig)
except StopIteration:
  pass

