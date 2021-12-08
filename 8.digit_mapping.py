import math

def main():
    with open('8.input') as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    # Part 1
    inputTuples = [inputLine.split(' | ') for inputLine in input]
    codeLines = [inputTuple[1] for inputTuple in inputTuples]
    uniqueLenCodes = [code for codes in codeLines for code in codes.split(' ') if len(code) in (2, 3, 4, 7)]
    print(len(uniqueLenCodes))

    # Part 2
    runningTotal = 0
    for inputTuple in inputTuples:
        words = inputTuple[0].split(' ')
        mapping = getMapping(words)
        seq = inputTuple[1].split(' ')
        result = []
        for seqEntry in seq:
            for k, v in mapping.iteritems():
                if getAContainsAllOfB(v, seqEntry) and getAContainsAllOfB(seqEntry, v):
                    result.append(k)
        print(result)

        resultInt = arrayToInt(result)
        print("%s | %s" % (resultInt, runningTotal))
        runningTotal += resultInt
    print(runningTotal)

def getMapping(words):
    # 2: 1
    # 3: 7
    # 4: 4
    # 5, [2, 3, 5]
    # 6: [0, 6, 9]
    # 7: 8
    mappings = {}
    mappings[1] = [word for word in words if len(word) == 2][0]
    words.remove(mappings[1])
    mappings[4] = [word for word in words if len(word) == 4][0]
    words.remove(mappings[4])
    mappings[7] = [word for word in words if len(word) == 3][0]
    words.remove(mappings[7])
    mappings[8] = [word for word in words if len(word) == 7][0]
    words.remove(mappings[8])
    for word in words:
        if len(word) == 5:
            continue
        # len is 6 -- 0, 6, 9
        if getAContainsAllOfB(word, mappings[4]):
            # word is 9
            mappings[9] = word
            continue
        if getAContainsAllOfB(word, mappings[1]):
            # word is 0
            mappings[0] = word
            continue
        mappings[6] = word
    words.remove(mappings[0])
    words.remove(mappings[6])
    words.remove(mappings[9])
    for word in words:
        # len is 5 -- 2, 3, 5
        if getAContainsAllOfB(word, mappings[7]):
            # word is 3
            mappings[3] = word
            continue
        if getAContainsAllOfB(mappings[6], word):
            # word is 5
            mappings[5] = word
            continue
        mappings[2] = word
    if len(mappings) != 10:
        raise Exception(mappings)
    return mappings

def getAContainsAllOfB(a, b):
    for c in b:
        if c not in a:
            return False
    return True

def arrayToInt(array):
    resultInt = 0
    array.reverse()
    for i, r in enumerate(array):
        resultInt += r * math.pow(10, i)
    return resultInt

main()