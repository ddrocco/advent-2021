def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    polymer = input[0]
    pairList = input[2:]
    pairs = {
        pairElt.split(' -> ')[0]: pairElt.split(' -> ')[1]
        for pairElt in pairList
    }

    # Part 1
    for j in range(10):
        newPolymer = ''
        for i in range(len(polymer) - 1):
            pair = polymer[i:i+2]
            newElt = pairs.get(pair, '')
            newPolymer += '%s%s' % (polymer[i], newElt)
        newPolymer += polymer[-1]
        polymer = newPolymer
    
    eltMap = {}
    for elt in polymer:
        eltMap[elt] = eltMap.get(elt, 0) + 1
    
    print(max(eltMap.values()) - min(eltMap.values()))

def mainTwo(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    startingPolymer = input[0]
    pairList = input[2:]
    pairs = {
        pairElt.split(' -> ')[0]: pairElt.split(' -> ')[1]
        for pairElt in pairList
    }

    spawnMapping = {
        k: [k[0] + v, v + k[1]] for k, v in pairs.iteritems()
    }

    currentPolymerMap = {}
    for i in range(len(startingPolymer) - 1):
        pair = startingPolymer[i:i+2]
        currentPolymerMap[pair] = currentPolymerMap.get(pair, 0) + 1

    for i in range(40):
        newPolymerMap = {}
        for k, v in currentPolymerMap.iteritems():
            newElts = spawnMapping[k]
            newPolymerMap[newElts[0]] = newPolymerMap.get(newElts[0], 0) + v
            newPolymerMap[newElts[1]] = newPolymerMap.get(newElts[1], 0) + v
        currentPolymerMap = newPolymerMap

    letterCounts = {}
    for k, v in currentPolymerMap.iteritems():
        letterCounts[k[0]] = letterCounts.get(k[0], 0) + v
        letterCounts[k[1]] = letterCounts.get(k[1], 0) + v

    letterCounts[startingPolymer[0]] += 1
    letterCounts[startingPolymer[-1]] += 1
    letterCounts = {
        k: v/2 for k, v in letterCounts.iteritems()
    }


    print(max(letterCounts.values()) - min(letterCounts.values()))


print('\ntest\n')
main('14.test')
mainTwo('14.test')
print('\nmain\n')
main('14.input')
mainTwo('14.input')