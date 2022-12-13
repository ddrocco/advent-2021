import copy
from itertools import product

def main():
    with open('11.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    # impl('test', testInputs)
    
    with open('11.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    pt1(case, input, worryDivision=3, rounds=20, pt=1)
    pt1(case, input, worryDivision=1, rounds=10000, pt=2)

def pt1(case, input, worryDivision=3, rounds=20, pt=1):
    monkeys = {}
    divisors = []
    divisorProd = 1
    for mIndex in range(0, len(input), 7):
        id = int(input[mIndex][7])
        items = [int(val) for val in input[mIndex+1][len('  Starting items: '):].split(', ')]
        operation = input[mIndex+2][len('  Operation: new = '):]
        testCond = int(input[mIndex+3][len('  Test: '):].split(' ')[2])
        trueId = input[mIndex+4][-1]
        falseId = input[mIndex+5][-1]

        divisors.append(testCond)
        monkeys[id] = Monkey(id, items, operation, testCond, trueId, falseId)
    
    for divisor in divisors:
        divisorProd *= divisor
    for i in range(rounds):
        if i % 5 == 0:
            print(i)
        for mId in range(len(monkeys)):
            monkeys[mId].act(worryDivision, monkeys, divisorProd)
    mBusinessVals = []
    for mId in range(len(monkeys)):
        mBusinessVals.append(monkeys[mId].inspections)
        # print(mId, monkeys[mId].items)
    print(mBusinessVals)
    maxVal = max(mBusinessVals)
    mBusinessVals.remove(maxVal)
    secondaryMaxVal = max(mBusinessVals)

    print('%s pt%s: %s' % (case, pt, maxVal * secondaryMaxVal))


class Monkey(object):
    def __init__(self, id, items, operation, testCond, trueId, falseId):
        self.id = id
        self.items = items
        self.operation = operation.split(" ")
        self.testCond = testCond
        self.trueId = int(trueId)
        self.falseId = int(falseId)
        self.inspections = 0

    def act(self, worryDivision, monkeys, divisorProd):
        for item in self.items:
            self.inspections += 1
            newItemVal = self.op(item)//worryDivision
            newItemVal %= divisorProd
            cond = self.condition(newItemVal)
            if cond:
                monkeys[self.trueId].items.append(newItemVal)
            else:
                monkeys[self.falseId].items.append(newItemVal)
        self.items = []

    def op(self, itemVal):
        if self.operation[2] == "old":
            return itemVal * itemVal
        if self.operation[1] == "+":
            return itemVal + int(self.operation[2])
        elif self.operation[1] == "*":
            return itemVal * int(self.operation[2])
        else:
            print("Oops", self.opWords)
            return -1
    
    def condition(self, itemVal):
        divOperator = self.testCond
        if itemVal % divOperator == 0:
            return True
        return False

main()