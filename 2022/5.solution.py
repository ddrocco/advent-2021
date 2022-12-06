import copy

def main():
    with open('5.test_input') as f:
        lines = f.readlines()
    testInput = [line.rstrip() for line in lines]
    impl('test', testInput)
    
    with open('5.input') as f:
        lines = f.readlines()
    input = [line.rstrip() for line in lines]
    impl('real', input)

def impl(case, input):
    #pt1
    stackLines = []
    for line in input:
        if line == '':
            break
        else:
            stackLines.append(line)
    stackLines.reverse()
    stacks = []
    for i in range(1, len(stackLines[1]), 4):
        stacks.append([stackLines[1][i]])
    for j in range(2, len(stackLines)):
        for idx, i in enumerate(range(1, len(stackLines[j]), 4)):
            if stackLines[j][i] == ' ':
                continue
            else:
                stacks[idx].append(stackLines[j][i])
    stacks1 = copy.deepcopy(stacks)
    stacks2 = copy.deepcopy(stacks)
    instructionLines = input[len(stackLines)+1:]
    for inst in instructionLines:
        instWords = inst.split(' ')
        num = int(instWords[1])
        src = int(instWords[3])-1
        dest = int(instWords[5])-1

        # pt1
        movedStack = stacks1[src][-num:]
        movedStack.reverse()
        stacks1[dest].extend(movedStack)
        stacks1[src] = stacks1[src][:-num]

        # pt2
        movedStack = stacks2[src][-num:]
        stacks2[dest].extend(movedStack)
        stacks2[src] = stacks2[src][:-num]
    
    print('%s pt1: %s' % (case, ''.join([stack[-1] for stack in stacks1])))
    print('%s pt2: %s' % (case, ''.join([stack[-1] for stack in stacks2])))

main()