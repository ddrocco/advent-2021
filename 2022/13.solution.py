import copy
from itertools import product

def main():
    with open('13.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    # impl('test', testInputs)
    
    with open('13.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    pt1(case, input)

def pt1(case, input):
    sum = 0
    for i, lineIndex in enumerate(range(0, len(input), 3)):
        left = parseAsArrayOfInt(input[lineIndex])
        right = parseAsArrayOfInt(input[lineIndex+1])

        if isCorrect(left, right):
            # print("True: ", i+1)
            sum += i+1

    print('%s pt1: %s' % (case, sum))

def isCorrect(left, right):
    # print("Comparing", left, right)
    if type(left) != type([]):
        # print("Left is converted to array")
        left = [left]
    if type(right) != type([]):
        # print("Right is converted to array")
        right = [right]

    for i, elt in enumerate(left):
        if len(right) <= i:
            # print("Right is out of elts (False)")
            return False
        if type(elt) == type(0) and type(right[i]) == type(0):
            if elt < right[i]:
                # print("Left is smaller (True)", elt, "<", right[i])
                return True
            elif right[i] < elt:
                # print("Left is smaller (False)", elt, ">", right[i])
                return False
            else:
                # print("Vals equal")
                continue
        val = isCorrect(elt, right[i])
        if val is not None:
            return val
        else:
            continue
    if len(left) < len(right):
        # print("Left out of elts, return True")
        return True
    # print("Both out of elts, return None")
    return None

def parseAsArrayOfInt(line):
    # Find arrays
    array = []
    runningIntStr = ""
    currArrayStack = [array]
    for c in line[1:-1]:
        if c == '[':
            newArr = []
            currArrayStack[-1].append(newArr)
            currArrayStack.append(newArr)
        elif c == ']':
            if len(runningIntStr) > 0:
                runningInt = int(runningIntStr)
                currArrayStack[-1].append(runningInt)
                runningIntStr = ""
            currArrayStack.pop(-1)
        elif c == ',':
            if len(runningIntStr) > 0:
                runningInt = int(runningIntStr)
                currArrayStack[-1].append(runningInt)
                runningIntStr = ""
        else:
            runningIntStr += c
    if len(runningIntStr) > 0:
        runningInt = int(runningIntStr)
        currArrayStack[-1].append(runningInt)
        runningIntStr = ""
    return array            


main()