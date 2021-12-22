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
            print("Reading instruction %s [%s] [%s]" % (i, "on" if instruction[0] else "off", instruction[1]))
            # Add:
            if instruction[0] == 1:
                # Check corners
                newCubes = [Cube(instruction[1])]
                #print("Corners")
                for c in cubes:
                    for corner in c.corners():
                        nextNewCubes = []
                        for newCube in newCubes:
                            nextNewCubes.extend(newCube.splitAtCornerIfOverlap(corner))
                        newCubes = nextNewCubes
                
                # Edges
                #print("Edges")
                for other in cubes:
                    nextNewCubes = []
                    for new in newCubes:
                        nextNewCubes.extend(new.splitAtEdgeIfEdgeOverlap(other))
                    newCubes = nextNewCubes

                prunedNewCubes = []
                # print("Prunes")
                for newCube in newCubes:
                    isGood = True
                    for cube in cubes:
                        if newCube.isWithin(cube):
                            isGood = False
                            # print("Prune %s" % newCube)
                            break
                    if isGood:
                        prunedNewCubes.append(newCube)
                cubes.extend(prunedNewCubes)
            # subtract:
            else:
                thisNegativeCube = Cube(instruction[1])
                # print("Corners")
                for corner in thisNegativeCube.corners():
                    allSplitCubes = []
                    for cube in cubes:
                        splitCubes = cube.splitAtCornerIfOverlap(corner)
                        for splitCube in splitCubes:
                            if not splitCube.isWithin(thisNegativeCube):
                                # print("%s is not within %s" % (splitCube, thisNegativeCube))
                                allSplitCubes.append(splitCube)
                            else:
                                # print("Pruning %s" % splitCube)
                                pass
                    cubes = allSplitCubes
            # Simplify:
            # TODO

        vol = 0
        for cube in cubes:
            vol += cube.volume()
            # print(cube)
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

    def edges(self):
        return {
            # X edges
            'x': [
                [[self.x[0], self.y[0], self.z[0]], [self.x[1], self.y[0], self.z[0]]],
                [[self.x[0], self.y[1], self.z[0]], [self.x[1], self.y[1], self.z[0]]],
                [[self.x[0], self.y[0], self.z[1]], [self.x[1], self.y[0], self.z[1]]],
                [[self.x[0], self.y[1], self.z[1]], [self.x[1], self.y[1], self.z[1]]],
            ],
            # Y edges
            'y': [
                [[self.x[0], self.y[0], self.z[0]], [self.x[0], self.y[1], self.z[0]]],
                [[self.x[1], self.y[0], self.z[0]], [self.x[1], self.y[1], self.z[0]]],
                [[self.x[0], self.y[0], self.z[1]], [self.x[0], self.y[1], self.z[1]]],
                [[self.x[1], self.y[0], self.z[1]], [self.x[1], self.y[1], self.z[1]]],
            ],
            # Z edges
            'z': [
                [[self.x[0], self.y[0], self.z[0]], [self.x[0], self.y[0], self.z[1]]],
                [[self.x[1], self.y[0], self.z[0]], [self.x[1], self.y[0], self.z[1]]],
                [[self.x[0], self.y[1], self.z[0]], [self.x[0], self.y[1], self.z[1]]],
                [[self.x[1], self.y[1], self.z[0]], [self.x[1], self.y[1], self.z[1]]],
            ],
        }
    
    def volume(self):
        x = self.x[1]-self.x[0]+1
        y = self.y[1]-self.y[0]+1
        z = self.z[1]-self.z[0]+1
        return x*y*z
        

    def splitX(self, x):
        if x <= self.x[0] or x > self.x[1]:
            return [self]
        cubeL = Cube([[self.x[0], x-1], self.y, self.z])
        cubeM = Cube([[x,x], self.y, self.z])
        cubeR = Cube([[x+1, self.x[1]], self.y, self.z])
        return [cubeL, cubeM, cubeR]

    def splitY(self, y):
        if y <= self.y[0] or y > self.y[1]:
            return [self]
        cubeU = Cube([self.x, [self.y[0], y-1], self.z])
        cubeM = Cube([self.x, [y,y], self.z])
        cubeD = Cube([self.x, [y+1, self.y[1]], self.z])
        return [cubeU, cubeM, cubeD]

    def splitZ(self, z):
        if z <= self.z[0] or z > self.z[1]:
            return [self]
        cubeF = Cube([self.x, self.y, [self.z[0], z-1]])
        cubeM = Cube([self.x, self.y, [z,z]])
        cubeB = Cube([self.x, self.y, [z+1, self.z[1]]])
        return [cubeF, cubeM, cubeB]

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

    def splitAtEdgeIfEdgeOverlap(self, other):
        unionCube = Cube([
            [max(self.x[0], other.x[0]), min(self.x[1], other.x[1])],
            [max(self.y[0], other.y[0]), min(self.y[1], other.y[1])],
            [max(self.z[0], other.z[0]), min(self.z[1], other.z[1])],
        ])
        if unionCube == self or unionCube == other or unionCube.isInvalid():
            return [self]
        selfCubes = [self]
        for corner in unionCube.corners():
            newSelfCubes = []
            for cube in selfCubes:
                newSelfCubes.extend(cube.splitAtCornerIfOverlap(corner))
            selfCubes = newSelfCubes
        if selfCubes != [self]:
            print("New splits")
        return selfCubes

    def getOverlapCube(self, other):
        unionCube = Cube([
            [max(self.x[0], other.x[0]), min(self.x[1], other.x[1])],
            [max(self.y[0], other.y[0]), min(self.y[1], other.y[1])],
            [max(self.z[0], other.z[0]), min(self.z[1], other.z[1])],
        ])
        if unionCube == self or unionCube == other or unionCube.isInvalid():
            return None
        print(unionCube)
        return unionCube


    def isInvalid(self):
        return self.x[1] < self.x[0] or self.y[1] < self.y[0] or self.z[1] < self.z[0]
            

if False:
    print('\nsmall test\n')
    main('22.smallTest')
if False:
    print('\ntest\n')
    main('22.test')
if False:
    print('\ntest2\n')
    main('22.test2')
if False:
    print('\nmain\n')
    main('22.input')
if False:
    print('\ndebug\n')
    main('22.debugTest')

if True:
    c = Cube([[0, 5], [0, 5], [0, 5]])
    d = Cube(([2, 3], [-5, 15], [2, 3]))
    e = c.getOverlapCube(d)
    print(e)
# 7690165934301608
# 2758514936282235