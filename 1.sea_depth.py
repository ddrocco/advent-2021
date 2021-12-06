with open('1.input') as f:
    lines = f.readlines()
input = [int(line.strip()) for line in lines]

last_input = input[0]
numIncreases = 0
for elt in input[1:]:
    if elt > last_input:
        numIncreases += 1
    last_input = elt

print('1.1: %s' % numIncreases)

last_input = sum(input[0:3])
numIncreases = 0
# print(len(input)-2)
for i in range(len(input)-1):
    curr_input = sum(input[i:i+3])
    if curr_input > last_input:
        numIncreases += 1
        # print("%s: %s is less than %s; %s" % (i, last_input, curr_input, numIncreases))
    # else:
        # print("%s: %s is greater than %s; %s" % (i, last_input, curr_input, numIncreases))
    last_input = curr_input

print('1.2: %s' % numIncreases)

numIncreases = 0
# print(len(input)-2)
for i in range(len(input)-3):
    if input[i+3] > input[i]:
        numIncreases += 1

print('1.2: %s' % numIncreases)
