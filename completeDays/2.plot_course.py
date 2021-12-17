with open('2.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

fwdInput = [
    int(entry[len('forward '):]) for entry in input if entry.startswith('forward ')
]
upInput = [
    int(entry[len('up '):]) for entry in input if entry.startswith('up ')
]
downInput = [
    int(entry[len('down '):]) for entry in input if entry.startswith('down ')
]

fwdDistance = sum(fwdInput)
upDistance = sum(upInput)
downDistance = sum(downInput)

print("2.1: %s" % (fwdDistance * (downDistance - upDistance)))

aim, depth, dist = (0, 0, 0)
for entry in input:
    if entry.startswith('forward '):
        parseVal = int(entry[len('forward '):])
        dist += parseVal
        depth += parseVal * aim
    if entry.startswith('up '):
        parseVal = int(entry[len('up '):])
        # depth -= parseVal
        aim -= parseVal
    if entry.startswith('down '):
        parseVal = int(entry[len('down '):])
        # depth += parseVal
        aim += parseVal

print("2.1: %s" % (dist * depth))
