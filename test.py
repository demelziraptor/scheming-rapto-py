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

def permutations(iterable, r=None):
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

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

def unique_fruits(fruit_list, current=False):
    if not current:
        for i in fruit_list[0]:
            yield unique_fruits(fruit_list[1:], i)
    else:
        if len(fruit_list) == 1:
            for i in fruit_list[0]:
                yield current + i
        else:
            for i in fruit_list[0]:
                tmp = current + i
                for val in unique_fruits(fruit_list[1:], tmp):
                    yield val

def our_options(fruit):
    fruit_list = []
    for i in range(len(fruit)):
        current_list = []
        for coords in xuniqueCombinations(fruit[i][1], fruit[i][0]):
            current_list.append(coords)
        fruit_list.append(current_list)  
    return unique_fruits(fruit_list)
    
def different_paths(fruit):
    for x in our_options(fruit):
        for y in x:
            perms = permutations(y)
            for perm in perms:
                print perm
    

different_paths(fruit35)



   




    
    
   
