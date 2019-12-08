inp = open('input').read()

width = 25
height = 6

layer_size = width * height
num_layers = len(inp) / layer_size
print num_layers, layer_size
layers = []
for i in xrange(num_layers):
  layers.append(inp[i * layer_size:(i+1) * layer_size])

def count_digits(layer, digit):
  cnt = 0
  for d in layer:
    if d == str(digit):
      cnt += 1
  return cnt

fewest_zeros = layer_size
fewest_zeros_layer = -1
for i, layer in enumerate(layers):
  zeros = count_digits(layer, 0)
  print 'layer', i, zeros, len(layer)
  if zeros < fewest_zeros:
    fewest_zeros = zeros
    fewest_zeros_layer = i

print 'part1:', count_digits(layers[fewest_zeros_layer], 1) * count_digits(layers[fewest_zeros_layer], 2)

def pixel_at(layer, r, c):
  return int(layer[r * width + c])

def get_pixel(r, c):
  for layer in layers:
    p = pixel_at(layer, r, c)
    if p != 2:
      return p

print 'part2:'
for r in xrange(height):
  line = []
  for c in xrange(width):
    line.append(get_pixel(r, c))
  print ''.join(map(str, line)).replace('0', ' ')
