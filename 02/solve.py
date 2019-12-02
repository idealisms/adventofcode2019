data_orig = map(int, open('input').read().split(','))

def solve(noun, verb):
  data = data_orig[:]
  data[1] = noun
  data[2] = verb
  #data = [1,1,1,4,99,5,6,0,99]
  pos = 0
  while True:
    if data[pos] == 99:
      break
    if data[pos] == 1:
      data[data[pos+3]] = data[data[pos+1]] + data[data[pos+2]]
      pos += 4
    elif data[pos] == 2:
      data[data[pos+3]] = data[data[pos+1]] * data[data[pos+2]]
      pos += 4
    else:
      raise Exception('Unexpected value')
  return data[0]


print 'part1:', solve(12, 2)
part2_output = 19690720
def part2():
  for n in range(100):
    for v in range(100):
      if solve(n, v) == part2_output:
        print 'part2:', n * 100 + v
        return
part2()

