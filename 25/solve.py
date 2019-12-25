import itertools

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
    output = []
    while True:
      opcode, modes = self.get_opcode_and_modes()
      if opcode == 99:
        self.log('Exiting')
        return output

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
        if inp is None or len(inp) == 0:
          #self.log('Waiting for input')
          return output
        addr = self.get_out_addr(1, modes)
        c = inp.pop(0)
        self.mem[addr] = c
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

SHORTHAND = {
  'n': 'north',
  'e': 'east',
  'w': 'west',
  's': 'south',
}

def save():
  f = open('save', 'w')
  f.write(str(ic.ip) + '\n')
  f.write(','.join(map(str, ic.mem)))
  f.close()

def load():
  inp = open('save').read()
  ip, mem = inp.split('\n')
  ic.ip = int(ip)
  ic.mem = map(int, mem.split(','))

items = [
  'tambourine',
  'mutex',
  'dark matter',
  'klein bottle',
  'fuel cell',
  'astrolabe',
  'monolith',
  'cake',
]

def try_combinations():
  for i in xrange(1, len(items)):
    for drop_items in itertools.combinations(items, i):
      load()
      print 'dropping ', str(drop_items)
      for item in drop_items:
        cmd = 'drop {}\n'.format(item)
        out = ic.run(map(ord, cmd))
        #print ''.join(map(chr, out))
      cmd = 'north\n'
      out = ic.run(map(ord, cmd))
      out = ''.join(map(chr, out))
      if 'ejected back to the checkpoint' not in out:
        print out
        print 'passed!'
        return

# Uncomment and run after creating a load state with all the items.
# ic.run(None)
# try_combinations()
# raise Exception
# solution is to DROP ('mutex', 'klein bottle', 'fuel cell', 'cake')

def get_input():
  while True:
    cmd = raw_input()
    cmd = SHORTHAND.get(cmd, cmd)

    if cmd == 'save':
      save()
      print 'saved'
      continue

    if cmd == 'load':
      load()
      print 'loaded'
      continue

    if (cmd not in ('north', 'south', 'east', 'west', 'inv')
        and not cmd.startswith('drop ') and not cmd.startswith('take ')):
      continue
    return map(ord, cmd + '\n')

# Run interactively until we collect all the items (see above)
# and position ourselves in the correct place. Save the state to a file
# so we can quickly try combinations.
inp = None
while True:
  out = ic.run(inp)
  print ''.join(map(chr, out))
  inp = get_input()
