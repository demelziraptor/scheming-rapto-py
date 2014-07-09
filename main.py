class Game():
    
    def __init__(self):
        ####
        # properties that stay the same throughout the game
        ####
        self.fruits = {}   # num of each type of fruit possible
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
        
        # state of the game - calculated
        self.needed_fruits = {}   # how much of each type of fruit need to get
        self.available_fruits = {}   # how much of each type still on the board
        self.num_types_needed = 0   # how many types of fruit left to win
        self.num_types_won = 0   # how many types of fruit already won
        
        # preferences for next move
        self.pref_fruit_types = []   # list of types of fruit going to try and get
        self.fruit_locations = []
        
        # next move
        self.dinner_location = (0,0)
        self.next_move = False    

    ####
    # methods required by game
    ####        
    def new_game(self):
        # calculate how many fruits for each type of fruit
        self.init_fruits()
        self.available_fruits = self.fruits.copy()
        self.needed_fruits = self.fruits.copy()
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
        # cannot take, calculate current game state
        self.calculate_game_state()
        # calculate preferences for this move
        self.calculate_move_preferences()
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
        if self.dinner_location and self.current_position == self.dinner_location:
            x,y = self.current_position
            if self.board[x][y] > 0:
                trace('DELICIOUS FRUIT OM NOM NOM NOM')
                self.next_move = TAKE
                self.dinner_location = False
                return True
        return False

    def calculate_game_state(self):
        """ calculates fruits available, fruits needed, and number of fruit types needed """
        self.num_types_won = 0
        additional_types_needed = 0
        for fruit_name,fruit_total in self.fruits.iteritems():
            mine = get_my_item_count(fruit_name)
            opponent = get_opponent_item_count(fruit_name)
            available = fruit_total - mine - opponent
            # set available fruit
            self.available_fruits[fruit_name] = available
            # count if I've won this type
            if mine >= self.targets[fruit_name]:
                self.num_types_won += 1
            # count if opponent has almost won a type
            if self._one_fruit_left_to_win(fruit_name, opponent):
                additional_types_needed = 1
                #pass
            # set needed fruit
            if (mine >= self.targets[fruit_name] or opponent >= self.targets[fruit_name] or 
                    not available or self._opponent_about_to_win_type(fruit_name, opponent)):
                self.needed_fruits[fruit_name] = 0
                continue
            self.needed_fruits[fruit_name] = self.targets[fruit_name] - mine
        self.num_types_needed = ((self.num_types_to_win - self.num_types_won) +
            additional_types_needed)

    def calculate_move_preferences(self):
        # reset preferences
        self.pref_fruit_types = []
        self.fruit_locations = []
        # set pref fruit types
        self.calculate_pref_fruit_types()
        # set pref fruit locations
        self.calculate_pref_fruit_with_attributes()
    
    def calculate_pref_fruit_types(self):
        """ calculate the types of fruit we want """
        needed_fruits = self.needed_fruits.copy()
        for i in range(self.num_types_needed):
            try:
                # TODO: available fruits????
                fruit = min(needed_fruits, key=available_fruits.get)
                if needed_fruits[fruit] == 0:
                    needed_fruits.pop(fruit, None)
                    continue
            except:
                # going to be a tie, no more prefs so pick any available fruit type
                fruit = self._find_any_leftover_fruit()
            self.pref_fruit_types.append(fruit)
    
    def calculate_pref_fruit_with_attributes(self):
        """ create list of fruit we possibly want with useful attributes """
        fruit_positions = {}
        for x in range(self.width):
            for y in range(self.height):
                name = self.board[x][y]
                if name in self.pref_fruit_types:
                    if name in fruit_positions and self.opponent_position != (x,y):
                        fruit_positions[name].append((x,y))
                    else:
                        fruit_positions[name] = [(x,y)]
        for fruit_type,locations in fruit_positions.iteritems():
            self.fruit_locations.append([self.needed_fruits[fruit_type], locations])
            
    ####
    # path calculation methods
    ####
    def path_permutations(self, iterable, r=None):
        trace('starting path permutations')
        trace(str(iterable))
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
        trace('starting fruit combinations')
        if n==0: yield []
        else:
            for i in xrange(len(items)):
                for cc in self.fruit_combinations(items[i+1:],n-1):
                    yield [items[i]]+cc

    def gen_unique_fruit_combinations(self, fruit_list, current=False):
        trace('starting gen unique fruit combinations')
        if not current:
            for i in fruit_list[0]:
                for val in self.gen_unique_fruit_combinations(fruit_list[1:], i):
                    yield val
        else:
            if len(fruit_list) == 1:
                for i in fruit_list[0]:
                    yield current + i
            else:
                for i in fruit_list[0]:
                    tmp = current + i
                    for val in self.gen_unique_fruit_combinations(fruit_list[1:], tmp):
                        yield val

    def unique_fruit_combinations(self, fruit):
        trace('starting unique fruit combinations')
        fruit_list = []
        for i in range(len(fruit)):
            current_list = []
            for coords in self.fruit_combinations(fruit[i][1], fruit[i][0]):
                current_list.append(coords)
            fruit_list.append(current_list)  
        return self.gen_unique_fruit_combinations(fruit_list)

    def different_paths(self):
        """ finds all possible paths and calculates minimum """
        trace('starting different paths')
        min_distance = 0
        min_path = []
        for y in self.unique_fruit_combinations(self.fruit_locations):
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
        trace('let\'s go ' + str(min_path) + ' distance ' + str(min_distance))
        return min_path
        
    def calculate_dinner_location(self):
        self.dinner_location = self.different_paths()[0]
    

    ####
    # helper methods
    ####
    def _max_num_nearby_positions(self, area):
        """ assuming no board edges, maximum number of nearby positions """
        max_per_distance = {}
        for i in range(area):
            max_per_distance[i+1] = (i+1) * 4
        return max_per_distance
    
    def _num_nearby_positions(self, position, area):
        """ returns dict with distance and count of valid positions """
        nearby = {}
        for x in range(position[0] - area, position[0] + area + 1):
            for y in range(position[1] - area, position[1] + area + 1):
                distance = self._distance(position, (x,y))
                if ((x < 0 or y < 0) or (x,y) == position or
                   (x >= self.width or y >= self.height) or distance > area):
                    continue
                if distance not in nearby:
                    nearby[distance] = 0
                nearby[distance] += 1    
    
    def _nearby_positions(self, position, area):
        """ generator to calculate nearby valid positions """
        for x in range(position[0] - area, position[0] + area + 1):
            for y in range(position[1] - area, position[1] + area + 1):
                if (x < 0 or y < 0) or (x,y) == position or (x >= self.width or y >= self.height):
                    continue
                if abs(position[0] - x) + abs(position[1] - y) > area:
                    continue
                yield (x,y) 
    
    def _opponent_about_to_win_type(self, fruit_name, count):
        """ returns true if opponent can take the fruit on their next go and win this type """
        fruit_at_opp = self.board[self.opponent_position[0]][self.opponent_position[1]]
        if fruit_at_opp == fruit_name and self._one_fruit_left_to_win(fruit_name, count):
            trace('opp about to win')
            return True
        return False
    
    def _one_fruit_left_to_win(self, fruit_name, count):
        """ returns true if only 1 (or 0.5) more fruit is required to win the type """
        to_go = self.targets[fruit_name] - count
        if (to_go > 0) and (to_go <= 1) and (to_go <= self.available_fruits[fruit_name]):
            trace('1 to go')
            return True
        return False    
    
    def _calculate_min_stuff_wanted(self, stuff_total):
        if stuff_total % 2 == 0:
            return (stuff_total + 2) / 2
        else:
            return (stuff_total + 1) / 2
            
    def _find_any_leftover_fruit(self):
        for fruit_name,fruit_total in self.available_fruits.iteritems():
            if fruit_total != 0 and fruit_name not in self.pref_fruit_types:
                return fruit_name
                       
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
            
    ####
    # init methods
    ####
    def init_fruits(self):
        for fruit_type in range(get_number_of_item_types()):
            fruit_count = get_total_item_count(fruit_type+1)
            self.fruits[fruit_type+1] = fruit_count
            
    def init_num_types_to_win(self):
        self.num_types_to_win = self._calculate_min_stuff_wanted(len(self.fruits))

    def init_targets(self):
        for fruit_name,fruit_count in self.fruits.iteritems():
            fruit_target = self._calculate_min_stuff_wanted(fruit_count)        
            self.targets[fruit_name] = fruit_target
    
    ####
    # broken random direction - need to fix without import
    ####    
    def pick_random_direction(self):
        possible_directions = [NORTH, SOUTH, EAST, WEST]
        if self.current_position[0] == 0:
            possible_directions.remove(WEST)
        if self.current_position[0] == self.width:
            possible_directions.remove(EAST)
        if self.current_position[1] == 0:
            possible_directions.remove(NORTH)
        if self.current_position[1] == self.height:
            possible_directions.remove(SOUTH)
        # cannot import to pick random, so just pick first
        return possible_directions[0]
       

GAME = Game()
                
def make_move():
    return GAME.make_move()
    
def new_game():
    GAME.new_game()
