start = 278384
end  = 824795

def has_duplicate(s):
  for i, c in enumerate(s):
    if i == 0:
      continue
    if c == s[i-1]:
      return True
  return False

def has_single_pair_digits(s):
  m = {}
  for digit in s:
    if digit in m:
      m[digit] += 1
    else:
      m[digit] = 1
  return 2 in m.values()

part1 = 0
part2 = 0
for guess in xrange(start + 1, end):
  s = ''.join(sorted(str(guess)))
  if s == str(guess) and has_duplicate(s):
    part1 += 1
    if has_single_pair_digits(s):
      part2 += 1

print 'part1:', part1
print 'part2:', part2
