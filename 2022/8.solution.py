import copy

def main():
    with open('8.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)
    pass
    
    with open('8.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    grid = [[Tree(val) for val in row] for row in input]
    
    # Pt 1
    for rowNum in range(len(grid)):
        # Left to right
        soFar = -1
        for colNum in range(len(grid[0])):
            if grid[rowNum][colNum].value > soFar:
                grid[rowNum][colNum].edgeViewable = True
                soFar = grid[rowNum][colNum].value
        # Right to left
        soFar = -1
        for colNum in range(len(grid[0])-1, 0, -1):
            if grid[rowNum][colNum].value > soFar:
                grid[rowNum][colNum].edgeViewable = True
                soFar = grid[rowNum][colNum].value
    for colNum in range(len(grid[0])):
        # Top to bottom
        soFar = -1
        for rowNum in range(len(grid)):
            if grid[rowNum][colNum].value > soFar:
                grid[rowNum][colNum].edgeViewable = True
                soFar = grid[rowNum][colNum].value
        # Bottom to top
        soFar = -1
        for rowNum in range(len(grid)-1, 0, -1):
            if grid[rowNum][colNum].value > soFar:
                grid[rowNum][colNum].edgeViewable = True
                soFar = grid[rowNum][colNum].value
    # Calculate results
    numTreesVisible = 0
    for row in grid:
        for col in row:
            if col.edgeViewable == True:
                numTreesVisible += 1

    print('%s pt1: %s' % (case, numTreesVisible))

    # Pt 2
    for thisRowNum in range(len(grid)):
        for thisColNum in range(len(grid[0])):
            thisTreeHeight = grid[thisRowNum][thisColNum].value

            # Left to right
            numTrees = 0
            for colNum in range(thisColNum+1, len(grid[0])):
                if grid[thisRowNum][colNum].value < thisTreeHeight:
                    numTrees += 1
                else:
                    numTrees += 1
                    break
            grid[thisRowNum][thisColNum].rightTrees = numTrees
            # Right to left
            numTrees = 0
            for colNum in range(thisColNum-1, -1, -1):
                if grid[thisRowNum][colNum].value < thisTreeHeight:
                    numTrees += 1
                else:
                    numTrees += 1
                    break
            grid[thisRowNum][thisColNum].leftTrees = numTrees

            # Top to bottom
            numTrees = 0
            for rowNum in range(thisRowNum+1, len(grid)):
                if grid[rowNum][thisColNum].value < thisTreeHeight:
                    numTrees += 1
                else:
                    numTrees += 1
                    break
            grid[thisRowNum][thisColNum].downTrees = numTrees
            # Bottom to top
            numTrees = 0
            for rowNum in range(thisRowNum-1, -1, -1):
                if grid[rowNum][thisColNum].value < thisTreeHeight:
                    numTrees += 1
                else:
                    numTrees += 1
                    break
            grid[thisRowNum][thisColNum].upTrees = numTrees

    bestScore = 0
    for i, row in enumerate(grid):
        for j, elt in enumerate(row):
            bestScore = max(bestScore, elt.score())
    print('%s pt2: %s' % (case, bestScore))

class Tree(object):
    def __init__(self, value):
        self.value = int(value)
        self.edgeViewable = False
        self.leftTrees = 0
        self.rightTrees = 0
        self.upTrees = 0
        self.downTrees = 0
    def score(self):
        return self.leftTrees * self.rightTrees * self.upTrees * self.downTrees
    def print(self):
        print("%s: [Left %s] [Right %s] [Up %s] [Down %s]" % (self.value, self.leftTrees, self.rightTrees, self.upTrees, self.downTrees))

main()