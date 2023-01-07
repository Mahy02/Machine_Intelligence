from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)  #here is calculates exculidean distance between the state node and the goal directly for all the graph 

#TODO: Import any modules and write any functions you want to use

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    utils.NotImplemented()
    #for a strong heuristic we want the h(n) to be admissible and consistent 
    #here strong_heurtsic takes the graph "problem" and takes the state
    #we should see each state in the graph and calculate its heurstic  "we can use manhattan distance where at each node we calculate manhatan distance to the goal"
    # In this problem, the agent can move Up, Down, Left or Right # and it has to collect all the coins then reach the exit
    #at each node we want to calculate manhatan distacne to the next place that has a coin
    #when all coins are collected we want to calculate manhtan distance to teh exit 