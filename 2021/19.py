def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    
    currScannerName = None
    currBeacons = []
    scanners = []
    for elt in input:
        if elt.startswith('--- scanner '):
            if currScannerName != None:
                scanners.append(Scanner(currScannerName, currBeacons))
                currBeacons = []
            currScannerName = elt[len('--- scanner '):-len(' ---')]
        elif elt != '':
            currBeacons.append([int(e) for e in elt.split(',')])
    scanners.append(Scanner(currScannerName, currBeacons))

    masterMap = MasterMap(scanners)
    while masterMap.unmappedScanners:
        mmn = len(masterMap.mappedScanners)
        masterMap.align()
        newMmn = len(masterMap.mappedScanners)
        if mmn == newMmn:
            print("Failure")
            print(masterMap)
            break
        else:
            print("Got %s" % newMmn)
    print(len(masterMap.getBeacons()))
    print(masterMap.maxManhattan())

fwdOrientations = ['+x', '-x', '+y', '-y', '+z', '-z']
orientations = {
    '+x': [
        [(1, 0), (1, 1), (1, 2)], # CONFIRMED +x +y +z 
        [(1, 0), (-1, 1), (-1, 2)], # +x -y -z
        [(1, 0), (1, 2), (-1, 1)], # +x +z -y
        [(1, 0), (-1, 2), (1, 1)], # +x -z +y
    ],
    '-x': [
        [(-1, 0), (1, 1), (-1, 2)], # CONFIRMED
        [(-1, 0), (-1, 1), (1, 2)],
        [(-1, 0), (1, 2), (1, 1)],
        [(-1, 0), (-1, 2), (-1, 1)],
    ],
    '+y': [
        [(1, 1), (1, 2), (1, 0)], # +y +z +x
        [(1, 1), (-1, 2), (-1, 0)], # +y -z -x
        [(1, 1), (1, 0), (-1, 2)], # +y +x -z
        [(1, 1), (-1, 0), (1, 2)], # +y -x +z
    ],
    '-y': [
        [(-1, 1), (1, 2), (-1, 0)],
        [(-1, 1), (-1, 2), (1, 0)],
        [(-1, 1), (1, 0), (1, 2)],
        [(-1, 1), (-1, 0), (-1, 2)],
    ],
    '+z': [
        [(1, 2), (1, 1), (-1, 0)], # +z +y -x
        [(1, 2), (-1, 1), (1, 0)], # +z -y +x
        [(1, 2), (1, 0), (1, 1)], # +z +x +y
        [(1, 2), (-1, 0), (-1, 1)], # +z -x -y
    ],
    '-z': [
        [(-1, 2), (1, 1), (1, 0)],
        [(-1, 2), (-1, 1), (-1, 0)],
        [(-1, 2), (1, 0), (-1, 1)],
        [(-1, 2), (-1, 0), (1, 1)],
    ],
}

class Scanner(object):
    def __init__(self, name, beacons):
        self.name = name
        self.beacons = beacons

    def findOverlap(self, other):
        for fwdOrientation in fwdOrientations:
            for o in orientations[fwdOrientation]:
                otherBeaconsDimensionalized = [
                    [o[0][0] * beacon[o[0][1]], o[1][0] * beacon[o[1][1]], o[2][0] * beacon[o[2][1]]]
                    for beacon in other.beacons
                ]
                dimensionalityOffsets = {}
                for sBeacon in self.beacons:
                    for oBeacon in otherBeaconsDimensionalized:
                        diff = (sBeacon[0]-oBeacon[0], sBeacon[1]-oBeacon[1], sBeacon[2]-oBeacon[2])
                        dimensionalityOffsets[diff] = dimensionalityOffsets.get(diff, 0) + 1
                for k, v in dimensionalityOffsets.iteritems():
                    if v >= 12:
                        other.beacons = otherBeaconsDimensionalized
                        return k, o
                #print("\n\nOffsets: %s\n" % o)
                for k, v in dimensionalityOffsets.iteritems():
                    pass
                    #print("%s: %s" % (k, v))
        return False, None

    def __repr__(self):
        return 'Scanner %s\n\n%s\n\n' % (self.name, self.beacons)

class MappedScanner(object):
    def __init__(self, scanner, orientation, x, y, z):
        self.scanner = scanner
        self.x = x
        self.y = y
        self.z = z
        self.orientation = orientation

    def __repr__(self):
        return "{%s,%s,%s} // {%s} : %s" % (self.x, self.y, self.z, self.orientation, self.scanner)

class MasterMap(object):
    def __init__(self, scanners):
        self.unmappedScanners = scanners[1:]
        self.mappedScanners = [MappedScanner(scanners[0], orientations['+x'], 0, 0, 0)]

    def align(self):
        for scanner1 in self.unmappedScanners:
            for mappedScanner in self.mappedScanners:
                scanner2 = mappedScanner.scanner
                offsetIfAny, orientation = scanner2.findOverlap(scanner1)
                if offsetIfAny:
                    self.mappedScanners.append(MappedScanner(
                        scanner1,
                        orientation,
                        mappedScanner.x + offsetIfAny[0],
                        mappedScanner.y + offsetIfAny[1],
                        mappedScanner.z + offsetIfAny[2],
                    ))
                    self.unmappedScanners.remove(scanner1)
                    return
    
    def getBeacons(self):
        beacons = {}
        for ms in self.mappedScanners:
            for b in ms.scanner.beacons:
                beacons[(b[0] + ms.x, b[1] + ms.y, b[2] + ms.z)] = True
        return beacons.keys()

    def maxManhattan(self):
        maxD = 0
        for i, ms in enumerate(self.mappedScanners):
            for oms in self.mappedScanners[i+1:]:
                distance = abs(ms.x - oms.x) + abs(ms.y - oms.y) + abs(ms.z - oms.z)
                maxD = max(distance, maxD)
        return maxD



    def __repr__(self):
        return "UNMAPPED SCANNERS: %s\n\nMAPPED SCANNERS: %s" % (self.unmappedScanners, self.mappedScanners)



#print('\ntest\n')
#main('19.test')
print('\nmain\n')
main('19.input')