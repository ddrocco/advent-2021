def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    parsedInput = [parse(None, elt) for elt in input]
    
    # Part 1
    currSnailPair = parsedInput[0]
    for elt in parsedInput[1:]:
        currSnailPair = currSnailPair.add(elt)
    print(currSnailPair.magnitude())

    # Part 2
    greatestMagnitude = 0
    for i, eltA in enumerate(input):
        for eltB in input[i+1:]:
            for config in [(eltA, eltB), (eltB, eltA)]:
                pairA = parse(None, config[0])
                pairB = parse(None, config[1])
                newPair = pairA.add(pairB)
                magnitude = newPair.magnitude()
                greatestMagnitude = max(magnitude, greatestMagnitude)
    print(greatestMagnitude)

def parse(snailParent, input):
    if input == None:
        return
    if isinstance(input, SnailPair):
        return input
    if input[0] == '[':
        lBracketCount = 0
        for i, c in enumerate(input[0:]):
            if c == '[':
                lBracketCount += 1
            elif c == ']':
                lBracketCount -= 1
            if c == ',' and lBracketCount == 1:
                return SnailPair(snailParent, input[1:i], input[i+1:-1])
    else:
        return SnailInt(snailParent, input[0])

class SnailThang(object):
    def __init__(self, parent):
        self.parent = parent

    @property
    def layer(self):
        if self.parent == None:
            return 0
        else:
            return self.parent.layer + 1

    def getLeftInt(self):
        if self.parent == None:
            return None
        if self == self.parent.elt1: # This is the left element.
            return self.parent.getLeftInt()
        currElt = self.parent.elt1
        # Go right until we get the rightmost elt.
        while not isinstance(currElt, SnailInt):
            currElt = currElt.elt2
        return currElt

    def getRightInt(self):
        if self.parent == None:
            return None
        if self == self.parent.elt2: # This is the right element.
            return self.parent.getRightInt()
        currElt = self.parent.elt2
        # Go left until we get the leftmost elt.
        while not isinstance(currElt, SnailInt):
            currElt = currElt.elt1
        return currElt

class SnailInt(SnailThang):
    def __init__(self, parent, val):
        if parent == None:
            raise Exception("Can't have snailint of None.")
        super(SnailInt, self).__init__(parent)
        self.val = int(val)

    def reduceSplit(self):
        # Split if val >= 10
        if self.val >= 10:
            self.split()
            return True
        else:
            return False

    def reduceExplode(self):
        return False

    def split(self):
        # print("split", self)
        newPair = SnailPair(self.parent, None, None)
        if self.parent.elt1 == self:
            self.parent.elt1 = newPair
        elif self.parent.elt2 == self:
            self.parent.elt2 = newPair
        else:
            raise Exception("Tried to split without parent")
        newPair.elt1 = SnailInt(newPair, self.val / 2)
        newPair.elt2 = SnailInt(newPair, (self.val + 1)/2)

    def __repr__(self):
        return str(self.val)

    def magnitude(self):
        return self.val

class SnailPair(SnailThang):
    def __init__(self, parent, elt1, elt2):
        super(SnailPair, self).__init__(parent)
        self.elt1 = parse(self, elt1)
        self.elt2 = parse(self, elt2)
    
    def __repr__(self):
        return '[%s, %s]' % (self.elt1, self.elt2)

    def add(self, newSnailPair):
        if self.parent != None or newSnailPair.parent != None:
            raise Exception("Parented snail pair merged")
        retPair = SnailPair(None, self, newSnailPair)
        self.parent = retPair
        newSnailPair.parent = retPair
        while retPair.reduce():
            # print(retPair)
            pass
        return retPair

    def reduce(self):
        if self.reduceExplode():
            return True
        if self.reduceSplit():
            return True

    def reduceSplit(self):        
        if self.elt1.reduceSplit():
            return True
        
        if self.elt2.reduceSplit():
            return True

    def reduceExplode(self):
        # Explode if layer >= 4
        if self.layer >= 4:
            self.explode()
            return True
        
        if self.elt1.reduceExplode():
            return True
        
        if self.elt2.reduceExplode():
            return True
    
    def explode(self):
        # print("explode", self)
        leftInt = self.getLeftInt()
        rightInt = self.getRightInt()
        if leftInt != None:
            leftInt.val += self.elt1.val
        if rightInt != None:
            rightInt.val += self.elt2.val
        if self.parent.elt1 == self:
            self.parent.elt1 = SnailInt(self.parent, 0)
        else:
            self.parent.elt2 = SnailInt(self.parent, 0)

    def magnitude(self):
        return 3 * self.elt1.magnitude() + 2 * self.elt2.magnitude()



print('\ntest\n')
main('18.test')
print('\nmain\n')
main('18.input')