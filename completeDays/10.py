parensMap = {
    '{': '}',
    '(': ')',
    '<': '>',
    '[': ']',
}

scoreMap = {
    '}': 1197,
    ')': 3,
    '>': 25137,
    ']': 57,
}

autoCompleteScoreMap = {
    '{': 3,
    '(': 1,
    '<': 4,
    '[': 2,
}

def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    # Part 1
    erroneousScore = 0
    autocompleteScores = []
    for line in input:
        wasErroneous = False
        stack = []
        for c in line:
            if c in ['(', '[', '<', '{']:
                stack.append(c)
            else:
                e = stack.pop()
                if parensMap.get(e) == c:
                    continue
                else:
                    erroneousScore += scoreMap.get(c)
                    wasErroneous = True
                    break
        if not wasErroneous:
            autocompleteScore = 0
            while stack:
                c = stack.pop()
                autocompleteScore *= 5
                autocompleteScore += autoCompleteScoreMap.get(c)
            autocompleteScores.append(autocompleteScore)

    # Part 1
    print(erroneousScore)

    # Part 2
    numScores = len(autocompleteScores)
    autocompleteScores.sort()
    print(autocompleteScores[numScores/2])
    print(autocompleteScores)


print('\ntest\n')
main('10.testInput')
print('\nmain\n')
main('10.input')