with open('1.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]
vals = []
val = 0
for i in input:
    if i == '':
        vals += [val]
        val = 0
    else:
        val += int(i)
vals.sort()
vals.reverse()
print('1: %s' % sum(vals[0:3]))