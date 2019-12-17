import math
inp = open('input').read().split('\n')

# inp = '''9 ORE => 2 A
# 8 ORE => 3 B
# 7 ORE => 5 C
# 3 A, 4 B => 1 AB
# 5 B, 7 C => 1 BC
# 4 C, 1 A => 1 CA
# 2 AB, 3 BC, 4 CA => 1 FUEL'''.split('\n')
# inp = '''157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''.split('\n')
# inp = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
# 17 NVRVD, 3 JNWZP => 8 VPVL
# 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
# 22 VJHF, 37 MNCFX => 5 FWMGM
# 139 ORE => 4 NVRVD
# 144 ORE => 7 JNWZP
# 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
# 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
# 145 ORE => 6 MNCFX
# 1 NVRVD => 8 CXFTF
# 1 VJHF, 6 MNCFX => 4 RFSQX
# 176 ORE => 6 VJHF'''.split('\n')
# inp = '''171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX'''.split('\n')


class Cost(object):
  def __init__(self, out_amount, in_):
    self.out_amount = out_amount
    self.inputs = []
    for token in in_.split(', '):
      amt, sym = token.split(' ')
      self.inputs.append((sym, int(amt)))

graph = {}
for line in inp:
  inputs_str, o = line.split(' => ')
  amt, sym = o.split(' ')
  graph[sym] = Cost(int(amt), inputs_str)

def compute_ore(needs):
  extra = {}

  while not needs.keys() == ['ORE']:
    for item, amount in needs.iteritems():
      if item == 'ORE':
        continue
      del needs[item]
      # First consume extra resources.
      if item in extra:
        if amount <= extra[item]:
          extra[item] -= amount
          break
        amount -= extra[item]
        extra[item] = 0
      # Now produce more.
      cost = graph[item]
      mult = int(math.ceil(amount / float(cost.out_amount)))
      for sym, amt in cost.inputs:
        if sym not in needs:
          needs[sym] = 0
        needs[sym] += amt * mult
      if mult * cost.out_amount > amount:
        if item not in extra:
          extra[item] = 0
        extra[item] += mult * cost.out_amount - amount
      break
  return needs['ORE']
part1 = compute_ore({'FUEL': 1})
print 'part1', part1

target = 1000000000000
def part2(target, lo, hi):
  while lo < hi:
    guess = int((lo + hi) / 2)
    if guess == lo:
      return guess
    ore = compute_ore({'FUEL': guess})
    print ore, guess
    if ore > target:
      hi = guess
    else:
      lo = guess


print 'part2', part2(1000000000000, 0, target / part1 * 2)
