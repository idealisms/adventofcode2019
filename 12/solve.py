import re
lines_input = open('input').read().split('\n')

def get_moons_from_input(lines):
  moons = []
  for line in lines:
    m = []
    line = line.rstrip('\r>')
    tokens = line.split(',')
    for token in tokens:
      lhs, rhs = token.split('=')
      m.append(int(rhs))
    moons.append(m)
  return moons

moons = get_moons_from_input(lines_input)
STEPS = 1000

# moons = [
#   [-1, 0, 2],
#   [2, -10, -7],
#   [4, -8, 8],
#   [3, 5, -1],
# ]
# STEPS = 10
vs = [
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0],
  [0, 0, 0]
]
for i in xrange(STEPS):
  for j, m1 in enumerate(moons):
    v = vs[j]
    for m2 in moons:
      if m1 == m2:
        continue
      if m2[0] > m1[0]:
        v[0] += 1
      elif m2[0] < m1[0]:
        v[0] -= 1
      if m2[1] > m1[1]:
        v[1] += 1
      elif m2[1] < m1[1]:
        v[1] -= 1
      if m2[2] > m1[2]:
        v[2] += 1
      elif m2[2] < m1[2]:
        v[2] -= 1
    vs.append(v)
  # Apply velocities
  for m, v in zip(moons, vs):
    m[0] += v[0]
    m[1] += v[1]
    m[2] += v[2]
  # print 'step', i + 1
  # for m, v in zip(moons,vs):
  #   print m, v

energy = 0
for m, v in zip(moons,vs):
  pot = 0
  kin = 0
  for i in range(3):
    pot += abs(m[i])
    kin += abs(v[i])
  energy += pot * kin
print 'part1:', energy

# Each axis is independent.
moons = get_moons_from_input(lines_input)
# moons = [
#   [-8, -10, 0],
#   [5, 5, 10],
#   [2, -7, 3],
#   [9, -8, -3],
# ]

def get_dimension(n):
  dimension = []
  for pos in moons:
    dimension.append(pos[n])
  return dimension

def compute_cycle(dim):
  v = [0] * 4
  seen = set()
  seen.add((tuple(dim), tuple(v)))
  steps = 0
  while True:
    steps += 1
    for i, m1 in enumerate(dim):
      for m2 in dim:
        if m2 > m1:
          v[i] += 1
        elif m2 < m1:
          v[i] -= 1
    # Apply velocities
    for i in range(len(dim)):
      dim[i] += v[i]
    key = (tuple(dim), tuple(v))
    if key in seen:
      print key
      return steps

cycle_lengths = []
for i in range(3):
  dimension = get_dimension(i)
  cycle_length = compute_cycle(dimension)
  print i, cycle_length
  cycle_lengths.append(cycle_length)

# From https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3
from functools import reduce
from fractions import gcd
def lcm(a, b):
    return a * b / gcd(a, b)

def lcms(*numbers):
     return reduce(lcm, numbers)

print 'part2:', lcms(*cycle_lengths)
