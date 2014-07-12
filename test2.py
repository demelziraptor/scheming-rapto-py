import profile

class TestPaths():

    def __init__(self):
        self.coord_list2 = [(1.0, [(5, 3)]), (2.0, [(0, 2), (0, 6), (8, 0)]), (3.0, [(1, 5), (2, 0), (6, 4), (7, 0), (9, 6)])]
        self.coord_list = [(1, [(1, 0)]), (2, [(2, 1), (6, 9), (7, 9)]), (3, [(0, 7), (2, 7), (6, 2), (7, 7), (10, 5)]), (4, [(1, 10), (3, 6), (4, 0), (4, 9), (6, 4), (6, 6), (10, 1)]), (5, [(1, 4), (1, 8), (2, 4), (3, 5), (3, 10), (5, 5), (7, 2), (9, 2), (10, 9)])]
        self.current_position = (7, 6)
        self.width = 10
        self.height = 10
        self.num_types_needed = 2
        self.calculate_dinner_location()
        print self.dinner_location

    def path_permutations(self, elements):
        if len(elements) <=1:
            yield elements
        else:
            for perm in self.path_permutations(elements[1:]):
                for i in range(len(elements)):
                    # nb elements[0:1] works in both string and list contexts
                    yield perm[:i] + elements[0:1] + perm[i:]
    
    def path_permutations2(self, iterable, r=None):
        """ given a set of unique coordinates, returns all possible permutations of those coordinates """
        #iterable = list(generator)
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        if r > n:
            return
        indices = range(n)
        cycles = range(n, n-r, -1)
        yield tuple(pool[i] for i in indices[:r])
        while n:
            for i in reversed(xrange(r)):
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

    def fruit_combinations(self, items, n):
        """ generator returns possible combinations for a list and num required"""
        if n==0: yield []
        else:
            for i in xrange(len(items)):
                for cc in self.fruit_combinations(items[i+1:],n-1):
                    yield [items[i]]+cc

    def gen_unique_fruit_combinations(self, fruit_list, current=False):
        """ generator returns unique combinations for a list containing lists of coords """
        if not current:
            if len(fruit_list) == 1:
                for i in fruit_list[0]:
                    yield i
            else:
                for i in fruit_list[0]:
                    for val in self.gen_unique_fruit_combinations(fruit_list[1:], i):
                        yield val
        else:
            if len(fruit_list) == 1:
                for i in fruit_list[0]:
                    yield current + i
            else:
                for i in fruit_list[0]:
                    for val in self.gen_unique_fruit_combinations(fruit_list[1:], current + i):
                        yield val

    def unique_fruit_combinations(self, fruit):
        """ returns a list of unique sets of coordinates for each type of fruit """
        fruit_list = []
        num_fruit = len(fruit)
        for i in xrange(num_fruit):
            fruit_list.append(list(self.fruit_combinations(fruit[i][1], fruit[i][0])))
        if self.num_types_needed > num_fruit:
            self.num_types_needed = num_fruit
        for group_option in self.fruit_combinations(fruit_list, self.num_types_needed):
            yield self.gen_unique_fruit_combinations(group_option).next()
    
    def path_distance2(self, start, path):
        local_abs = abs
        total_distance = 0
        pos = start
        for coord in path:
            total_distance += local_abs(pos[0] - coord[0]) + local_abs(pos[1] - coord[1])
            pos = coord
        return total_distance
        
    def distance(self, p0, p1):
        """ no abs as slow, need to use if statements instead """
        if p0[0] > p1[0]:
            d = p0[0] - p1[0]
        else:
            d = p1[0] - p0[0]
        if p0[1] > p1[1]:
            return d + (p0[1] - p1[1])
        else:
            return d + (p1[1] - p0[1])
    
    def path_distance(self, start, path):
        total_distance = 0
        pos = start
        for coord in path:
            if pos[0] > coord[0]:
                total_distance += pos[0] - coord[0]
            else:
                total_distance += coord[0] - pos[0]
            if pos[1] > coord[1]:
                total_distance += pos[1] - coord[1]
            else:
                total_distance += coord[1] - pos[1]
            pos = coord
        return total_distance
    
    def different_paths(self):
        """ finds all possible paths and calculates minimum """
        min_distance = 0
        min_path = []
        num_paths = 0
        for y in self.unique_fruit_combinations(self.coord_list):
            #print 'y', y
            for path in self.path_permutations(list(y)):
                #print 'path', path
                num_paths += 1
                num_fruit_in_path = len(path)
                total_distance = self.path_distance(self.current_position, path) + num_fruit_in_path
                if not min_distance:
                    min_distance = total_distance
                    min_path = path
                    continue
                if total_distance < min_distance:
                    min_distance = total_distance
                    min_path = path
                if total_distance == min_distance:
                    if (self.distance(self.current_position, path[0]) > 
                            self.distance(self.current_position, min_path[0])):
                        min_distance = total_distance
                        min_path = path
        print 'let\'s go', str(min_path), 'distance', str(min_distance)
        print 'number of paths', num_paths
        return min_path
        
    def calculate_dinner_location(self):
        self.dinner_location = self.different_paths()[0]
        


profile.run('TestPaths()')

