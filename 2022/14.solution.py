from util.set import set

def main():
    with open('14.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)
    
    with open('14.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    grid, startSize, maxY = pt1(case, input)
    pt2(case, grid, startSize, maxY)

def pt1(case, input):
    grid = set([])
    minX = 500
    maxX = 500
    maxY = 0

    for line in input:
        elts = line.split(' -> ')
        startX = None
        startY = None
        for c in [elt.split(',') for elt in elts]:
            x = int(c[0])
            y = int(c[1])
            if startX is not None and startY is not None:
                if x == startX:
                    for i in range(min(y, startY), max(y, startY) + 1):
                        grid.add((x, i))
                elif y == startY:
                    for i in range(min(x, startX), max(x, startX) + 1):
                        grid.add((i, y))
                else:
                    print("Oops")
            startX = x
            startY = y
            minX = min(minX, startX)
            maxX = max(maxX, startX)
            maxY = max(maxY, startY)

    startingGridSize = grid.count()
    sandX = 500
    sandY = 0
    while sandX >= minX and sandX <= maxX and sandY <= maxY:
        if not grid.has((sandX, sandY+1)):
            sandY += 1
        elif not grid.has((sandX-1, sandY+1)):
            sandX -= 1
            sandY += 1
        elif not grid.has((sandX+1, sandY+1)):
            sandX += 1
            sandY += 1
        else:
            grid.add((sandX, sandY))
            sandX = 500
            sandY = 0
    endingGridSize = grid.count()
    print('%s pt1: %s' % (case, endingGridSize - startingGridSize))
    return grid, startingGridSize, maxY

def pt2(case, grid, startSize, maxY):
    sandX = 500
    sandY = 0
    while not grid.has((500, 0)):
        if sandY == maxY + 1:
            grid.add((sandX, sandY))
            sandX = 500
            sandY = 0
        elif not grid.has((sandX, sandY+1)):
            sandY += 1
        elif not grid.has((sandX-1, sandY+1)):
            sandX -= 1
            sandY += 1
        elif not grid.has((sandX+1, sandY+1)):
            sandX += 1
            sandY += 1
        else:
            grid.add((sandX, sandY))
            sandX = 500
            sandY = 0
    endingGridSize = grid.count()
    print('%s pt2: %s' % (case, endingGridSize - startSize))
    
main()