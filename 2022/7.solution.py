import copy

def main():
    with open('7.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)
    pass
    
    with open('7.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    rootDir = getRootDir(input)
    res1 = sum(rootDir.getAllInSize())
    res2 = pt2(rootDir)
    
    print('%s pt1: %s' % (case, res1))
    print('%s pt2: %s' % (case, res2))

def getRootDir(input):
    root = directory()
    currDirs = []
    lineNum = 0
    while lineNum < len(input):
        line = input[lineNum]
        if line[0] == '$':
            if line.split(' ')[1] == 'cd':
                if line.split(' ')[2] == '/':
                    currDirs = []
                    lineNum += 1
                elif line.split(' ')[2] == '..':
                    currDirs = currDirs[:-1]
                    lineNum += 1
                else:
                    currDirs.append(line.split(' ')[2])
                    lineNum += 1
            elif line.split(' ')[1] == 'ls':
                dirObj = root
                for cd in currDirs:
                    dirObj = dirObj.dir[cd]
                lineNum += 1
                while lineNum < len(input) and input[lineNum][0] != '$':
                    if input[lineNum][:3] == 'dir':
                        dirObj.append(input[lineNum].split(' ')[1], directory())
                        lineNum += 1
                    else:
                        dirObj.append(input[lineNum].split(' ')[1], int(input[lineNum].split(' ')[0]))
                        lineNum += 1
    return root

def pt2(root):
    totSize = 70000000
    neededSize = 30000000
    rootSize = root.size()
    currentlyAvailable = totSize - rootSize
    mustDelete = neededSize - currentlyAvailable
    return min(root.getAllAtLeast(mustDelete))

class directory(object):
    def __init__(self):
        self.dir = {}

    def size(self):
        runningSize = 0
        for k in self.dir:
            v = self.dir[k]
            if isinstance(v, int):
                runningSize += v
            elif isinstance(v, directory):
                runningSize += v.size()
        return runningSize

    def append(self, k, v):
        self.dir[k] = v

    def getAllInSize(self):
        entries = []
        for k in self.dir:
            v = self.dir[k]
            if isinstance(v, directory):
                entries.extend(v.getAllInSize())
        if self.size() <= 100000:
            entries.append(self.size())
        return entries

    def getAllAtLeast(self, atLeastSize):
        entries = []
        for k in self.dir:
            v = self.dir[k]
            if isinstance(v, directory):
                entries.extend(v.getAllAtLeast(atLeastSize))
        if self.size() >= atLeastSize:
            entries.append(self.size())
        return entries


'''def pt2(input):
    runningStr = [' '] * 14
    for i, c in enumerate(input):
        runningStr = runningStr[1:]
        runningStr.append(c)
        if ' ' not in runningStr:
            if numUnique(runningStr) == 14:
                return i+1
    return -1'''

main()