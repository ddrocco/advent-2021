import math
import copy

with open('3.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

bitCount = len(input[0])

zeroFrequencies = [0] * bitCount
oneFrequencies = [0] * bitCount
for line in input:
    for i, bit in enumerate(line):
        if bit == '0':
            zeroFrequencies[i] += 1
        elif bit == '1':
            oneFrequencies[i] += 1

gamma = [None] * bitCount
epsilon = [None] * bitCount
for i in range(bitCount):
    if zeroFrequencies[i] > oneFrequencies[i]:
        gamma[i] = 0
        epsilon[i] = 1
    else:
        gamma[i] = 1
        epsilon[i] = 0

binGamma = 0
binEpsilon = 0
bitRangeReversed = range(bitCount)
bitRangeReversed.reverse()
for i, j in enumerate(bitRangeReversed):
    binGamma += gamma[i] * math.pow(2, j)
    binEpsilon += epsilon[i] * math.pow(2, j)

print(binGamma * binEpsilon)

oxyNumbers = copy.copy(input)
co2Numbers = copy.copy(input)
for i in range(bitCount):
    if len(oxyNumbers) > 1:
        # oxy
        numOnes = sum([1 for num in oxyNumbers if num[i] == '1'])
        numZeroes = sum([1 for num in oxyNumbers if num[i] == '0'])
        if numOnes >= numZeroes:
            oxyNumbers = [num for num in oxyNumbers if num[i] == '1']
        else:
            oxyNumbers = [num for num in oxyNumbers if num[i] == '0']
    if len(co2Numbers) > 1:
        # co2
        numOnes = sum([1 for num in co2Numbers if num[i] == '1'])
        numZeroes = sum([1 for num in co2Numbers if num[i] == '0'])
        if numZeroes <= numOnes:
            co2Numbers = [num for num in co2Numbers if num[i] == '0']
        else:
            co2Numbers = [num for num in co2Numbers if num[i] == '1']
if len(oxyNumbers) == 1 and len(co2Numbers) == 1:
    print("Success")
    oxyNumber = oxyNumbers[0]
    co2Number = co2Numbers[0]
    oxyTotal = 0
    co2Total = 0
    for i, j in enumerate(bitRangeReversed):
        oxyTotal += int(oxyNumber[i]) * math.pow(2, j)
        co2Total += int(co2Number[i]) * math.pow(2, j)
    print(oxyTotal * co2Total)
else:
    print(oxyNumbers, co2Numbers)