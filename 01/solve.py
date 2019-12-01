inp = open('input').read()
s = 0

m = {}
def fuel(n):
  if n in m:
    return m[n]
  f = n / 3 - 2
  if f <= 0:
    return 0
  m[n] = f + fuel(f)
  return m[n]

for v in inp.split('\n'):
  if v:
    s += fuel(int(v))
print s
