from util.set import set
import re

TEST_PT_1 = False
PROD_PT_1 = False
TEST_PT_2 = False
PROD_PT_2 = True
global BEST_GEODES
BEST_GEODES = 0

Q_NUM = 19

def main():
    with open('%s.test_input' % Q_NUM) as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs, TEST_PT_1, TEST_PT_2)
    
    with open('%s.input' % Q_NUM) as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs, PROD_PT_1, PROD_PT_2)

def impl(case, input, doPt1, doPt2):
    if doPt1:
        pt1(case, input)
    if doPt2:
        pt2(case, input)

def pt1(case, input):
    res = 0
    for line in input:
        bpNum = int(line.split(":")[0][len("Blueprint "):])
        oreOreCost = int(line.split( " ")[6])
        clayOreCost = int(line.split( " ")[12])
        obsOreCost = int(line.split( " ")[18])
        obsClayCost = int(line.split( " ")[21])
        geodeOreCost = int(line.split( " ")[27])
        geodeObsCost = int(line.split( " ")[30])

        # ore, clay, obsidian, geodes
        robots = [1, 0, 0, 0]
        resources = [0, 0, 0, 0]
        costs = costsStruct(oreOreCost, clayOreCost, obsOreCost, obsClayCost, geodeOreCost, geodeObsCost)
        geodes = optimizeRobots(24, robots, resources, costs)
        res += bpNum * geodes
        print("\t%s - %d got %d geodes; +%d=%d" % (case, bpNum, geodes, bpNum * geodes, res))
    print('%s pt1: %s' % (case, res))

class costsStruct():
    def __init__(self, oreOreCost, cOreCost, obsOreCost, obsCCost, gOreCost, gObsCost):
        self.oreOreCost = oreOreCost
        self.cOreCost = cOreCost
        self.obsOreCost = obsOreCost
        self.obsCCost = obsCCost
        self.gOreCost = gOreCost
        self.gObsCost = gObsCost


# Returns number of geodes
def optimizeRobots(daysLeft, robots, resources, costs):
    # Option 1. Don't build any more robots.
    geodes = resources[3] + robots[3] * daysLeft
    global BEST_GEODES
    if geodes > BEST_GEODES:
        print("New max %d!" % geodes)
        BEST_GEODES = geodes

    # Option 2. Wait to build an ore[0] robot.
    if daysLeft > 3 and robots[0] < max(costs.oreOreCost, costs.cOreCost, costs.obsOreCost, costs.gOreCost):
        optionDays = daysLeft
        optionRob = copy(robots)
        optionRes = copy(resources)
        # Wait for resources if need-be
        while optionRes[0] < costs.oreOreCost:
            optionDays -= 1
            generate(optionRes, optionRob)
        # Generate while building.
        generate(optionRes, optionRob)
        optionDays -= 1
        # Build the robot
        optionRes[0] -= costs.oreOreCost
        optionRob[0] += 1
        # Ensure days left is greater than 2 (e.g. use this robot + build geode + get geode):
        if optionDays > 2:
            optionGeodes = optimizeRobots(optionDays, optionRob, optionRes, costs)
            geodes = max(geodes, optionGeodes)

    # Option 3. Wait to build a clay[1] robot.
    if daysLeft > 5 and robots[1] < costs.obsCCost:
        optionDays = daysLeft
        optionRob = copy(robots)
        optionRes = copy(resources)
        # Wait for resources if need-be
        while optionRes[0] < costs.cOreCost:
            optionDays -= 1
            generate(optionRes, optionRob)
        # Generate while building.
        generate(optionRes, optionRob)
        optionDays -= 1
        # Build the robot
        optionRes[0] -= costs.cOreCost
        optionRob[1] += 1
        # Ensure days left is greater than 4 (e.g. use this robot + build obs + get obs + build geode + get geode):
        if optionDays > 4:
            optionGeodes = optimizeRobots(optionDays, optionRob, optionRes, costs)
            geodes = max(geodes, optionGeodes)
    
    # Option 4. Wait to build an obsidian[2] robot (only if clay[1] present).
    if daysLeft > 3 and robots[1] > 0 and robots[2] < costs.gObsCost:
        optionDays = daysLeft
        optionRob = copy(robots)
        optionRes = copy(resources)
        # Wait for resources if need-be
        while optionRes[0] < costs.obsOreCost or optionRes[1] < costs.obsCCost:
            optionDays -= 1
            generate(optionRes, optionRob)
        # Generate while building.
        generate(optionRes, optionRob)
        optionDays -= 1
        # Build the robot
        optionRes[0] -= costs.obsOreCost
        optionRes[1] -= costs.obsCCost
        optionRob[2] += 1
        # Ensure days left is greater than 2 (e.g. use this robot + build + use 1 geode):
        if optionDays > 2:
            optionGeodes = optimizeRobots(optionDays, optionRob, optionRes, costs)
            geodes = max(geodes, optionGeodes)
        
    # Option 5. Wait to build a geode[3] robot (only if obsidian[2] present).
    if daysLeft > 1 and robots[2] > 0:
        optionDays = daysLeft
        optionRob = copy(robots)
        optionRes = copy(resources)
        # Wait for resources if need-be
        while optionRes[0] < costs.gOreCost or optionRes[2] < costs.gObsCost:
            optionDays -= 1
            generate(optionRes, optionRob)
        # Generate while building.
        generate(optionRes, optionRob)
        optionDays -= 1
        # Build the robot
        optionRes[0] -= costs.gOreCost
        optionRes[2] -= costs.gObsCost
        optionRob[3] += 1
        # Ensure days left is greater than 0 (e.g. use this robot):
        if optionDays > 0:
            optionGeodes = optimizeRobots(optionDays, optionRob, optionRes, costs)
            geodes = max(geodes, optionGeodes)

    return geodes

def pt2(case, input):
    res = 1
    for line in input[:3]:
        bpNum = int(line.split(":")[0][len("Blueprint "):])
        oreOreCost = int(line.split( " ")[6])
        clayOreCost = int(line.split( " ")[12])
        obsOreCost = int(line.split( " ")[18])
        obsClayCost = int(line.split( " ")[21])
        geodeOreCost = int(line.split( " ")[27])
        geodeObsCost = int(line.split( " ")[30])

        # ore, clay, obsidian, geodes
        robots = [1, 0, 0, 0]
        resources = [0, 0, 0, 0]
        costs = costsStruct(oreOreCost, clayOreCost, obsOreCost, obsClayCost, geodeOreCost, geodeObsCost)
        geodes = optimizeRobots(32, robots, resources, costs)
        res *= geodes
        print("\t%s - %d got %d geodes; =%d" % (case, bpNum, geodes, res))
    print('%s pt2: %s' % (case, res))

def get_digits(n, s):
    result = re.search('\d{%s}'%n, s)
    return result.group(0) if result else result
def copy(a):
    return [elt for elt in a]
def generate(resources, robots):
    for i, v in enumerate(robots):
        resources[i] += v

main()