import copy
from itertools import product

def main():
    with open('12.test_input') as f:
        lines = f.readlines()
    testInputs = [line.rstrip() for line in lines]
    impl('test', testInputs)
    
    with open('12.input') as f:
        lines = f.readlines()
    inputs = [line.rstrip() for line in lines]
    impl('real', inputs)

def impl(case, input):
    pt1(case, input)
    pt2(case, input)

def pt1(case, input):
    grid = []
    start = [-1,-1]
    end = [-1,-1]
    visited = []
    finalDistance = -1
    for i, line in enumerate(input):
        grid.append([])
        for j, letter in enumerate(line):
            if letter == 'S':
                start = [i, j]
                letter = 'a'
            elif letter == 'E':
                end = [i, j]
                letter = 'z'
            grid[i].append(ord(letter))
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    queue = [(start, 0)]
    while len(queue) > 0:
        coords, distance = queue.pop(0)
        x = coords[0]
        y = coords[1]
        if [x,y] == end:
            finalDistance = distance
            break
        height = grid[x][y]
        if x > 0 and not visited[x-1][y] and grid[x-1][y] - height <= 1:
            queue.append(([x-1, y], distance+1))
            # print(distance)
            visited[x-1][y] = distance
        if x < len(grid)-1 and not visited[x+1][y] and grid[x+1][y] - height <= 1:
            queue.append(([x+1, y], distance+1))
            # print(distance)
            visited[x+1][y] = distance
        if y > 0 and not visited[x][y-1] and grid[x][y-1] - height <= 1:
            queue.append(([x, y-1], distance+1))
            # print(distance)
            visited[x][y-1] = distance
        if y < len(grid[0])-1 and not visited[x][y+1] and grid[x][y+1] - height <= 1:
            queue.append(([x, y+1], distance+1))
            # print(distance)
            visited[x][y+1] = distance
    
    print('%s pt1: %s' % (case, finalDistance))

def pt2(case, input):
    grid = []
    start = [-1,-1]
    visited = []
    finalDistance = -1
    for i, line in enumerate(input):
        grid.append([])
        for j, letter in enumerate(line):
            if letter == 'S':
                letter = 'a'
            if letter == 'E':
                start = [i, j]
                letter = 'z'
            grid[i].append(ord(letter))
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    queue = [(start, 0)]
    while len(queue) > 0:
        coords, distance = queue.pop(0)
        x = coords[0]
        y = coords[1]
        if grid[x][y] == ord('a'):
            finalDistance = distance
            break
        height = grid[x][y]
        if x > 0 and not visited[x-1][y] and grid[x-1][y] - height >= -1:
            queue.append(([x-1, y], distance+1))
            # print(distance)
            visited[x-1][y] = distance
        if x < len(grid)-1 and not visited[x+1][y] and grid[x+1][y] - height >= -1:
            queue.append(([x+1, y], distance+1))
            # print(distance)
            visited[x+1][y] = distance
        if y > 0 and not visited[x][y-1] and grid[x][y-1] - height >= -1:
            queue.append(([x, y-1], distance+1))
            # print(distance)
            visited[x][y-1] = distance
        if y < len(grid[0])-1 and not visited[x][y+1] and grid[x][y+1] - height >= -1:
            queue.append(([x, y+1], distance+1))
            # print(distance)
            visited[x][y+1] = distance
    
    print('%s pt2: %s' % (case, finalDistance))

main()