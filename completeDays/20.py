import math

def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]

    valueMap = []
    image = []
    isNowMappingImage = False
    for elt in input:
        if isNowMappingImage:
            image.append(elt)
        elif elt != '':
            valueMap.extend([e for e in elt])
        else:
            isNowMappingImage = True

    print("\nStart:\n")

    for i in range(2):
        image = enhance(valueMap, image, i)
        print(i)

    printLit(image)

    for i in range(2, 50):
        image = enhance(valueMap, image, i)
        print(i)

    printLit(image)

def printLit(image):
    litCount = 0
    for im in image:
        for i in im:
            if i == '#':
                litCount += 1
    print("Lit Count: %s" % litCount)


def enhance(valueMap, image, iteration):
    if iteration == 0:
        default = '.'
    elif iteration % 2 == 1 and valueMap[0] == '#':
        default = '#'
    else:
        default = valueMap[-1]

    newImage = []
    for y in range(-1, len(image) + 1):
        newRow = []
        for x in range(-1, len(image[0]) + 1):
            eightAround = get8Around(y, x, image, default)                
            idx, newDigit = mapValue(eightAround, valueMap)
            if x == 3 and y == -1 and iteration == -1:
                print("Derek")
                print(eightAround)
                print('\n')
                print(idx, ' ', valueMap[idx])
                print('\n')
                newRow.append('~')
            else:
                newRow.append(newDigit)
        newImage.append(newRow)
    return newImage

def mapValue(eightAround, valueMap):
    index = 0
    fakeBinary = eightAround[0] + eightAround[1] + eightAround[2]
    fakeBinary.reverse()
    for i in range(9):
        if fakeBinary[i] == '.':
            continue
        elif fakeBinary[i] == '#':
            index += int(math.pow(2, i))
        else:
            raise Exception("Bad value")
    return index, valueMap[index]

    

def get8Around(y, x, image, default):
    eightAround = [[None, None, None], [None, None, None], [None, None, None]]

    # Row 0:
    if y > 0:
        if x > 0:
            eightAround[0][0] = image[y-1][x-1]
        else:
            eightAround[0][0] = default
        if x >= 0 and x <= len(image[0]) - 1:
            eightAround[0][1] = image[y-1][x]
        else:
            eightAround[0][1] = default
        if x < len(image[0]) - 1:
            eightAround[0][2] = image[y-1][x+1]
        else:
            eightAround[0][2] = default
    else:
        eightAround[0] = [default, default, default]

    # Row 1:
    if y >= 0 and y <= len(image) - 1:
        if x > 0:
            eightAround[1][0] = image[y][x-1]
        else:
            eightAround[1][0] = default
        if x >= 0 and x <= len(image[0]) - 1:
            eightAround[1][1] = image[y][x]
        else:
            eightAround[1][1] = default
        if x < len(image[0]) - 1:
            eightAround[1][2] = image[y][x+1]
        else:
            eightAround[1][2] = default
    else:
        eightAround[1] = [default, default, default]

    # Row 2:
    if y < len(image) - 1:
        if x > 0:
            eightAround[2][0] = image[y+1][x-1]
        else:
            eightAround[2][0] = default
        if x >= 0 and x <= len(image[0]) - 1:
            eightAround[2][1] = image[y+1][x]
        else:
            eightAround[2][1] = default
        if x < len(image[0]) - 1:
            eightAround[2][2] = image[y+1][x+1]
        else:
            eightAround[2][2] = default
    else:
        eightAround[2] = [default, default, default]
    return eightAround

if False:
    print('\ntest\n')
    main('20.test')
if True:
    print('\nmain\n')
    main('20.input')