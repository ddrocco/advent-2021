def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    croppedInput = input[0][len('target area: x='):]
    xVals = [int(xVal) for xVal in croppedInput.split(',')[0].split('..')]
    yVals = [int(yVal) for yVal in croppedInput.split('=')[-1].split('..')]

    # Part 1:
    if xVals[0] < 0 and xVals[1] < 0:
        xVals[0] *= -1
        xVals[1] *= -1
    xVals = [min(xVals), max(xVals)]
    yVals = [min(yVals), max(yVals)]
    print(xVals, yVals)

    # Calculate possible X's:
    possibleXVs = []
    for i in range(max(xVals)+1):
        xV = i
        x = 0
        while x < max(xVals):
            x += xV
            if min(xVals) <= x and x <= max(xVals):
                possibleXVs.append(i)
                break
            if xV > 0:
                xV -= 1
            elif xV < 0:
                xV += 1
            if xV == 0:
                break

    possibleYVs = []
    for i in range(min(yVals),-min(yVals)+1):
        yV = i
        if yV > 0:
            yV = yV*-1 -1
        y = 0
        while y > min(yVals):
            y += yV
            if min(yVals) <= y and y <= max(yVals):
                possibleYVs.append(i)
                break
            yV -= 1

    maxMaxY = 0
    possibilities = []
    for i in possibleXVs:
        for j in possibleYVs:
            xV = i
            yV = j
            x = 0
            y = 0
            maxY = 0
            successful = False
            while x < max(xVals) and y > min(yVals):
                x += xV
                y += yV
                maxY = max(y, maxY)
                if min(xVals) <= x and x <= max(xVals) and min(yVals) <= y and y <= max(yVals):
                    successful = True
                    break
                if xV > 0:
                    xV -= 1
                elif xV < 0:
                    xV += 1
                yV -= 1
            if successful:
                maxMaxY = max(maxY, maxMaxY)
                possibilities.append((i, j))
    print(maxMaxY)
    print(len(possibilities))


print('\ntest\n')
main('17.test')
print('\nmain\n')
main('17.input')