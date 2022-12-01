
def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    # Part 1
    p1Pos = int(input[0][len('Player 1 starting position: '):])
    p2Pos = int(input[1][len('Player 2 starting position: '):])
    print("Starting Pos %s; and %s" % (p1Pos, p2Pos))
    # Deterministic die is 1-100, but might as well be 1-10.
    deterministicDie = 1
    rolls = 0
    p1Score = 0
    p2Score = 0
    while p1Score < 1000 and p2Score < 1000:
        p1Pos = (p1Pos + (3 * deterministicDie + 3)) % 10
        if p1Pos == 0:
            p1Pos = 10
        p1Score += p1Pos
        deterministicDie += 3
        rolls += 3
        # print("P1 scores %s and now has %s" % (p1Pos, p1Score))
        if p1Score >= 1000:
            break
        p2Pos = (p2Pos + (3 * deterministicDie + 3)) % 10
        if p2Pos == 0:
            p2Pos = 10
        p2Score += p2Pos
        deterministicDie += 3
        rolls += 3
        # print("P2 scores %s and now has %s" % (p2Pos, p2Score))
    # print(p1Score, p2Score, rolls)
    print(min(p1Score, p2Score) * rolls)

    p1Pos = int(input[0][len('Player 1 starting position: '):])
    p2Pos = int(input[1][len('Player 2 starting position: '):])
    # P1Wins, P2Wins
    completedUniverseCount = [0, 0]
    p1UniverseCount = {
        # Key is p1Pos, p1Score
        (p1Pos, 0): 1
    }
    p2UniverseCount = {
        # Key is p2Pos, p2Score
        (p2Pos, 0): 1
    }
    while p1UniverseCount.keys() and p2UniverseCount.keys():
        p1UniverseCount, newCompleteP1Universes = iterate(p1UniverseCount)
        completedUniverseCount[0] += newCompleteP1Universes * sum(p2UniverseCount.values())

        if not p1UniverseCount.keys():
            break

        p2UniverseCount, newCompleteP2Universes = iterate(p2UniverseCount)
        completedUniverseCount[1] += newCompleteP2Universes * sum(p1UniverseCount.values())
    print(completedUniverseCount)
    print(int(max(completedUniverseCount)))

def iterate(universeCount):
    nextUniverseCount = {}
    completedUniverseCount = 0
    for universe in universeCount.keys():
        pos = universe[0]
        score = universe[1]
        # 3 : 1/27
        # 4 : 3/27
        # 5 : 6/27
        # 6 : 7/27
        # 7 : 6/27
        # 8 : 3/27
        # 9 : 1/27
        key = (
            (((pos + 3) - 1) % 10) + 1,
            score + (((pos + 3) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 1 * universeCount[universe]
        key = (
            (((pos + 4) - 1) % 10) + 1,
            score + (((pos + 4) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 3 * universeCount[universe]
        key = (
            (((pos + 5) - 1) % 10) + 1,
            score + (((pos + 5) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 6 * universeCount[universe]
        key = (
            (((pos + 6) - 1) % 10) + 1,
            score + (((pos + 6) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 7 * universeCount[universe]
        key = (
            (((pos + 7) - 1) % 10) + 1,
            score + (((pos + 7) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 6 * universeCount[universe]
        key = (
            (((pos + 8) - 1) % 10) + 1,
            score + (((pos + 8) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 3 * universeCount[universe]
        key = (
            (((pos + 9) - 1) % 10) + 1,
            score + (((pos + 9) - 1) % 10) + 1,
        )
        nextUniverseCount[key] = nextUniverseCount.get(key, 0) + 1 * universeCount[universe]

    uToRemove = []
    maxScore = 0
    minScore = 21
    for u in nextUniverseCount.keys():
        if u[1] >= 21:
            completedUniverseCount += nextUniverseCount[u]
            uToRemove.append(u)
        maxScore = max(maxScore, u[1])
        minScore = min(minScore, u[1])
    for u in uToRemove:
        nextUniverseCount.pop(u)
    # print("Day is done : %s - %s" % (minScore, maxScore))
    return nextUniverseCount, completedUniverseCount


if True:
    print('\ntest\n')
    main('21.test')
if True:
    print('\nmain\n')
    main('21.input')