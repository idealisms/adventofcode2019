wire1, wire2 = open('input').read().split('\n')

wire1_parts = wire1.split(',')
wire2_parts = wire2.split(',')

def map_wire(parts):
  positions = []
  x = 0
  y = 0
  for part in parts:
    d = part[0]
    dist = int(part[1:])

    if d == 'U':
      for i in xrange(dist):
        positions.append((x, y+i+1))
      y += dist
    elif d == 'D':
      for i in xrange(dist):
        positions.append((x, y-i-1))
      y -= dist
    elif d == 'R':
      for i in xrange(dist):
        positions.append((x+i+1, y))
      x += dist
    elif d == 'L':
      for i in xrange(dist):
        positions.append((x-i-1, y))
      x -= dist
    else:
      raise Exception('Unexpected rule')
  return positions

wire1_positions = map_wire(wire1_parts)
wire2_positions = map_wire(wire2_parts)
wire2_positions_set = set(wire2_positions)
print len(wire1_positions), len(wire2_positions)

closest = 100000
for pos in wire1_positions:
  if pos in wire2_positions_set:
    closest = min(closest, abs(pos[0]) + abs(pos[1]))
print 'part1:', closest
# 12:28

closest = 1000000
for d, pos in enumerate(wire1_positions):
  if pos[0] == 0 and pos[1] == 0:
    continue
  if pos in wire2_positions_set:
    closest = min(closest, d+1 + wire2_positions.index(pos)+1)
print 'part2:', closest
# 20:10
