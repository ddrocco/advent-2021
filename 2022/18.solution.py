from util.set import set

TEST_PT_1 = True
PROD_PT_1 = True
TEST_PT_2 = True
PROD_PT_2 = True

Q_NUM = 18

def main():
    with open('%s.test_input' % Q_NUM) as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs, TEST_PT_1, TEST_PT_2)
    
    with open('%s.input' % Q_NUM) as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs, PROD_PT_1, PROD_PT_2)

def impl(case, input, doPt1, doPt2):
    if doPt1:
        cubes = pt1(case, input)
        if doPt2:
            pt2(case, cubes)
    return

def pt1(case, input):
    cubes = set([])
    totalSurfaceArea = 0
    for line in input:
        dims = line.split(",")
        x = int(dims[0])
        y = int(dims[1])
        z = int(dims[2])
        newSurfaceArea = 0
        for d in [
            (x-1,y,z),(x+1,y,z),
            (x,y-1,z),(x,y+1,z),
            (x,y,z-1),(x,y,z+1),
        ]:
            if cubes.has(d):
                newSurfaceArea -= 1
            else:
                newSurfaceArea += 1
        cubes.add((x,y,z))
        totalSurfaceArea += newSurfaceArea
    print('%s pt1: %s' % (case, totalSurfaceArea))
    return cubes

def pt2(case, lavaCubes):
    minX = 10000
    minY = 10000
    minZ = 10000
    maxX = -10000
    maxY = -10000
    maxZ = -10000
    for k in lavaCubes.underlyingData:
        minX = min(k[0], minX)
        maxX = max(k[0], maxX)
        minY = min(k[1], minY)
        maxY = max(k[1], maxY)
        minZ = min(k[2], minZ)
        maxZ = max(k[2], maxZ)
    minX -= 1
    minY -= 1
    minZ -= 1
    maxX += 1
    maxY += 1
    maxZ += 1
    visitedCubes = set([(minX, minY, minZ)])
    visitQueue = [(minX, minY, minZ)]
    coolFaces = 0
    # Traverse visit queue.  Whenever encountering a lava cube, add a face.  That's it.
    while len(visitQueue) > 0:
        x,y,z = visitQueue.pop()
        for d in [
            (x-1,y,z),(x+1,y,z),
            (x,y-1,z),(x,y+1,z),
            (x,y,z-1),(x,y,z+1),
        ]:
            if lavaCubes.has(d):
                coolFaces += 1
            elif not visitedCubes.has(d) and minX <= x and maxX >= x and minY <= y and maxY >= y and minZ <= z and maxZ >= z:
                visitQueue.append(d)
                visitedCubes.add(d)
    print('%s pt2: %s' % (case, coolFaces))






main()