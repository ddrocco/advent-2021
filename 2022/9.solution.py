import copy

def main():
    with open('9.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)

    with open('9.test_input_2') as f:
        lines = f.readlines()
    testInputs2 = [line.rstrip() for line in lines]
    impl('test 2', testInputs2)
    
    with open('9.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    pt1(case, input)
    pt2(case, input)

def pt1(case, input):
    h = [0,0]
    t = [0,0]
    visitedPos = {0: set([0])}
    for row in input:
        dir = row.split(' ')[0]
        num = int(row.split(' ')[1])
        for _ in range(num):
            if dir == 'R':
                h[0] += 1
            elif dir == 'L':
                h[0] -= 1
            elif dir == 'U':
                h[1] += 1
            elif dir == 'D':
                h[1] -= 1
            t = updateKnot(h, t)
            if visitedPos.get(t[0]) == None:
                visitedPos[t[0]] = set([])
            visitedPos[t[0]].add(t[1])
    sizeSum = 0
    for vp in visitedPos:
        sizeSum += visitedPos[vp].count()
    print('%s pt1: %s' % (case, sizeSum))

def pt2(case, input):
    knots = [[0,0] for _ in range(10)]
    visitedPos = {0: set([0])}
    for row in input:
        dir = row.split(' ')[0]
        num = int(row.split(' ')[1])
        for _ in range(num):
            if dir == 'R':
                knots[0][0] += 1
            elif dir == 'L':
                knots[0][0] -= 1
            elif dir == 'U':
                knots[0][1] += 1
            elif dir == 'D':
                knots[0][1] -= 1
            for i in range(len(knots) - 1):
                knots[i+1] = updateKnot(knots[i], knots[i+1])
            if visitedPos.get(knots[-1][0]) == None:
                visitedPos[knots[-1][0]] = set([])
            visitedPos[knots[-1][0]].add(knots[-1][1])
    sizeSum = 0
    for vp in visitedPos:
        sizeSum += visitedPos[vp].count()
    print('%s pt2: %s' % (case, sizeSum))

def updateKnot(h, t):
    retTail = [t[0], t[1]]
    if abs(h[0] - t[0]) == 2 and abs(h[1] - t[1]) == 2:
        retTail[0] = (h[0] + t[0]) / 2
        retTail[1] = (h[1] + t[1]) / 2
    elif abs(h[0] - t[0]) == 2:
        retTail[0] = (h[0] + t[0]) / 2
        if h[1] != t[1]:
            retTail[1] = h[1]
    elif abs(h[1] - t[1]) == 2:
        retTail[1] = (h[1] + t[1]) / 2
        if h[0] != t[0]:
            retTail[0] = h[0]
    return retTail


class set(object):
    def __init__(self, elts):
        self.underlyingData = {}
        for elt in elts:
            self.underlyingData[elt] = True
    def add(self, elt):
        self.underlyingData[elt] = True
    def count(self):
        return len(self.underlyingData)


main()