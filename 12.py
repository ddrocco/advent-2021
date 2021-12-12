import copy

def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    caveMap = {}
    for entry in input:
        entryElts = entry.split('-')
        if not caveMap.get(entryElts[0]):
            caveMap[entryElts[0]] = []
        caveMap[entryElts[0]].append(entryElts[1])
    secondaryMap = copy.copy(caveMap)
    for k, vList in secondaryMap.iteritems():
        for v in vList:
            if not caveMap.get(v):
                caveMap[v] = []
            if k not in caveMap[v]:
                caveMap[v].append(k)
    for k in caveMap.keys():
        if 'start' in caveMap[k]:
            caveMap[k].remove('start')
    print(caveMap)

    # Part 1
    pathCount = 0
    paths = [['start']]
    while paths:
        currPath = paths.pop()
        currCave = currPath[-1]
        for dest in caveMap.get(currCave, []):
            if dest == 'end':
                pathCount += 1
                # print(currPath + [dest])
                continue
            if dest.isupper() or dest not in currPath:
                paths.append(currPath + [dest])
    print(pathCount)

    # Part 2
    pathCount = 0
    paths = [(['start'], False)]
    while paths:
        currPath, hasVisitedSmallTwice = paths.pop()
        currCave = currPath[-1]
        for dest in caveMap.get(currCave, []):
            if dest == 'end':
                pathCount += 1
                # print(currPath + [dest])
                continue
            if dest.isupper() or dest not in currPath:
                paths.append((currPath + [dest], hasVisitedSmallTwice))
                continue
            if not hasVisitedSmallTwice:
                paths.append((currPath + [dest], True))
    print(pathCount)



print('\ntest1\n')
main('12.testInput1')
print('\ntest2\n')
main('12.testInput2')
print('\ntest3\n')
main('12.testInput3')
print('\nmain\n')
main('12.input')