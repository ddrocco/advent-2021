def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    # print(input)
    
    dots = []
    folds = []
    noLongerDots = False
    for line in input:
        if line == '':
            noLongerDots = True
        elif not noLongerDots:
            elts = line.split(',')
            dots.append((int(elts[0]), int(elts[1])))
        else:
            elts = line[len('fold along '):].split('=')
            folds.append((elts[0], int(elts[1])))

    for fold in folds[0:1]:
        dots = doFold(dots, fold)

    print(len(dots))

    for fold in folds[1:]:
        dots = doFold(dots, fold)

    printDots(dots)

def doFold(dots, fold):
    newDots = []
    cutoff = fold[1]
    if fold[0] == 'x':
        for dot in dots:
            if dot[0] > cutoff:
                newDot = (cutoff * 2 - dot[0], dot[1])
            else:
                newDot = dot
            if newDot not in newDots:
                newDots.append(newDot)
    else: # fold[0] == 'y'
        for dot in dots:
            newDot = None
            if dot[1] > cutoff:
                newDot = (dot[0], cutoff * 2 - dot[1])
            else:
                newDot = dot
            if newDot not in newDots:
                newDots.append(newDot)
    return newDots

def printDots(dots):
    maxX = 0
    maxY = 0
    for dot in dots:
        maxX = max(dot[0]+1, maxX)
        maxY = max(dot[1]+1, maxY)
    for y in range(maxY):
        str = ''
        for x in range(maxX):
            if (x,y) in dots:
                str += '#'
            else:
                str += '.'
        print('%s\n' % str)


print('\ntest\n')
main('13.testInput')
print('\nmain\n')
main('13.input')