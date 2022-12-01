import math

def main():
    with open('9.input') as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    # Part 1
    xLen = len(input[0])
    yLen = len(input)

    bufferedInput = []
    bufferedInput.append(('%s' % '.') * (xLen + 2))
    for i in range(yLen):
        bufferedInput.append("%s%s%s" % ('.', input[i], '.'))
    bufferedInput.append(('%s' % '.') * (xLen + 2))

    lowPoints = []
    # print(bufferedInput)
    for y in range(1, yLen+1):
        # print("Scanning y=%s: %s" % (y, bufferedInput[y]))
        for x in range(1, xLen+1):
            # print("\tScanning x=%s: %s" % (x, bufferedInput[y][x]))
            v = bufferedInput[y][x]
            if (
                isGreaterThanOrInvalid(v, bufferedInput[y][x+1]) and
                isGreaterThanOrInvalid(v, bufferedInput[y][x-1]) and
                isGreaterThanOrInvalid(v, bufferedInput[y+1][x]) and
                isGreaterThanOrInvalid(v, bufferedInput[y-1][x])
            ):
                lowPoints.append(int(v)+1)
                '''
                print("\t\tLocal minimum %s at (%s, %s) comp (%s, %s, %s, %s)" % (
                    v,
                    x,
                    y,
                    bufferedInput[y][x+1],
                    bufferedInput[y][x-1],
                    bufferedInput[y+1][x],
                    bufferedInput[y-1][x]))
                '''
    print(sum(lowPoints))

    # Part 2
    visitedSpaces = [[False for x in range(xLen)] for y in range(yLen)]
    print(visitedSpaces)

    visitQueue = []
    basins = []
    for y in range(yLen):
        for x in range(xLen):
            if visitedSpaces[y][x] == False:
                if int(input[y][x]) != 9:
                    basinSize = 0
                    print("Enqueueing %s, %s" % (y, x))
                    visitQueue.append((y, x))
                    while visitQueue:
                        visitY, visitX = visitQueue.pop()
                        if visitedSpaces[visitY][visitX]:
                            print("Skipping %s, %s" % (visitY, visitX))
                            continue
                        visitedSpaces[visitY][visitX] = True
                        if int(input[visitY][visitX]) == 9:
                            print("Visiting %s, %s - 9 wall" % (visitY, visitX))
                            continue
                        basinSize += 1
                        print("Visiting %s, %s - adding to basin (%s)" % (visitY, visitX, basinSize))
                        if visitX > 0:
                            visitQueue.append((visitY, visitX-1))
                        if visitX < xLen-1:
                            visitQueue.append((visitY, visitX+1))
                        if visitY > 0:
                            visitQueue.append((visitY-1, visitX))
                        if visitY < yLen-1:
                            visitQueue.append((visitY+1, visitX))
                    basins.append(basinSize)
                else:
                    print("Visiting %s, %s" % (y, x))
                    visitedSpaces[y][x] = True
    print(basins)
    maxBasins = []
    for i in range(3):
        newMaxBasin = max(basins)
        basins.remove(newMaxBasin)
        maxBasins.append(newMaxBasin)
    print(maxBasins[0] * maxBasins[1] * maxBasins[2])

        
                
                    
                        


def isGreaterThanOrInvalid(val, cmp):
    if cmp == '.':
        return True
    elif int(cmp) > int(val):
        return True
    return False

main()