def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    # print(input)

    inputInstructions = []
    for instruction in input:
        eltements = instruction.split(' ')
        boo = 1 if eltements[0] == 'on' else 0
        arr = eltements[1].split(',')
        simpleArr = []
        for a in arr:
            simpleArr.append(
                [int(elt) for elt in a.split('=')[1].split('..')]
            )
        inputInstructions.append((boo, simpleArr))
    # print(inputInstructions)
    
    # Part 1
    if True:
        onCubes = {}
        for instruction in inputInstructions:
            Zs = instruction[1][2]
            minZ = max(Zs[0], -50)
            maxZ = min(Zs[1], 50)

            Ys = instruction[1][1]
            minY = max(Ys[0], -50)
            maxY = min(Ys[1], 50)

            Xs = instruction[1][0]
            minX = max(Xs[0], -50)
            maxX = min(Xs[1], 50)

            for z in range(minZ, maxZ+1):
                for y in range(minY, maxY+1):
                    for x in range(minX, maxX+1):
                        onCubes[(x, y, z)] = instruction[0]
        
        print(sum(onCubes.values()))
    
    # Part 2
    if True:
        cubes = []
        for i, instruction in enumerate(inputInstructions):
            print("Reading instruction %s [%s] [%s]\n\n" % (i, "on" if instruction[0] else "off", instruction[1]))
            # Add:
            if instruction[0] == 1:
                newCubes = [Cube(instruction[1])]
                # printVol(newCubes)
                for oldCube in cubes:
                    # print("SUBTRACTING %s" % oldCube)
                    fixedNewCubes = []
                    for newCube in newCubes:
                        overlap = newCube.getOverlapCube(oldCube)
                        if overlap:
                            # print("Subtracting %s" % overlap)
                            fixedNewCubes.extend(newCube.subtract(overlap))
                        else:
                            fixedNewCubes.append(newCube)
                    newCubes = fixedNewCubes
                cubes.extend(newCubes)
                # printVol(newCubes)
                cubes = unionize(cubes)
            # subtract:
            else:
                thisNegativeCube = Cube(instruction[1])
                newCubes = []
                for cube in cubes:
                    overlap = cube.getOverlapCube(thisNegativeCube)
                    if overlap:
                        newCubes.extend(cube.subtract(overlap))
                    else:
                        newCubes.append(cube)
                cubes = newCubes
                cubes = unionize(cubes)
            # print(cubes)
            # printVol(cubes)

        printVol(cubes)

def printVol(cubeArray):
    vol = 0
    for cube in cubeArray:
        vol += cube.volume()
    print(vol)

class Cube(object):
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "{%s:%s},{%s:%s},{%s:%s} - %sx%sx%s - %s" % (
            self.x[0], self.x[1], self.y[0], self.y[1], self.z[0], self.z[1],
            self.x[1]-self.x[0]+1,
            self.y[1]-self.y[0]+1,
            self.z[1]-self.z[0]+1,
            self.volume()
        )

    def isWithin(self, other):
        if (self.x[0] >= other.x[0] and self.x[1] <= other.x[1] and
            self.y[0] >= other.y[0] and self.y[1] <= other.y[1] and
            self.z[0] >= other.z[0] and self.z[1] <= other.z[1]):
            return True
        return False

    def corners(self):
        c = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    c.append([
                        self.x[i], self.y[j], self.z[k]
                    ])
        return c
    
    def volume(self):
        x = self.x[1]-self.x[0]+1
        y = self.y[1]-self.y[0]+1
        z = self.z[1]-self.z[0]+1
        return x*y*z
        

    def splitX(self, x):
        if x < self.x[0] or x > self.x[1]:
            return [self]
        cubeL = Cube([[self.x[0], x-1], self.y, self.z])
        cubeM = Cube([[x,x], self.y, self.z])
        cubeR = Cube([[x+1, self.x[1]], self.y, self.z])
        return [cubeL, cubeM, cubeR]

    def splitY(self, y):
        if y < self.y[0] or y > self.y[1]:
            return [self]
        cubeU = Cube([self.x, [self.y[0], y-1], self.z])
        cubeM = Cube([self.x, [y,y], self.z])
        cubeD = Cube([self.x, [y+1, self.y[1]], self.z])
        return [cubeU, cubeM, cubeD]

    def splitZ(self, z):
        if z < self.z[0] or z > self.z[1]:
            return [self]
        cubeF = Cube([self.x, self.y, [self.z[0], z-1]])
        cubeM = Cube([self.x, self.y, [z,z]])
        cubeB = Cube([self.x, self.y, [z+1, self.z[1]]])
        return [
            cubeF, cubeM, cubeB]

    def splitAtCornerIfOverlap(self, corner):
        if (self.x[0] <= corner[0] and corner[0] <= self.x[1] and 
            self.y[0] <= corner[1] and corner[1] <= self.y[1] and 
            self.z[0] <= corner[2] and corner[2] <= self.z[1]):
            # print("Overlap at %s" % corner)
            xSplits = self.splitX(corner[0])
            ySplits = []
            for xSplit in xSplits:
                ySplits.extend(xSplit.splitY(corner[1]))
            zSplits = []
            for ySplit in ySplits:
                zSplits.extend(ySplit.splitZ(corner[2]))
            return zSplits
        else:
            return [self]

    def subtract(self, other):
        selfCubes = [self]
        for c in other.corners():
            newSelfCubes = []
            for selfCube in selfCubes:
                newElts = selfCube.splitAtCornerIfOverlap(c)
                for newElt in newElts:
                    if not newElt.isWithin(other) and not newElt.isInvalid():
                        newSelfCubes.append(newElt)
            selfCubes = newSelfCubes
        # return selfCubes
        return unionize(selfCubes)

    def getOverlapCube(self, other):
        unionCube = Cube([
            [max(self.x[0], other.x[0]), min(self.x[1], other.x[1])],
            [max(self.y[0], other.y[0]), min(self.y[1], other.y[1])],
            [max(self.z[0], other.z[0]), min(self.z[1], other.z[1])],
        ])
        if unionCube.isInvalid():
            return None
        return unionCube


    def isInvalid(self):
        return self.x[1] < self.x[0] or self.y[1] < self.y[0] or self.z[1] < self.z[0]

def unionize(cubeArray):
    changed = True
    while changed == True:
        toRemove = []
        toAdd = []
        changed = False
        for i, cube1 in enumerate(cubeArray):
            if cube1 in toRemove:
                break
            for j, cube2 in enumerate(cubeArray[i+1:]):
                if cube2 in toRemove:
                    break
                # z
                if cube1.x == cube2.x and cube1.y == cube2.y and (min(cube1.z[1], cube2.z[1]) + 1 == max(cube1.z[0], cube2.z[0])):
                    toRemove.append(cube1)
                    toRemove.append(cube2)
                    toAdd.append(Cube(
                        [cube1.x, cube1.y, [min(cube1.z[0], cube2.z[0]), max(cube1.z[1], cube2.z[1])]]
                    ))
                    changed = True
                    break
                # x
                if cube1.z == cube2.z and cube1.y == cube2.y and (min(cube1.x[1], cube2.x[1]) + 1 == max(cube1.x[0], cube2.x[0])):
                    toRemove.append(cube1)
                    toRemove.append(cube2)
                    toAdd.append(Cube(
                        [[min(cube1.x[0], cube2.x[0]), max(cube1.x[1], cube2.x[1])], cube1.y, cube1.z]
                    ))
                    changed = True
                    break
                # y
                if cube1.z == cube2.z and cube1.x == cube2.x and (min(cube1.y[1], cube2.y[1]) + 1 == max(cube1.y[0], cube2.y[0])):
                    toRemove.append(cube1)
                    toRemove.append(cube2)
                    toAdd.append(Cube(
                        [cube1.x, [min(cube1.y[0], cube2.y[0]), max(cube1.y[1], cube2.y[1])], cube1.z]
                    ))
                    changed = True
                    break
        for elt in toRemove:
            cubeArray.remove(elt)
        for elt in toAdd:
            cubeArray.append(elt)
    return cubeArray


if False:
    print('\ntest\n')
    main('22.pt1Test')
if False:
    print('\ntest2\n')
    main('22.pt2Test')
if True:
    print('\nmain\n')
    main('22.input')
if False:
    print('\ndebug\n')
    main('22.debugTest')

if False:
    # Debug Test 1
    c = Cube([[0, 5], [0, 5], [0, 5]])
    print("cvol", c.volume())
    d = Cube(([2, 3], [-5, 15], [2, 3]))
    print("dvol", d.volume())
    e = c.getOverlapCube(d)
    print(e)
    print("evol", e.volume())
    print("~")
    q = c.subtract(e)
    print(q)
    vol = 0
    for elt in q:
        vol += elt.volume()
    print("qvol", vol)

if False:
    # Debug test 2
    c = Cube([[0, 5], [0, 5], [0, 5]])
    d = c.subtract(c)
    print(d)

if False:
    # Debug test 3
    # biggerOne = Cube([[-22, 28], [-29, 23], [-38, 16]])
    smallerOne = Cube([[-19,28],[18,23],[8,16]])
    subtractee = Cube([[-19,33],[18,23],[8,28]])
    overlap = smallerOne.getOverlapCube(subtractee)
    print(overlap)

# 7690165934301608
# 2758514936282235