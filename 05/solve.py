mem_orig = map(int, open('input').read().split(','))

def get_opcode_and_modes(n):
  modes = n / 100
  opcode = n % 100
  return opcode, [modes % 10, (modes / 10) % 10, (modes / 100) % 10]

def run(inp):
  ip = 0
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
      mem[mem[ip+1]] = inp
      ip += 2
    elif opcode == 4:
      p1 = mem[mem[ip+1]] if mode[0] == 0 else mem[ip+1]
      print 'ouput:', p1
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
  return mem[0]

print('part1')
mem = mem_orig[:]
run(1)
print
print('part2')
mem = mem_orig[:]
run(5)
