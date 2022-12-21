from util.set import set
import re

TEST_PT_1 = True
PROD_PT_1 = False
TEST_PT_2 = False
PROD_PT_2 = False

Q_NUM = 20

def main():
    with open('%s.test_input' % Q_NUM) as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs, TEST_PT_1, TEST_PT_2)
    
    with open('%s.input' % Q_NUM) as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs, PROD_PT_1, PROD_PT_2)

def impl(case, input, doPt1, doPt2):
    if doPt1:
        pt1(case, input)
    if doPt2:
        pt2(case, input)

def pt1(case, input):
    numsInOrder = [int(elt) for elt in input]
    dynamicNums = [int(elt) for elt in input] # Deep copy
    print(dynamicNums)
    for i, num in enumerate(numsInOrder):
        dynamicNums.append(None)
        index = dynamicNums.index(num)
        newIndexBase = index+num
        newIndex = newIndexBase % len(numsInOrder)
        if num == 4:
            print(newIndex, index+num, (index+num) % len(numsInOrder), len(numsInOrder))
        dynamicNums[index] = None
        dynamicNums.insert(newIndex, num)
        dynamicNums.remove(None)
        dynamicNums.remove(None)
        print("%d:\t %s" % (num, dynamicNums))
    res = 1
    print('%s pt1: %s' % (case, res))

def pt2(case, input):
    res = 1
    print('%s pt2: %s' % (case, res))

main()