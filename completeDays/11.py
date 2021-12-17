def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    octopuses = []

    for y in range(10):
        octopuses.append([])
        for x in range(10):
            octopuses[y].append(int(input[y][x]))
    #for y in range(10):
    #    print(octopuses[y])

    totalFlashes = 0
    ans1 = None
    ans2 = None
    for i in range(1000):
        # increase all by 1
        flashes = []
        yetToResolveFlashes = []
        for y in range(10):
            for x in range(10):
                octopuses[y][x] += 1
                if octopuses[y][x] > 9:
                    flashes.append((y, x))
                    yetToResolveFlashes.append((y, x))
        while yetToResolveFlashes:
            y, x = yetToResolveFlashes.pop()
            eightAround = get8Around(y, x)
            for targetY, targetX in eightAround:
                octopuses[targetY][targetX] += 1
                if octopuses[targetY][targetX] > 9 and (targetY, targetX) not in flashes:
                    flashes.append((targetY, targetX))
                    yetToResolveFlashes.append((targetY, targetX))
        totalFlashes += len(flashes)
        for y, x in flashes:
            octopuses[y][x] = 0
        if i + 1 == 100:
            ans1 = totalFlashes
        if len(flashes) == 100:
            ans2 = i + 1
        if ans1 and ans2:
            print("Pt 1: %s" % ans1)
            print("Pt 2: %s" % ans2)
            return

def get8Around(y, x):
    yRange = [y]
    xRange = [x]
    if y > 0:
        yRange.append(y-1)
    if y < 9:
        yRange.append(y+1)
    if x > 0:
        xRange.append(x-1)
    if x < 9:
        xRange.append(x+1)
    eightAround = []
    for thisY in yRange:
        for thisX in xRange:
            eightAround.append((thisY, thisX))
    eightAround.remove((y, x))
    return eightAround

print('\ntest\n')
main('11.testInput')
print('\nmain\n')
main('11.input')