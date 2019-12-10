import fractions

lines = open('input').read().split('\n')
# lines = '''.#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##'''.split('\n')


y_max = len(lines)
x_max = len(lines[0])

asteroids = []
for y, line in enumerate(lines):
  for x, c in enumerate(line):
    if c == '#':
      asteroids.append((x, y))

asteroids_set = set(asteroids)

most = 0
station = None
asteroids_can_see = set()
for ast in asteroids:
  can_see = set()
  #print ast
  for ast2 in asteroids:
    if ast == ast2:
      continue
    #print ' ', ast2
    dx = ast2[0] - ast[0]
    dy = ast2[1] - ast[1]
    gcd = abs(fractions.gcd(dx, dy))
    dx /= gcd
    dy /= gcd
    x, y = ast
    #print '  ', gcd, dx, dy
    while (x, y) != ast2:
      x += dx
      y += dy
      if (x, y) == ast2:
        can_see.add(ast2)
      elif (x, y) in asteroids_set:
        # Another asteroid is in the way.
        break
  print '{} can see {} other asteroids'.format(ast, len(can_see))
  if len(can_see) > most:
    most = max(len(can_see), most)
    station = ast
    asteroids_can_see = can_see
print 'part 1:', most
print 'station location for part 2:', station
# 23:12

def shoot_up(station, asteroids, vaporized):
  y = station[1] - 1
  while y >= 0:
    try:
      ast = (station[0], y)
      asteroids.remove(ast)
      print '{} removed {}'.format(vaporized + 1, ast)
      return vaporized + 1
    except ValueError:
      y -= 1
  return vaporized

def shoot_right(station, asteroids, vaporized):
  possible = []
  for ast in asteroids:
    if ast[0] > station[0]:
      possible.append((float(station[1] - ast[1])/(station[0] - ast[0]), ast))
  possible.sort()
  for _, ast in possible:
    vaporized += 1
    asteroids.remove(ast)
    print '{} removed {}'.format(vaporized, ast)
  return vaporized

def shoot_down(station, asteroids, vaporized):
  y = station[1] + 1
  while y <= y_max:
    try:
      ast = (station[0], y)
      asteroids.remove(ast)
      print '{} removed {}'.format(vaporized + 1, ast)
      return vaporized + 1
    except ValueError:
      y += 1
  return vaporized

def shoot_left(station, asteroids, vaporized):
  possible = []
  for ast in asteroids:
    #print station, ast
    if ast[0] < station[0]:
      possible.append((float(station[1] - ast[1])/(station[0] - ast[0]), ast))
  possible.sort()
  ast200 = None
  for _, ast in possible:
    vaporized += 1
    if vaporized == 200:
      ast200 = ast
    asteroids.remove(ast)
    print '{} removed {}'.format(vaporized, ast)
  return ast200

vaporized = 0
asteroids = list(asteroids_can_see)
vaporized = shoot_up(station, asteroids, vaporized)
vaporized = shoot_right(station, asteroids, vaporized)
vaporized = shoot_down(station, asteroids, vaporized)
ast200 = shoot_left(station, asteroids, vaporized)
print 'asteroids left (should be 0):', len(asteroids)
print 'part2:', ast200[0] * 100 + ast200[1]
# 1:14:18