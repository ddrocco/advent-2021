import copy

def main():
    with open('6.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    for i, testInput in enumerate(testInputs):
        impl('test %s' % i, testInput)
        pass
    
    with open('6.input') as f:
        lines = f.readlines()
    input = [line.rstrip() for line in lines]
    impl('real', input[0])

def impl(case, input):
    val1 = pt1(input)
    val2 = pt2(input)
    
    print('%s pt1: %s' % (case, val1))
    print('%s pt2: %s' % (case, val2))

def pt1(input):
    runningStr = [' '] * 4
    for i, c in enumerate(input):
        runningStr = runningStr[1:]
        runningStr.append(c)
        if ' ' not in runningStr:
            if numUnique(runningStr) == 4:
                return i+1
    return -1

def pt2(input):
    runningStr = [' '] * 14
    for i, c in enumerate(input):
        runningStr = runningStr[1:]
        runningStr.append(c)
        if ' ' not in runningStr:
            if numUnique(runningStr) == 14:
                return i+1
    return -1

def numUnique(chars):
    d = {}
    for c in chars:
        d[c] = 1
    return len(d)

main()