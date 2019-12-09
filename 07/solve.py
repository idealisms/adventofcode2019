import itertools

mem_orig = map(int, open('input').read().split(','))

def get_opcode_and_modes(n):
  modes = n / 100
  opcode = n % 100
  return opcode, [modes % 10, (modes / 10) % 10, (modes / 100) % 10]

def run(inputs):
  ip = 0
  inp = 0
  output = None
  while True:
    opcode, mode = get_opcode_and_modes(mem[ip])
    if opcode == 99:
      break

    #print mem[ip], opcode, mode

    if opcode == 1:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      mem[mem[ip+3]] = p1 + p2
      # print ' ', p1, p2
      ip += 4
    elif opcode == 2:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      mem[mem[ip+3]] = p1 * p2
      ip += 4
    elif opcode == 3:
      mem[mem[ip+1]] = inputs[inp]
      inp += 1
      ip += 2
    elif opcode == 4:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      print 'ouput:', p1
      output = p1
      ip += 2
    elif opcode == 5:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      if p1 != 0:
        ip = p2
      else:
        ip += 3
    elif opcode == 6:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      if p1 == 0:
        ip = p2
      else:
        ip += 3
    elif opcode == 7:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      mem[mem[ip+3]] = 1 if p1 < p2 else 0
      ip += 4
    elif opcode == 8:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      p2 = mem[mem[ip+2]] if mode[1] == 0 else mem[ip+2]
      mem[mem[ip+3]] = 1 if p1 == p2 else 0
      ip += 4
    else:
      print opcode
      raise Exception('Unexpected value')
  return output

signal = 0
for order in itertools.permutations(range(5)):
  output = 0
  for amp in order:
    mem = mem_orig[:]
    output = run([amp, output])
  signal = max(signal, output)
print 'part1', signal
print

class Amplifier(object):
  def __init__(self, phase, mem):
    self.phase = phase
    self.ip = 0
    self.mem = mem[:]
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
      params.append(self.mem[self.mem[self.ip+offset]] if modes[offset-1] == 0
                    else self.mem[self.ip+offset])
    return params

  def run(self, inp):
    while True:
      opcode, modes = self.get_opcode_and_modes()
      if opcode == 99:
        print '[Phase {}] Exiting'.format(self.phase)
        raise StopIteration()

      #print self.mem[self.ip], opcode, modes

      if opcode == 1:
        p1, p2 = self.read_params(2, modes)
        self.mem[self.mem[self.ip+3]] = p1 + p2
        self.ip += 4
      elif opcode == 2:
        p1, p2 = self.read_params(2, modes)
        self.mem[self.mem[self.ip+3]] = p1 * p2
        self.ip += 4
      elif opcode == 3:
        if inp is None:
          print '[Phase {}] Waiting for input'.format(self.phase)
          return
        self.mem[self.mem[self.ip+1]] = inp
        inp = None
        self.ip += 2
      elif opcode == 4:
        p1, = self.read_params(1, modes)
        print '[Phase {}] Output:'.format(self.phase), p1
        output = p1
        self.ip += 2
        return output
      elif opcode == 5:
        p1, p2 = self.read_params(2, modes)
        self.ip = p2 if p1 != 0 else 3
      elif opcode == 6:
        p1, p2 = self.read_params(2, modes)
        self.ip = p2 if p1 == 0 else 3
      elif opcode == 7:
        p1, p2 = self.read_params(2, modes)
        self.mem[self.mem[self.ip+3]] = 1 if p1 < p2 else 0
        self.ip += 4
      elif opcode == 8:
        p1, p2 = self.read_params(2, modes)
        self.mem[self.mem[self.ip+3]] = 1 if p1 == p2 else 0
        self.ip += 4
      else:
        raise Exception('Unexpected opcode: {}'.format(opcode))


#mem_orig = map(int, '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'.split(','))
#mem_orig = map(int, '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'.split(','))
best = 0
for order in itertools.permutations(range(5, 10)):
  mem = mem_orig[:]
  a = Amplifier(order[0], mem_orig)
  b = Amplifier(order[1], mem_orig)
  c = Amplifier(order[2], mem_orig)
  d = Amplifier(order[3], mem_orig)
  e = Amplifier(order[4], mem_orig)
  output = 0
  print order
  try:
    for i in range(10000):
      output = a.run(output)
      output = b.run(output)
      output = c.run(output)
      output = d.run(output)
      output = e.run(output)
  except StopIteration:
    print 'stopped'
  best = max(best, output)

print 'part2', best
