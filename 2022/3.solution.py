def main():
    with open('3.test_input') as f:
        lines = f.readlines()
    testInput = [line.strip() for line in lines]
    impl('test', testInput)
    
    with open('3.input') as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    impl('real', input)

valmap = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
    'A': 1+26,
    'B': 2+26,
    'C': 3+26,
    'D': 4+26,
    'E': 5+26,
    'F': 6+26,
    'G': 7+26,
    'H': 8+26,
    'I': 9+26,
    'J': 10+26,
    'K': 11+26,
    'L': 12+26,
    'M': 13+26,
    'N': 14+26,
    'O': 15+26,
    'P': 16+26,
    'Q': 17+26,
    'R': 18+26,
    'S': 19+26,
    'T': 20+26,
    'U': 21+26,
    'V': 22+26,
    'W': 23+26,
    'X': 24+26,
    'Y': 25+26,
    'Z': 26+26,
}

def impl(case, input):
    tot1 = 0
    # Pt 1
    for line in input:
        val = None
        cset1 = {}
        cset2 = {}
        halfway = int(len(line)/2)
        comp1 = line[:halfway]
        comp2 = line[halfway:]
        for c in comp1:
            cset1[c] = 1
        for c in comp2:
            cset2[c] = 1
        for c in cset1:
            if cset2.get(c) == 1:
                val = c
                break
        prio = valmap.get(val)
        tot1 += prio

    # Pt 2
    tot2 = 0
    for subsetIndex in range(0, len(input), 3):
        csets = {
            0: {},
            1: {},
            2: {},
        }
        for i, line in enumerate(input[subsetIndex:subsetIndex+3]):
            for c in line:
                csets[i][c] = 1
        val = None
        for c in csets[0]:
            if csets[1].get(c) == 1 and csets[2].get(c) == 1:
                val = c
                break
        prio = valmap.get(val)
        tot2 += prio
    print('%s pt1: %s' % (case, tot1))
    print('%s pt2: %s' % (case, tot2))

main()