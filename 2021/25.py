import copy

def main(filename, maxIterations=0):
    with open(filename) as f:
        lines = f.readlines()
    input = [[c for c in line.strip()] for line in lines]
    
    cucMap = CucMap(input, maxIterations)

    if False: # Test nextX
        for i in range(7):
            print("%s: %s" % (i, cucMap.nextX(i)))

    while cucMap.update():
        continue
        # cucMap.doPrint()
    print("done in %s iterations" % cucMap.iteration)

class CucMap(object):
    def __init__(self, cucMap, maxIterations):
        self.map = cucMap
        self.iteration = 0 if maxIterations else 1
        self.maxIterations = maxIterations
    
    def nextX(self, x):
        if x == len(self.map[0]) - 1:
            return 0
        else:
            return x + 1

    def nextY(self, y):
        if y == len(self.map) - 1:
            return 0
        else:
            return y + 1

    def doPrint(self):
        print("%s / %s" % (self.iteration, self.maxIterations))
        for row in self.map:
            print(''.join(row))
        print('')

    def update(self):
        # Move right
        rightMovers = []
        for y, row in enumerate(self.map):
            for x, c in enumerate(row):
                if c == '>' and row[self.nextX(x)] == '.':
                    rightMovers.append((x, y))
        for x, y in rightMovers:
            self.map[y][x] = '.'
            self.map[y][self.nextX(x)] = '>'

        # Move down
        downMovers = []
        for y, row in enumerate(self.map):
            for x, c in enumerate(row):
                if c == 'v' and self.map[self.nextY(y)][x] == '.':
                    downMovers.append((x, y))
        for x, y in downMovers:
            self.map[y][x] = '.'
            self.map[self.nextY(y)][x] = 'v'

        if len(rightMovers) == 0 and len(downMovers) == 0:
            return False

        self.iteration += 1
        if self.iteration == self.maxIterations:
            return False
        else:
            return True


if False:
    print('\ndebug\n')
    main('25.debug', 4)
if False:
    print('\ntest\n')
    main('25.test')
if True:
    print('\nmain\n')
    main('25.input')