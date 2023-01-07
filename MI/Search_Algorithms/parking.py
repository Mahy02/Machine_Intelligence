from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]


# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.



    #Note that point is a class containing the location (x and y)
    #cars is a tuple of points  (x,y)  state[i] i is the point which is the position/location of car i
    # cars have many cars each car has specific index in the tuple and each index has a point (each index represents a car and its position)
    #(pointofcar0, pointofcar1..............)
   
    #passages are the locations avaliable to the car to move in and they are a Set
    
    #slots is a dict {(x,y): index }  //point is a location/posiition of the parking slots  each slot has a specific car that should be in it 
    # x,y is the position slot of car [index]
    #key is a point #to access key it is one slot in the slots and its value is slots[slot] its value is the index of this slot "index of the car"
    #for slots
    #{point:0 , point:4  , point:10.....etc} "not necessary in order"
    
    #parking state is a (x,y) point 

    #For understanding how it works:::::
    # now we have slots {point:0 , point:4  , point:10.....etc} each slot represent key posiiton/point of that slot and the index of the car that should be in that slot
    # then each car has a psoition and each car represent the state (pointofcar0, pointofcar1..............) 

   

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        return self.cars  #returning the initial state of all cars 
    #end of get initial state func
       
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:        
        #TODO: ADD YOUR CODE HERE
        # goal is to have each car in its parking place  so looping around each parking slot we want the position slot.x and slot.y= to the car position
        #we will get the index of the car supposed to be in that specific car slot from the value slots[slot]
        #each car is a state so state[i].x and state[i].y 
        #state[i]   x,y  car.x car.y
        #here i is the index of the value-->slots[slot]
        #1. we want to loop around the slots
        for slot in self.slots.keys():  #looping around positions
            #2. checking that each car is in its parking slot
            if slot.x == state[self.slots[slot]].x and slot.y== state[self.slots[slot]].y:
                continue   #continue checking other slots
            else: #some car is not in its position
                return False
            #end of if
        #end of for loop
        #if continued through whole loop and didnt return then reached the goal so return true
        return True
    #end of is_goal

    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:  #parking action is a tuple (index of car, direction it will move in)
        #TODO: ADD YOUR CODE HERE

        #point right #x+1
        right_point=Point( 1,  0)
        #point left #x-1
        left_point=Point(-1,  0)
        #point up #y-1
        uo_point=Point( 0, -1) 
        #point down #y+1
        down_point=Point( 0,  1)

        right_position=None 
        left_position=None 
        up_position=None 
        down_position=None 

        #list of actions that the car/state can take
        actions = []
        #we want to loop around each cars in the state and each car see which directions it can move in and return the list state is a set of points for each car
        
        #1. looping around each car
        for car_index, car in enumerate(state):   #car is a point (x,y) 
            #2.#for each direction in directions the car will move so its position will change "up, down, right and left"
            index=car_index
            right_position=car.__add__(right_point)
            left_position= car.__add__(left_point)
            up_position= car.__add__(uo_point)
            down_position= car.__add__(down_point)

            #park 1-->  (0,r)
            #answer should be (0,r) (0,l)  why left??
            
            # Disallow walking into walls   #from passages  &   #disallow walking into a position having another car
            if right_position  in self.passages and right_position not in state:
                #to get index of car we get it from slot where slot[key]= value  where key is point "here is car" and value is the index
                action_tuple=(index, Direction.RIGHT)
                actions.append(action_tuple)  
            #endif
            if left_position  in self.passages and left_position not in state:
                #to get index of car we get it from slot where slot[key]= value  where key is point "here is car" and value is the index
                action_tuple=(index, Direction.LEFT)
                actions.append(action_tuple)
            #endif
            if up_position  in self.passages and up_position not in  state:
                #to get index of car we get it from slot where slot[key]= value  where key is point "here is car" and value is the index
                action_tuple=(index, Direction.UP)
                actions.append(action_tuple)
            #endif
            if down_position  in self.passages and down_position not in state:
                #to get index of car we get it from slot where slot[key]= value  where key is point "here is car" and value is the index
                action_tuple=(index, Direction.DOWN)
                actions.append(action_tuple)
            #endif
        #end of for loop
        return actions
    #end of Get_actions function

    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:  #parking action is [(index, direction)...] #state is(x,y)
        #TODO: ADD YOUR CODE HERE
        
        new_state=list(state)
       
        #point right #x+1
        right_point=Point( 1,  0)
        #point left #x-1
        left_point=Point(-1,  0)
        #point up #y-1
        uo_point=Point( 0, -1) 
        #point down #y+1
        down_point=Point( 0,  1)

        new_position=None 

        index,direction=action
        
        #if direction is right move right
        if direction== 0:   #2nd element of the tupple in the list of index car
            new_position= state[index].__add__(right_point)
        #end of if
        #if drection is left move left
        if direction== 2:   #2nd element of the tupple in the list of index car
            new_position= state[index].__add__(left_point)
        #end of if
        #if direction is up move up
        if direction== 1:   #2nd element of the tupple in the list of index car
            new_position= state[index].__add__(uo_point)
        #end of if
        #if direction is down move down
        if direction== 3:   #2nd element of the tupple in the list of index car
            new_position= state[index].__add__(down_point)
        #end of if

        #make new state = new pos
        new_state[index]=new_position
        new_state=tuple(new_state)

        return new_state 
    #end of get_successor
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:    #note that here and in get successor it takes one action only
        #TODO: ADD YOUR CODE HERE
        cost=1 #usual cost
        #here we see cost of moving one car onlyyyyy
        #check if a car is an a position of a slot that is not its cost will be +100
        #parking action is (int, direction)
        #if direction is right check the position and cost

        if str(action[1]) =='R':   #2nd element of the tupple in the list of index car
            position=Point(state[action[0]].x+1, state[action[0]].y) #just to test the position
            if position in self.slots.keys(): #if it exists in slots as keys
                if self.slots[position]!= action[0]:  #check if its index is not same as the one in the slot
                    cost+=100 #then it is in another slot than its own so cost+100
                #end if
            #end if
        #end if
         #if drection is left move left
        if str(action[1]) =='L':   #2nd element of the tupple in the list of index car
            position=Point(state[action[0]].x-1, state[action[0]].y)
            #now we have new position--we want to check that its inside a parking slot position
            if position in self.slots.keys(): #if it exists in slots as keys
                #if it the position is a parking slot position then check if the index of parking slot car is the same as the one of our car
                if self.slots[position]!= action[0]:  #check if its index is not same as the one in the slot
                    cost+=100 #then it is in another slot than its own so cost+100
                    print(cost)
                #end if
            #end if
        #end if
        #if direction is up move up
        if str(action[1]) =='U':   #2nd element of the tupple in the list of index car
            position=Point(state[action[0]].x, state[action[0]].y-1) 
            if position in self.slots.keys(): #if it exists in slots as keys
                if self.slots[position]!= action[0]:  #check if its index is not same as the one in the slot
                    cost+=100 #then it is in another slot than its own so cost+100
                    print(cost)
                #end if
            #end if
        #end if
        #if direction is down move down
        if str(action[1]) =='D':   #2nd element of the tupple in the list of index car
            position=Point(state[action[0]].x, state[action[0]].y+1)
            if position in self.slots.keys(): #if it exists in slots as keys
                if self.slots[position]!=action[0]:  #check if its index is not same as the one in the slot
                    cost+=100 #then it is in another slot than its own so cost+100
                    print(cost)
                #end if
            #end if
        #end if
        return cost
    #end of get cost
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
