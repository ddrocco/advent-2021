class Solution(object):
    end = (None, None)

    def __init__(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        self.input = [line.strip() for line in lines]
        # print(self.input)

        # d, x, y
        self.end=(len(self.input[0])-1, len(self.input)-1)
        dist = self.calcPath()
        print("Part 1 -- " + str(dist))

        self.fixInputForPart2()
        dist = self.calcPath()
        print("Part 2 -- " + str(dist))

    def calcPath(self):
        start=(0,0,0)
        visitQueue = [start]
        # What's a Set?  A hashmap of empty or True?
        visited = {}

        while visitQueue:
            currDist, x, y = visitQueue.pop()
            if visited.get((x, y)):
                continue
            if ((x,y)) == self.end:
                return currDist
            visited[(x,y)] = currDist
            toVisits = self.get4Around(x, y)
            newVisits = []
            for toVisit in toVisits:
                visitX = toVisit[0]
                visitY = toVisit[1]
                if visited.get((visitX, visitY)) == None:
                    newVisits.append((currDist + int(self.input[visitY][visitX]), visitX, visitY))
            for newVisit in newVisits:
                if visitQueue:
                    placed = False
                    for i, visitElt in enumerate(visitQueue):
                        # Fuck it, it's an O(n) priority queue
                        if visitElt[0] < newVisit[0]:
                            visitQueue = visitQueue[0:i] + [newVisit] + visitQueue[i:]
                            placed = True
                            break
                    if not placed:
                        # Somehow forgetting this was the bug that it took me longest to find.
                        visitQueue += [newVisit]
                else:
                    visitQueue = [newVisit]
        return -1

    def get4Around(self, x, y):
        fourAround = []
        if y > 0:
            fourAround.append((x, y-1))
        if y < self.end[1]:
            fourAround.append((x, y+1))
        if x > 0:
            fourAround.append((x-1, y))
        if x < self.end[0]:
            fourAround.append((x+1, y))
        return fourAround

    def fixInputForPart2(self):
        newInput = []
        for yOffset in range(5):
            for y in range(self.end[1]+1):
                newInputRow = ''
                for xOffset in range(5):
                    for x in range(self.end[0]+1):
                        # Let's recompute the string every time because why not
                        newInputRow += digitPlusOffset(self.input[y][x], yOffset + xOffset)
                newInput.append(newInputRow)
        self.input = newInput
        self.end = (len(self.input[0])-1, len(self.input)-1)

def digitPlusOffset(c, offset):
    digit = int(c) + offset
    while digit > 9:
        digit -= 9
    return str(digit)

print('\ntest\n')
Solution('15.test')
print('\nmain\n')
Solution('15.input')