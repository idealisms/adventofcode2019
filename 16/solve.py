inp_orig = open('input').read()

inp = '12345678'
inp = '80871224585914546619083218645595'
inp = inp_orig
phases = 100

inp = map(int, list(inp))

pattern = [0, 1, 0, -1]

def comp_digit(digits, scale):
  sum = 0
  for i in xrange(size):
    sum += digits[i] * scale[i]
  return abs(sum) % 10

def next_phase(inp):
  size = len(inp)
  out = []
  for digit in xrange(size):
    total = 0
    for i in xrange(size):
      total += inp[i] * pattern[((i + 1) / (digit + 1)) % 4]
    out.append(abs(total) % 10)
  return out

for _ in xrange(phases):
  inp = next_phase(inp)
print 'part1:', ''.join(map(str, inp[:8]))

inp = '03036732577212944063491565474664'
inp = '02935109699940807407585447034323'
inp = inp_orig
offset = int(inp[:7])
inp = map(int, inp) * 10000

def part2(inp, steps, digit_offset):
  digits = []
  base = compute_digit(inp, steps, offset+1)
  for _ in xrange(8):
    digit = 0
    size = len(base)
    for i, v in enumerate(base):
      digit += v * inp[-size+i]
      digit = digit % 10
    digits.append(digit)
    base.pop()
  return ''.join(map(str, digits))

def compute_digit(inp, steps, digit_offset):
  x = len(inp) - digit_offset

  out = [1] * (x + 1)
  for i in xrange(steps - 1):
    next_row = []
    for j, v in enumerate(out):
      next_row.append(v)
      if j > 0:
        next_row[j] += next_row[j-1]
        next_row[j] = next_row[j] % 10
    out = next_row
  return out

print 'part2:', part2(inp, 100, offset)
