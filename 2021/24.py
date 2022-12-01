import math

# See https://docs.google.com/spreadsheets/d/1WHk9ol6XQgwc0QBb0l90e3KxxCFf3Vs06QIqRL4BFa4/edit?usp=sharing


def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    TestRun(94992994195998, input).run()

class TestRun(object):
    def __init__(self, monad, input):
        print('start\n')
        self.monad = monad
        self.monadArr = [int(c) for c in str(monad)]
        self.input = input
        self.instruction = 1

        self.registers = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self.digit = 0

    def printState(self):
        print(
            "%s\t%s:\n\t\t%s\t%s\t%s\t%s" % (
            self.instruction,
            self.monadArr[0:self.digit],
            self.registers['w'],
            self.registers['x'],
            self.registers['y'],
            self.registers['z']
        ))

    def run(self):
        for instruction in self.input:
            elts = instruction.split(' ')
            self.registers[elts[1]] = self.operate(elts)
            self.instruction += 1
            self.printState()
        if self.registers['z'] == 0:
            print("%s - success" % self.monad)
            return True
        else:
            print("%s - failure - %s" % (self.monad, self.registers['z']))
            return False

    def operate(self, elts):
        instr = elts[0]
        if instr == 'inp':
            popDigit = self.digit
            self.digit += 1
            return int(self.monadArr[popDigit])
        a = self.registers[elts[1]]
        b = elts[2]
        if b in ['w', 'x', 'y', 'z']:
            b = self.registers[b]
        else:
            b = int(b)
        if instr == 'add':
            return a + b
        if instr == 'mul':
            return a * b
        if instr == 'div':
            if b == 0:
                raise Exception('div by 0')
            return int(a / b)
        if instr == 'mod':
            if a<0:
                raise Exception('mod by a<0')
            if b<=0:
                raise Exception('mod by b<=0')
            return a % b
        if instr == 'eql':
            return 1 if a == b else 0
        raise Exception('invalid instr')

def toInvertedString(intVal):
    strVal = ""
    while intVal:
        strVal += str(int(intVal % 10))
        intVal = int(intVal / 10)
    return strVal

if True:
    print('\ntest\n')
    main('24.test')
if False:
    print('\nmain\n')
    main('24.input')