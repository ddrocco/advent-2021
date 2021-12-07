with open('7.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

inputArray = [int(inputElt) for inputElt in input[0].split(',')]

minVal = min(inputArray)
maxVal = max(inputArray)

# Part 1
options = []
for i in range(minVal, maxVal+1):
    total = sum([abs(inputElt - i) for inputElt in inputArray])
    print("%s: %s total" % (i, total))
    options.append(total)
print("Minimum: %s" % min(options))

# Part 2
options = []
for i in range(minVal, maxVal+1):
    total = sum([k*(k+1)/2 for k in [abs(inputElt - i) for inputElt in inputArray]])
    print("%s: %s total" % (i, total))
    options.append(total)
print("Minimum: %s" % min(options))

# 1: 1
# 2: 3
# 3: 6
# 4: 10

# x(x+1)/2