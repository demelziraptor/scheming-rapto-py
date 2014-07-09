fruit3 = ((1, ((2,3),)), 
          (2, ((3,3), (6,2), (5,5))), 
          (3, ((0,4), (0,5), (1,2), (2,6), (4,0))))
          
fruit35 = ((2, ((3,3), (6,2), (5,5))), 
          (2, ((0,4), (0,5), (1,2))),
          (2, ((0,6), (6,1), (3,1))))

fruit45 = ((2, ((3,3), (6,2), (5,5))), 
          (2, ((0,4), (0,5), (1,2))),
          (2, ((0,6), (6,1), (3,1))),
          (2, ((4,0), (3,0), (6,6))))

fruit4 = ((1, ((2,3),)), 
          (2, ((3,3), (6,2), (5,5))), 
          (3, ((0,4), (0,5), (1,2), (2,6), (4,0))),
          (4, ((0,6), (6,1), (3,1), (3,0), (6,6), (6,0))))
          
fruit = ((1, ((2,3),)), 
          (2, ((3,3), (6,2), (5,5))))
          
my_position = (7,7)

def path_permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def fruit_combinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in fruit_combinations(items[i+1:],n-1):
                yield [items[i]]+cc

def gen_unique_fruit_combinations(fruit_list, current=False):
    if not current:
        for i in fruit_list[0]:
            yield gen_unique_fruit_combinations(fruit_list[1:], i)
    else:
        if len(fruit_list) == 1:
            for i in fruit_list[0]:
                yield current + i
        else:
            for i in fruit_list[0]:
                tmp = current + i
                for val in gen_unique_fruit_combinations(fruit_list[1:], tmp):
                    yield val

def unique_fruit_combinations(fruit):
    fruit_list = []
    for i in range(len(fruit)):
        current_list = []
        for coords in fruit_combinations(fruit[i][1], fruit[i][0]):
            current_list.append(coords)
        fruit_list.append(current_list)  
    return gen_unique_fruit_combinations(fruit_list)
    
def distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])

def different_paths(fruit, my_position):
    min_distance = 0
    min_path = []
    for x in unique_fruit_combinations(fruit):
        for y in x:
            paths = path_permutations(y)
            for path in paths:
                total_distance = 0
                current_position = my_position
                for coord in path:
                    total_distance += distance(current_position, coord)
                    current_position = coord
                if not min_distance:
                    min_distance = total_distance
                    min_path = path
                else:
                    if total_distance < min_distance:
                        min_distance = total_distance
                        min_path = path
    print 'let\'s go', min_path, 'distance', min_distance
    return min_path

if different_paths(fruit35, my_position)[0] == my_position:
    print 'TAKE'
else:
    print 'move somewhere'


   




    
    
   
