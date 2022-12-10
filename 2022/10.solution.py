import copy

def main():
    with open('10.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)
    
    with open('10.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    pt1(case, input)

def pt1(case, input):
    # Pt1
    signalStrs = []
    cycle = 1
    xval = 1
    # Pt2
    rows = []
    currRow = ''
    for line in input:
        # Pt2
        if shouldDraw(xval, cycle):
            currRow += '#'
        else:
            currRow += '.'
        if cycle % 40 == 0:
            rows.append(currRow)
            currRow = ''

        if (cycle + 20) % 40 == 0:
            signalStrs.append(cycle * xval)
        if line == "noop":
            cycle += 1
        else:
            valAdj = int(line.split(" ")[1])
            if (cycle+21) % 40 == 0:
                signalStrs.append((cycle+1) * xval)
            # Pt2
            if shouldDraw(xval, cycle+1):
                currRow += '#'
            else:
                currRow += '.'
            if (cycle+1) % 40 == 0:
                rows.append(currRow)
                currRow = ''
            # Pt1
            xval += valAdj
            cycle += 2
    strSum = sum(signalStrs)
    print('%s pt1: %s' % (case, strSum))
    for row in rows:
        print(row, len(row))

def shouldDraw(xval, cycle):
    adjCycle = (cycle-1) % 40
    if abs(xval-adjCycle) <= 1:
        # print("Yes", xval, adjCycle)
        return True
    else:
        # print("No", xval, adjCycle)
        return False


main()