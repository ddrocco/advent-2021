def main():
    with open('4.test_input') as f:
        lines = f.readlines()
    testInput = [line.strip() for line in lines]
    impl('test', testInput)
    
    with open('4.input') as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    impl('real', input)

def impl(case, input):
    ans1 = 0
    ans2 = 0
    for line in input:
        shifts = line.split(',')
        e1Pts = shifts[0].split('-')
        e2Pts = shifts[1].split('-')
        e1Start = int(e1Pts[0])
        e1End = int(e1Pts[1])
        e2Start = int(e2Pts[0])
        e2End = int(e2Pts[1])
        if (
            (e1Start <= e2Start and e1End >= e2End) or
            (e2Start <= e1Start and e2End >= e1End)
        ):
            ans1 +=1
            ans2 +=1
        elif (
            (e1Start >= e2Start and e1Start <= e2End) or
            (e1End >= e2Start and e1End <= e2End) or
            (e2Start >= e1Start and e2Start <= e1End) or
            (e2End >= e1Start and e2End <= e1End)
        ):
            ans2 += 1
    
    print('%s pt1: %s' % (case, ans1))
    print('%s pt2: %s' % (case, ans2))

main()