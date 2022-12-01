from queue import PriorityQueue

def main(filename):
    with open(filename) as f:
        lines = f.readlines()
    input = [line.strip() for line in lines]
    print(input)
    
    # Part 1 coded on scratch
    print(sum([
        30,
        3000,
        11000,
        11000,

        11,
        11,

        800,
        700,

        7000,
        4000,
        4000,

        60,
        6,
        5,

        500,
        600,

        7,
        8,

        8000,

        40,

        600,

        40,

        700,
        
        50,
        60,
        60,
        70,
    ]))
    
    



if True:
    print('\ntest\n')
    main('23.test')
if False:
    print('\nmain\n')
    main('23.input')