class Game():

    def __init__(self):
        ####
        # properties that stay the same throughout the game
        ####
        self.targets = {}   # max to win each type
        self.num_types_to_win = 0   # num of types of fruit need to win
        self.width = WIDTH
        self.height = HEIGHT
        
        ####
        # properties that change
        ####
        # state of the game - fixed from game
        self.board = []
        self.current_position = (0,0)
        self.opponent_position = (0,0)
        self.num_types_needed = 0
        
        # coordinates considered for next move
        self.coord_list = []
        
        # next move
        self.dinner_location = (0,0)
        self.next_move = False  


    ####
    # methods required by game
    ####        
    def new_game(self):
        # calculate target fruits for each type of fruit
        self.init_targets()
        # calculate number of types needed to win
        self.init_num_types_to_win()
        
    def make_move(self):
        # reset move and get fixed game properties
        self.next_move = False
        self.set_current_position()
        self.board = get_board()
        # if on the same place as current closest fruit, pick up
        if self.can_take_fruit():
            return self.move()
        # cannot take, get list of coords
        self.calculate_coord_list()
        # calculate which fruit to go for
        self.calculate_dinner_location()
        # move!
        return self.move()

    ####
    # main methods
    ####
    def set_current_position(self):
        self.current_position = (get_my_x(), get_my_y())
        self.opponent_position = (get_opponent_x(), get_opponent_y())
    
    def move(self):
        if self.dinner_location:
            self._calculate_direction()
        return self.next_move
    
    def can_take_fruit(self):
        """ takes fruit if possible """
        if self.dinner_location and self.current_position == self.dinner_location:
            x,y = self.current_position
            if self.board[x][y] > 0:
                trace('DELICIOUS FRUIT OM NOM NOM NOM')
                self.next_move = TAKE
                self.dinner_location = False
                return True
        return False

    def number_of_fruit_needed(self, fruit, available):
        """ returns number of fruit needed if can win that type, or 0 otherwise """
        have = get_my_item_count(fruit)
        needed = self.targets[fruit] - have
        trace('have: ' + str(have) + ' needed ' + str(needed))
        if needed <= 0:
            trace('reduce needed count')
            self.num_types_needed -= 1
            trace('new count ' + str(self.num_types_needed))
        if needed > 0 and needed <= available:
            return int(round(needed))
        return 0

    def calculate_coord_list(self):
        """ generate list of coords """
        self.coord_list = []
        self.num_types_needed = self.num_types_to_win
        coords_by_type = {}
        coords_by_available = []
        for x in xrange(self.width):
            for y in xrange(self.height):
                if self.opponent_position == (x,y):
                    continue
                name = self.board[x][y]
                if name:
                    try:
                        coords_by_type[name].append((x,y))
                    except:
                        coords_by_type[name] = [(x,y)]
        need_something = False
        for fruit,coords in coords_by_type.iteritems():
            needed = self.number_of_fruit_needed(fruit, len(coords))
            if needed:
                need_something = True
                self.coord_list.append((needed, coords))
            coords_by_available.append((len(coords), coords))
        trace('number of types needed: ' + str(self.num_types_needed))
        if not coords_by_available:
            # opponent currently on last fruit, go anywhere
            self.coord_list.append((1, (0,0)))
            return
        if not need_something:
            self.coord_list = coords_by_available
        trace(str(self.coord_list))
        
    def path_permutations(self, elements):
        if len(elements) <=1:
            yield elements
        else:
            for perm in self.path_permutations(elements[1:]):
                for i in range(len(elements)):
                    # nb elements[0:1] works in both string and list contexts
                    yield perm[:i] + elements[0:1] + perm[i:]

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
    
    def different_paths(self):
        """ finds all possible paths and calculates minimum """
        min_distance = 0
        min_path = []
        local_len = len
        for y in self.unique_fruit_combinations(self.coord_list):
            for path in self.path_permutations(list(y)):
                num_fruit_in_path = local_len(path)
                total_distance = num_fruit_in_path
                pos = self.current_position
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
                trace('path: ' + str(path) + ' distance ' + str(total_distance))
                if not min_distance:
                    min_distance = total_distance
                    min_path = path
                    continue
                if total_distance < min_distance:
                    min_distance = total_distance
                    min_path = path
                if total_distance == min_distance:
                    if (self.distance(self.current_position, path[0]) < 
                        self.distance(self.current_position, min_path[0])):
                        min_distance = total_distance
                        min_path = path
        trace('let\'s go ' + str(min_path) + ' distance ' + str(min_distance))
        return min_path
        
    def calculate_dinner_location(self):
        self.dinner_location = self.different_paths()[0]
        
    def _distance(self, p0, p1):
        """ difference in x + difference in y to calculate distance """
        return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
        
    def _calculate_direction(self):
        mx,my = self.current_position
        tx,ty = self.dinner_location
        trace('current position: ' + str(self.current_position))
        trace('dinner position: ' + str(self.dinner_location))
        if mx > tx:
            self.next_move = WEST
            return
        if mx < tx:
            self.next_move = EAST
            return
        if my > ty:
            self.next_move = NORTH
            return
        if my < ty:
            self.next_move = SOUTH
            return
        # actually, dinner is here! convenient! :D
        self.next_move = TAKE
        
    def _calculate_min_stuff_wanted(self, stuff_total):
        if stuff_total % 2 == 0:
            return (stuff_total + 2) / 2
        else:
            return (stuff_total + 1) / 2
            
    ####
    # init methods
    ####
    def init_num_types_to_win(self):
        self.num_types_to_win = self._calculate_min_stuff_wanted(get_number_of_item_types())

    def init_targets(self):
        for fruit in range(get_number_of_item_types()):
            fruit_name = fruit+1
            fruit_count = get_total_item_count(fruit_name)
            fruit_target = self._calculate_min_stuff_wanted(fruit_count)        
            self.targets[fruit_name] = fruit_target
            
            
GAME = Game()
                
def make_move():
    return GAME.make_move()
    
def new_game():
    GAME.new_game()
