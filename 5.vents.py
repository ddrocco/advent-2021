with open('5.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

#print(input)

# Part 1
allVentries = {}
for entry in input:
    startAndEnd = entry.split(' -> ')
    start = startAndEnd[0]
    end = startAndEnd[1]
    startX = start.split(',')[0]
    startY = start.split(',')[1]
    endX = end.split(',')[0]
    endY = end.split(',')[1]
    #print("Parsing %s,%s to %s,%s" % (startX, startY, endX, endY))
    if startX == endX:
        lowY = min(int(startY), int(endY))
        highY = max(int(startY), int(endY))
        for i in range(lowY, highY+1):
            key = '%s,%s' % (startX, i)
            #print(key)
            allVentries[key] = allVentries.get(key, 0) + 1
    elif startY == endY:
        lowX = min(int(startX), int(endX))
        highX = max(int(startX), int(endX))
        for i in range(lowX, highX+1):
            key = '%s,%s' % (i, startY)
            #print(key)
            allVentries[key] = allVentries.get(key, 0) + 1
bigVentries = {
    k: v for k, v in allVentries.items() if v > 1
}
#print('')
#allVentryList = list(allVentries)
#allVentryList.sort()
#print(allVentryList)
#print('')
#bigVentryList = list(bigVentries)
#bigVentryList.sort()
#print(bigVentryList)

#print('')
print(len(bigVentries))

# Part 2
allVentries = {}
for entry in input:
    startAndEnd = entry.split(' -> ')
    start = startAndEnd[0]
    end = startAndEnd[1]
    startX = int(start.split(',')[0])
    startY = int(start.split(',')[1])
    endX = int(end.split(',')[0])
    endY = int(end.split(',')[1])
    #print("Parsing %s,%s to %s,%s" % (startX, startY, endX, endY))
    if startX == endX:
        lowY = min(int(startY), int(endY))
        highY = max(int(startY), int(endY))
        for i in range(lowY, highY+1):
            key = '%s,%s' % (startX, i)
            #print(key)
            allVentries[key] = allVentries.get(key, 0) + 1
    elif startY == endY:
        lowX = min(int(startX), int(endX))
        highX = max(int(startX), int(endX))
        for i in range(lowX, highX+1):
            key = '%s,%s' % (i, startY)
            #print(key)
            allVentries[key] = allVentries.get(key, 0) + 1
    else:
        # print("Parsing %s,%s to %s,%s" % (startX, startY, endX, endY))
        lowX = min(int(startX), int(endX))
        highX = max(int(startX), int(endX))
        lowY = min(int(startY), int(endY))
        highY = max(int(startY), int(endY))
        if startX == lowX and startY == lowY or startX == highX and startY == highY:
            # both climb together
            # print("together")
            for i, x in enumerate(range(int(lowX), int(highX)+1)):
                key = '%s,%s' % (x, int(lowY) + i)
                # print(key)
                allVentries[key] = allVentries.get(key, 0) + 1
        else:
            # climb opposite
            # print("opposite")
            for i, x in enumerate(range(int(lowX), int(highX)+1)):
                key = '%s,%s' % (x, int(highY) - i)
                # print(key)
                allVentries[key] = allVentries.get(key, 0) + 1
bigVentries = {
    k: v for k, v in allVentries.items() if v > 1
}
print(len(bigVentries))