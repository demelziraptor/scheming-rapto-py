import timeit
import sys

class TestPaths():

    def __init__(self):
        self.coord_list = [(1.0, [(5, 3)]), (2.0, [(0, 2), (0, 6), (8, 0)]), (3.0, [(1, 5), (2, 0), (6, 4), (7, 0), (9, 6)])]
        self.current_position = (7, 6)
        self.width = 10
        self.height = 10
        self.calculate_dinner_location()
        print self.dinner_location

    def path_permutations(self, iterable, r=None):
        """ generator returns all possible paths of given coordinates """
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
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

    def fruit_combinations(self, items, n):
        """ generator returns possible combinations for a list and num required"""
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
        if n==0: yield []
        else:
            for i in xrange(len(items)):
                for cc in self.fruit_combinations(items[i+1:],n-1):
                    yield [items[i]]+cc

    def gen_unique_fruit_combinations(self, fruit_list, current=False):
        """ generator returns unique combinations for a list containing lists of coords """
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
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
        """ gets possible combinations for type of fruit, then combines to create coord combinations """
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
        fruit_list = []
        for i in range(len(fruit)):
            current_list = []
            for coords in self.fruit_combinations(fruit[i][1], fruit[i][0]):
                current_list.append(coords)
            fruit_list.append(current_list)
        return self.gen_unique_fruit_combinations(fruit_list)

    def different_paths(self):
        """ finds all possible paths and calculates minimum """
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
        min_distance = 0
        min_path = []
        for y in self.unique_fruit_combinations(self.coord_list):
            paths = self.path_permutations(y)
            for path in paths:
                total_distance = 0
                current_position = self.current_position
                for coord in path:
                    total_distance += self._distance(current_position, coord)
                    current_position = coord
                if not min_distance:
                    min_distance = total_distance
                    min_path = path
                else:
                    if total_distance < min_distance:
                        min_distance = total_distance
                        min_path = path
                    if total_distance == min_distance:
                        if (self._distance(path[0], self.current_position) > 
                                self._distance(min_path[0], self.current_position)):
                            min_distance = total_distance
                            min_path = path
        print 'let\'s go', str(min_path), 'distance', str(min_distance)
        return min_path
        
    def calculate_dinner_location(self):
        times['mid'].append((sys._getframe().f_code.co_name, timeit.default_timer()))
        self.dinner_location = self.different_paths()[0]
        
    def _distance(self, p0, p1):
        """ difference in x + difference in y to calculate distance """
        return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
        


times = {}
times['START'] = timeit.default_timer()
times['mid'] = []
TestPaths()
times['END'] = timeit.default_timer()

for time in times['mid']:
    print 'Function:', time[0], ' ~ time:', time[1]
print '\n\nTotal:', str(times['END'] - times['START'])

