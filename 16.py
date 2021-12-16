import math

bitmap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

inverseBitmap = {
    v: k for k, v in bitmap.iteritems()
}

class Packet(object):
    def __init__(self, bits):
        self.version = None
        self.typeID = None
        self.src = ''
        self.data = []

        if len(bits) < 6:
            return

        versionInput = '0' + bits[:3]
        self.version = inverseBitmap[versionInput]
        typeIdInput = '0' + bits[3:6]
        self.typeID = inverseBitmap[typeIdInput]

        # print("Ingesting type %s, v %s" % (self.typeID, self.version))
        if self.typeID == '4':
            self.ingestLiteral(bits)
        else:
            self.ingestOperator(bits)
        # print("Done: %s (len %s)" % (self.data, len(self.src)))


    def ingestLiteral(self, bits):
        bitsPtr = 6
        breaktime = False
        numBits = []
        while not breaktime:
            leadingBit = bits[bitsPtr]
            bitsPtr += 1
            numBits += bits[bitsPtr:bitsPtr+4]
            bitsPtr += 4
            if leadingBit == '0':
                breaktime = True
        numBits.reverse()
        numVal = 0
        for i, bit in enumerate(numBits):
            numVal += int(bit) * math.pow(2, i)
        self.data = [numVal]
        self.src = bits[:bitsPtr]

    def ingestOperator(self, bits):
        self.header = bits[6]
        # print("O - Got header %s" % self.header)
        if self.header == '0':
            self.ingestOperatorBits(bits)
        else:
            self.ingestOperatorPackets(bits)

    def ingestOperatorBits(self, bits):
        rawLengthOfSubPackets = [c for c in bits[7:22]]
        rawLengthOfSubPackets.reverse()
        lengthOfSubPackets = 0
        for i, bit in enumerate(rawLengthOfSubPackets):
            lengthOfSubPackets += int(bit) * math.pow(2, i)
        # print("OB - Got %s length for subpackets" % lengthOfSubPackets)
        
        bitPtr = 22
        while bitPtr < 22 + lengthOfSubPackets:
            # print("OB - New subpacket at %s (/%s)" % (bitPtr, len(bits)))
            newPacket = Packet(bits[bitPtr:])
            self.data.append(newPacket)
            bitPtr += len(newPacket.src)
        self.src += bits[:bitPtr]
    
    def ingestOperatorPackets(self, bits):
        rawNumberOfSubPackets = [c for c in bits[7:18]]
        rawNumberOfSubPackets.reverse()
        numberOfSubPackets = 0
        for i, bit in enumerate(rawNumberOfSubPackets):
            numberOfSubPackets += int(bit) * math.pow(2, i)
        # print("OP - Got %s subpackets" % numberOfSubPackets)

        bitPtr = 18
        for i in range(int(numberOfSubPackets)):
            # print("OP - New subpacket at %s (/%s)" % (bitPtr, len(bits)))
            newPacket = Packet(bits[bitPtr:])
            self.data.append(newPacket)
            bitPtr += len(newPacket.src)
        self.src += bits[:bitPtr]

    def getVersionSum(self):
        if self.typeID == '4':
            return int(self.version)
        return int(self.version) + sum([entry.getVersionSum() for entry in self.data])

    def execute(self):
        if self.typeID == '0':
            #sum
            return sum([entry.execute() for entry in self.data])
        if self.typeID == '1':
            #prod
            val = 1
            for entry in self.data:
                val *= entry.execute()
            return val
        if self.typeID == '2':
            #min
            return min([entry.execute() for entry in self.data])
        if self.typeID == '3':
            #max
            return max([entry.execute() for entry in self.data])
        if self.typeID == '4':
            #num
            return self.data[0]
        if self.typeID == '5':
            # greater than
            if self.data[0].execute() > self.data[1].execute():
                return 1
            return 0
        if self.typeID == '6':
            # less than
            if self.data[0].execute() < self.data[1].execute():
                return 1
            return 0
        if self.typeID == '7':
            # equal to
            if self.data[0].execute() == self.data[1].execute():
                return 1
            return 0

class Solution(object):
    def __init__(self, filename):
        self.bits = ''
        self.input = None
        self.packets = []

        with open(filename) as f:
            lines = f.readlines()
        self.input = [line.strip() for line in lines][0]
        # print(self.input)
        for c in self.input:
            self.bits += bitmap.get(c)
        # print(self.bits)

        packet = Packet(self.bits)
        print("PT1  %s" % packet.getVersionSum())
        print("PT2  %s" % packet.execute())

print('\ntest1\n')
Solution('16.test1')
print('\ntest2\n')
Solution('16.test2')
print('\ntest3\n')
Solution('16.test3')
print('\ntest4\n')
Solution('16.test4')
print('\ntest5\n')
Solution('16.test5')
print('\nmain\n')
Solution('16.input')