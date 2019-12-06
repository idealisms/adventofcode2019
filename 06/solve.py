lines = open('input').read().split('\n')

m = {}
for line in lines:
  left, right = line.split(')')
  m[right] = left

def count_orbits(obj):
  cnt = 0
  while obj in m:
    cnt += 1
    obj = m[obj]
  return cnt

orbits = 0
for obj in m.keys():
  orbits += count_orbits(obj)
print 'part1:', orbits
# 6:14

def get_orbits(obj):
  orbits = []
  while obj in m:
    orbits.append(m[obj])
    obj = m[obj]
  return orbits

you_orbits = get_orbits('YOU')
san_orbits = get_orbits('SAN')
shortest = 1000
for i, orbit in enumerate(you_orbits):
  if orbit in san_orbits:
    shortest = min(shortest, i + san_orbits.index(orbit))
print 'part2:', shortest
# 12:54