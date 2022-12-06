def main():
    with open('2.input') as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    score1 = 0
    score2 = 0
    for i in input:
        opp = i[0]
        me = i[2]

        score1 += getScore1(opp, me)
        score2 += getScore2(opp, me)
    print('2: %s and %s' % (score1, score2))

def getScore1(opp, me):
    if opp == 'A':
        if me == 'X':
            return 1+3
        elif me == 'Y':
            return 2+6
        elif me == 'Z':
            return 3+0
        else:
            print("oops")
    elif opp == 'B':
        if me == 'X':
            return 1+0
        elif me == 'Y':
            return 2+3
        elif me == 'Z':
            return 3+6
        else:
            print("oops")
    elif opp == 'C':
        if me == 'X':
            return 1+6
        elif me == 'Y':
            return 2+0
        elif me == 'Z':
            return 3+3
        else:
            print("oops")
    else:
        print("opps")

def getScore2(opp, me):
    if opp == 'A':
        if me == 'X':
            return 3+0
        elif me == 'Y':
            return 1+3
        elif me == 'Z':
            return 2+6
        else:
            print("oops")
    elif opp == 'B':
        if me == 'X':
            return 1+0
        elif me == 'Y':
            return 2+3
        elif me == 'Z':
            return 3+6
        else:
            print("oops")
    elif opp == 'C':
        if me == 'X':
            return 2+0
        elif me == 'Y':
            return 3+3
        elif me == 'Z':
            return 1+6
        else:
            print("oops")
    else:
        print("opps")

main()

