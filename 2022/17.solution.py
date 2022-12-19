from util.set import set

TEST_PT_1 = False
PROD_PT_1 = False
TEST_PT_2 = False
PROD_PT_2 = True

NUM_ROCKS = 2022 # 2022

Q_NUM = 17

def main():
    with open('%s.test_input' % Q_NUM) as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs[0], TEST_PT_1, TEST_PT_2)
    
    with open('%s.input' % Q_NUM) as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs[0], PROD_PT_1, PROD_PT_2)

def impl(case, input, doPt1, doPt2):
    if doPt1:
        pt1(case, input)
    if doPt2:
        pt2(case, input)
    return

def pt1(case, input):
    rockHeight = 0
    # We're adding rows, so x is the second coordinate.
    # grid[y][x] gets what's at [x][y].
    grid = [['#' for i in range(7)]]
    grid.extend([['.' for i in range(7)] for j in range(7)])
    rockSpawns = [
        [(2, -4), (3, -4), (4, -4), (5, -4)], # -
        [(3, -4), (2, -3), (3, -3), (4, -3), (3, -2)], # +
        [(2, -4), (3, -4), (4, -4), (4, -3), (4, -2)], # _|
        [(2, -4), (2, -3), (2, -2), (2, -1)], # |
        [(2, -4), (3, -4), (2, -3), (3, -3)], # box
    ]
    inputTracker = 0
    lastRecordedRockHeight = 0
    for rockNum in range(NUM_ROCKS):
        if rockNum % len(input)*5 == 0:
            # print("%s - %d/%d: %d (%d)" % (case, rockNum, NUM_ROCKS, rockHeight, rockHeight-lastRecordedRockHeight))
            lastRecordedRockHeight = rockHeight
            pass
        # Spawn a rock.
        rock = rockSpawns[rockNum % 5]
        drops = 0
        while True:
            # Rock falls until it hits something.
            # 1. Currents push rock.
            inputCmd = input[inputTracker % len(input)]
            inputTracker += 1
            relative = None
            if inputCmd == '<':
                relative = -1
            else:
                relative = 1
            shouldMove = True
            for pebble in rock:
                if (pebble[0]+relative > 6 or
                    pebble[0]+relative < 0 or
                    grid[pebble[1]][pebble[0]+relative] == "#"
                ):
                    shouldMove = False
                    break
            if shouldMove:
                rock = [(pebble[0]+relative, pebble[1]) for pebble in rock]
            # Rock falls.
            isFloored = False
            for pebble in rock:
                if grid[pebble[1]-1][pebble[0]] == "#":
                    isFloored = True
                    # print(pebble[1]-1, grid[pebble[1]-1])
                    break
            if isFloored:
                for pebble in rock:
                    grid[pebble[1]][pebble[0]] = "#"
                    if grid[pebble[1]] == ['#' * 7]:
                        print("FULL")
                # Break out of while loop.
                # print("%d: %d drops" % (rockNum, drops))
                break
            else:
                drops += 1
                rock = [(pebble[0], pebble[1]-1) for pebble in rock]
        # Extend the grid based on the new highest height.
        rockHeight = rock[-1][1] + len(grid)
        numNewRows = rock[-1][1] + 8
        grid.extend([['.' for i in range(7)] for j in range(numNewRows)])

    print('%s pt1: %s' % (case, rockHeight))

def pt2(case, input):
    rockHeight = 0
    # We're adding rows, so x is the second coordinate.
    # grid[y][x] gets what's at [x][y].
    grid = [['#' for i in range(7)]]
    grid.extend([['.' for i in range(7)] for j in range(7)])
    rockSpawns = [
        [(2, -4), (3, -4), (4, -4), (5, -4)], # -
        [(3, -4), (2, -3), (3, -3), (4, -3), (3, -2)], # +
        [(2, -4), (3, -4), (4, -4), (4, -3), (4, -2)], # _|
        [(2, -4), (2, -3), (2, -2), (2, -1)], # |
        [(2, -4), (3, -4), (2, -3), (3, -3)], # box
    ]
    inputTracker = 0
    numRocksTotal = 1000000000000
    maxTrackVals = 0
    lastMaxTrackValRockNum = 0
    maxTrackValDiffs = []
    lastMaxValHeight = 0
    extraHeight = None
    rockNum = 0
    # We won't iterate this many times and will break once we find a pattern.
    while rockNum < numRocksTotal:
        trackVals = 0
        mayTrackVals = True
        # Spawn a rock.
        rock = rockSpawns[rockNum % 5]
        drops = 0

        # Only track rock #4 when it starts at input 0.
        if rockNum % 5 != 3 and inputTracker % len(input) != 0:
            mayTrackVals = False

        rockFallStep = 1
        while True:
            # Rock falls until it hits something.
            # 1. Currents push rock.
            inputCmd = input[inputTracker % len(input)]
            inputTracker += 1
            relative = None
            if inputCmd == '<':
                relative = -1
            else:
                relative = 1
            shouldMove = True
            for pebble in rock:
                if (pebble[0]+relative > 6 or
                    pebble[0]+relative < 0 or
                    grid[pebble[1]][pebble[0]+relative] == "#"
                ):
                    shouldMove = False
                    break
            if shouldMove:
                rock = [(pebble[0]+relative, pebble[1]) for pebble in rock]
                if mayTrackVals:
                    trackVals += 2^(2*rockFallStep)
            elif mayTrackVals:
                    trackVals += 2^(2*rockFallStep+1)
            rockFallStep += 1
            # Rock falls.
            isFloored = False
            for pebble in rock:
                if grid[pebble[1]-1][pebble[0]] == "#":
                    isFloored = True
                    # print(pebble[1]-1, grid[pebble[1]-1])
                    break
            if isFloored:
                if mayTrackVals:
                    if trackVals == maxTrackVals:
                        diff = rockNum - lastMaxTrackValRockNum
                        maxTrackValDiffs.append(diff)
                        print(maxTrackValDiffs)
                        if len(maxTrackValDiffs) >= 3 and diff == maxTrackValDiffs[-3] and diff == maxTrackValDiffs[-2] and diff == maxTrackValDiffs[-1]:
                            cycleSize = diff
                            cycleHeightDiff = rockHeight - lastMaxValHeight
                            
                            numRemainingRocks = numRocksTotal - rockNum
                            remainingOffset = numRemainingRocks % cycleSize
                            numRemainingCycles = (numRemainingRocks - remainingOffset) / cycleSize
                            extraHeight = numRemainingCycles * cycleHeightDiff
                            numRocksTotal = rockNum + remainingOffset
                            print(numRemainingCycles, cycleHeightDiff)

                        lastMaxTrackValRockNum = rockNum
                        lastMaxValHeight = rockHeight
                    if trackVals > maxTrackVals:
                        maxTrackVals = trackVals
                        lastMaxTrackValRockNum = rockNum
                for pebble in rock:
                    grid[pebble[1]][pebble[0]] = "#"

                # Break out of while loop.
                # print("%d: %d drops" % (rockNum, drops))
                break
            else:
                drops += 1
                rock = [(pebble[0], pebble[1]-1) for pebble in rock]
        # Extend the grid based on the new highest height.
        rockHeight = rock[-1][1] + len(grid)
        numNewRows = rock[-1][1] + 8
        grid.extend([['.' for i in range(7)] for j in range(numNewRows)])

        rockNum += 1
    # printGrid(grid)
    print('%s pt2: %s' % (case, rockHeight + extraHeight))

def printGrid(grid):
    gridLen = len(grid)
    for i in range(gridLen):
        print(grid[gridLen-i-1])

main()