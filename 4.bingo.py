import math
import copy

with open('4.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

class Board(object):
    def __init__(self, board):
        self.source = board
        self.picked = []
        for i in range(5):
            self.picked.append([])
            for j in range(5):
                self.picked[i].append(self.source[i][j])
    
    def getRows(self):
        return self.source
    
    def getCols(self):
        cols = []
        for i in range(5):
            cols.append([])
            for j in range(5):
                cols[i].append(self.source[j][i])
        return cols
    
    def getPickedRows(self):
        return self.picked
    
    def getPickedCols(self):
        cols = []
        for i in range(5):
            cols.append([])
            for j in range(5):
                cols[i].append(self.picked[j][i])
        return cols

    def doPrint(self):
        for row in self.getRows():
            print(row)

    def isComplete(self):
        rowSum = 0
        colSum = 0
        for row in self.getPickedRows():
            numRowCorrect = 0
            for entry in row:
                if entry == True:
                    numRowCorrect += 1
            if numRowCorrect == 5:
                return self.getSum()
        for col in self.getPickedCols():
            numColCorrect = 0
            for entry in col:
                if entry == True:
                    numColCorrect += 1
            if numColCorrect == 5:
                return self.getSum()
        return False

    def getSum(self):
        tot = 0
        for i in range(5):
            for j in range(5):
                if self.getPickedRows()[i][j] != True:
                    tot += int(self.getPickedRows()[i][j])
        return tot

    def addNumber(self, num):
        for i in range(5):
            for j in range(5):
                if self.source[i][j] == num:
                    self.picked[i][j] = True
        if self.isComplete() is not False:
            return self.isComplete() * int(num)
        return False

# Setup
numbersCalled = input[0].split(',')
boards = [input[i:i+5] for i in range(2, len(input), 6)]
for i, board in enumerate(boards):
    for j, boardRow in enumerate(board):
        boards[i][j] = [num for num in boardRow.split(' ') if num != '']
    boards[i] = Board(boards[i])

# Part 1
for numberCalled in numbersCalled:
    print("CALLING %s" % numberCalled)
    biggestVal = 0
    for board in boards:
        val = board.addNumber(numberCalled)
        if val != False:
            if val > biggestVal:
                print(board.getPickedRows())
                biggestVal = val
    if biggestVal != 0:
        break
print(biggestVal)

# Part 2
for numberCalled in numbersCalled:
    print("CALLING %s" % numberCalled)
    boardsToRemove = []
    val = 0
    for board in boards:
        val = board.addNumber(numberCalled)
        if val != False:
            boardsToRemove.append(board)
    if val != 0 and len(boards) == 1:
        break
    for board in boardsToRemove:
        boards.remove(board)
print(val)

            