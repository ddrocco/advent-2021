with open('6.input') as f:
    lines = f.readlines()
input = [line.strip() for line in lines]

print(input)

# Part 1
fishPop = {i: 0 for i in range(9)}
for entry in input[0].split(','):
    fishAge = int(entry)
    fishPop[fishAge] += 1

for i in range(80):
    newFishPop = {
        i: fishPop[i+1] for i in range(8)
    }
    newFishPop[6] += fishPop[0]
    newFishPop[8] = fishPop[0]
    fishPop = newFishPop

print(sum(fishPop.values()))

# Part 2
for i in range(256-80):
    newFishPop = {
        i: fishPop[i+1] for i in range(8)
    }
    newFishPop[6] += fishPop[0]
    newFishPop[8] = fishPop[0]
    fishPop = newFishPop
print(sum(fishPop.values()))