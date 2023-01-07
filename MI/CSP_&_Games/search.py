from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 
# All the search functions should return the expected tree value and the best action to take based on the search results



# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action
#end greedy



#################################################################################################################
# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].


#version one of minimax
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    turn=game.get_turn(state) #get turn of current player if 0 then it is max player else it is min player
    #game.is_terminal(state) --> returns a tuple (bool if terminal state or not, values for all agents(list) "will be none if not terminal")
    # the value of the state for the agent 'i' will be be at the index 'i'.
    # So for example, if the game contains two players fighting each other, values[0] will be the state's value
    # for player 1 and value[1] will be the state's value for player 2. Usually, the value[0] = -value[1] since
    # they are enemies and if one of them receives a positive value (reward) in a certain state, the other will most likely receive a negative value (penalty).
    terminal, agents_terminal_values= game.is_terminal(state)    
    #bool and ist to hold all the terminal values of all the agents 
    #if a terminal node we want to return the value and the best action for the max node in a tuple (value, action)
    #If the given state is terminal, the returned action should be `None`.
    if terminal==True: 
        game_over=(agents_terminal_values[0], None)
        return game_over
    #end if
    # If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 
    if max_depth==0:   #if max depth is reached it returns the heuristic of the node  #Note for me: dk yet if 0 or -1
        game_over=(heuristic(game,state,0),None)
        return game_over
    #end if
    #see if min playe or max player

    if turn==0: #max node  #its like calling max search function
        act= None
        #maxi= (('-inf'), act) #where we want max value from the successors and the action to return them
        value=-100000000.0
        actions= game.get_actions(state)  #now we have list of possible actions
        #choose max from successors
        for action in actions:
            successor_child= game.get_successor(state, action)
            #we want to call the function recursively till reach a terminal state to get the minimax value of every successor [because we should start from leaves]
            minimax_value, minimax_action= minimax(game, successor_child, heuristic, max_depth-1)  #keep going down the depth of the tree
            if minimax_value> value:
                value=minimax_value
                #if minimax_action==None: #reached terminal state so assign an action
                act=action #assign the new action
                #end if
            #endif
        #endfor
        return value, act
        # return maxi
    else: #opponents  #like min_search function
        #chooses the min
        act= None
        #mini= (('inf'), act)
        value=10000000.0
        actions= game.get_actions(state)  #now we have list of possible actions
        for action in actions:
            successor_child= game.get_successor(state, action)
            minimax_value, minimax_action= minimax(game, successor_child, heuristic, max_depth-1)  #keep going down the depth of the tree
            if minimax_value< value:
                value= minimax_value
                #if minimax_action==None:
                act=action #assign the new action
        return value, act
                #endif
            #endif
        #endfor
        #return mini
    #endif
    
#end minimiax



#################################################################################################################

#################################################################################################################


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
#Alpha–beta search updates the values of α and β as it goes along and prunes the remaining  branches at a node (i.e., terminates the recursive call) as soon as the value of the current node is known to be worse than the current α or β value for MAX or MIN, respectively. 
#alpha beta from up to down and value from down to up

#explanation of what we will do in the alphabeta function::

#function created to allow recursive call in alphabeta(). it differs in having 2 extra parameters alpha and beta
#α = the value of the best (i.e., highest-value) choice we have found so far at any choice point along the path for MAX.
# alpha has -infinity as holds max value
#β = the value of the best (i.e., lowest-value) choice we have found so far at any choice point along the path for MIN.
#beta has + infinity for min value
#prunning condition:
    #in max:
        #if max value>= beta(best min) prune bec max is waiting for sth big and the value w ehave is already bigger than beta(wont get any gretater value) then prune dont complete branch
        #update alpha
    # in min
        #if min value <= alpha (best max) prune as same idea alpha wont get any less
        #update beta

##pseudo code:

#we initialize value = -infinity at root and alpha with -inf and beta inf
#Starting from the root, we traverse the tree in a depth-first order and pass the alpha and beta to each call.
#max node values are -inf and min nodes values are inf and go down tree initializing alpha and beta
#call till reach leaves

#when reached first depth of 1st branch  "reached leaves"::
    #if a min turn:
        #while loop on successor actions
        #choose  node of successors children and compare it with the value (which is supposed to be inf at beg)
        #assign new value to bbe min for nw [value = min(value, child_value)]
        #compare new value with alpha 
        # if <= alpha 
            # prune "break from the while loop"
        #else
            # update beta= new value [Beta = min(beta, value)]
            #complete node successors "supposed to be a while loop"
        #after the while loop 
        #we now should be having the min value so update min value "traversing up"
    #if a max turn:
        #while loop on successor actions
        #choose  node of successors children and compare it with the value (which is supposed to be -inf at beg)
        #assign new value to bbe max for nw
        #compare new value with beta  (-inf at beg)
        # if >= beta  
            # prune "break from the while loop"
        #else
            # update alpha= new value
            #complete node successors "supposed to be a while loop"
            #call min search  on new alpha and beta -------this will be autommatic with recursion because:
            #each level is either calling min search or max search 
        #after the while loop 
        #we now should be having the min value so update min value "traversing up"


def myalphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = (-10000000), beta: float = (10000000)) -> Tuple[float, A]:
        
        turn=game.get_turn(state) #get turn of current player if 0 then it is max player else it is min player
        terminal, agents_terminal_values= game.is_terminal(state)    

        #exit conditions: #reaches leaves
        #if reaches leaves he should go back up
        if terminal==True:   
            game_over=(agents_terminal_values[0], None)
            return game_over  #value that will go up and the action
        #end if

        if max_depth==0:    #reached depth limit 
            game_over=(heuristic(game,state,0),None)
            return game_over
        #endif

        if turn==0: #max node  #its like calling max search function
            #we want to go down then up
            #values should be -inf if max and inf if min if going down
            #TRAVERSING UP AFTER REACHING TERMINAL STATE and setting real final value:
            value=(-10000000.0)
            act= None
            actions= game.get_actions(state)  #now we have list of possible actions
            for action in actions:
                successor_child= game.get_successor(state, action)
                myalphabeta_val, myalphabeta_act= myalphabeta(game, successor_child, heuristic, max_depth-1, alpha, beta)
                if(myalphabeta_val> value):
                    value=myalphabeta_val
                    act= action
                    if value>=beta: #prune
                        break
                    else: #complete and set beta
                        alpha = max(value, alpha)
                    #endif
                #endif
            #endfor
        #else min nodes like calling min function
        else:
            #we want to go down then up
            #values should be -inf if max and inf if min if going down
            #TRAVERSING UP AFTER REACHING TERMINAL STATE and setting real final value:
            value=(10000000.0)
            act= None
            actions= game.get_actions(state)  #now we have list of possible actions
            for action in actions:
                successor_child= game.get_successor(state, action)
                myalphabeta_val, myalphabeta_act=myalphabeta(game, successor_child, heuristic, max_depth-1, alpha, beta)
                if(myalphabeta_val<value):
                    value= myalphabeta_val
                    act= action
                    if value<=alpha: #prune
                        break
                    else: #complete and set beta
                        beta = min(value, beta)
                    #endif
                #endif
            #endfor
        #end if
        return value,act
#end of myalphabeta

def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return myalphabeta(game,state,heuristic,max_depth) #recursive call to my alpha beta to do exactly like minmax but with pruing 
#end of alpabetea

#############################################################################################################################################

#############################################################################################################################################



# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def my_alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1,  alpha: float = (-10000000), beta: float = (10000000)) -> Tuple[float, A]:
        turn=game.get_turn(state) #get turn of current player if 0 then it is max player else it is min player
        terminal, agents_terminal_values= game.is_terminal(state)    

        #exit conditions: #reaches leaves
        #if reaches leaves he should go back up
        if terminal==True:   
            game_over=(agents_terminal_values[0], None)
            return game_over  #value that will go up and the action
        #end if

        if max_depth==0:    #reached depth limit 
            game_over=(heuristic(game,state,0),None)
            return game_over
        #endif

        #we want to sort the actions based on a heurstic then loop on it
        #if its a max we sort decs to explore nodes with max heurstic first and if min it is sorted asc to explore nodes with min heurstic first
        prio_and_action={}

        #now loop on actions:
        actions= game.get_actions(state)  #now we have list of possible actions
        for action in actions:
            successor_child= game.get_successor(state, action)
            #get herustric of each child state
            prio= heuristic(game,successor_child,0 )
            #now that we have a prio we can make a dictionary where key is action and value is the heustric prio
            prio_and_action[action]= prio
        #end for

        #now we have our dictionary that consists of priority of each action and its action
        #we want to sort the items [prio] asc if min:
        sorted_list= sorted(prio_and_action.items(), key= lambda x:x[1])
        #sorting keys desc if max:
        rev_sorted_list= sorted(prio_and_action.items(), key= lambda x:x[1], reverse=True)

        sorted_dic= dict(sorted_list)
        rev_sorted_dic= dict(rev_sorted_list)

        #now extracting keys only [actions]
        max_actions_list= list(rev_sorted_dic)
        min_actions_list= list(sorted_dic)

        
        if turn==0: #max node  #its like calling max search function
            #we want to go down then up
            #values should be -inf if max and inf if min if going down
            #TRAVERSING UP AFTER REACHING TERMINAL STATE and setting real final value:
            value=(-10000000.0)
            act= None
            for action in max_actions_list:  #looping on our new created action list with desc prio
                successor_child= game.get_successor(state, action)
                myalphabeta_val, myalphabeta_act= my_alphabeta_with_move_ordering(game, successor_child, heuristic, max_depth-1, alpha, beta)
                if(myalphabeta_val> value):
                    value=myalphabeta_val
                    act= action
                if value>=beta: #prune
                    #break
                    return value,act
                else: #complete and set beta
                    alpha = max(value, alpha)
                    #endif
                #endif
            #endfor
        #else min nodes like calling min function
        else:
            #we want to go down then up
            #values should be -inf if max and inf if min if going down
            #TRAVERSING UP AFTER REACHING TERMINAL STATE and setting real final value:
            value=(10000000.0)
            act= None
            for action in min_actions_list:
                successor_child= game.get_successor(state, action)
                myalphabeta_val, myalphabeta_act=my_alphabeta_with_move_ordering(game, successor_child, heuristic, max_depth-1, alpha, beta)
                if(myalphabeta_val<value):
                    value= myalphabeta_val
                    act= action
                if value<=alpha: #prune
                    #break
                    return value,act
                else: #complete and set beta
                    beta = min(value, beta)
                    #endif
                #endif
            #endfor
        #end if
        return value,act
#end of my_alpha_beta_with_move_ordering

def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    return my_alphabeta_with_move_ordering(game,state,heuristic,max_depth)

#############################################################################################################################################

#############################################################################################################################################

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    #we go max from root then chance then min then chance .....etc
    #if turn> 0 wont be min nodes will be chance nodes
    turn=game.get_turn(state)   #get turn of current player if 0 then it is max player else it is a chance node or min node
    terminal, agents_terminal_values= game.is_terminal(state) 
    #exit conditions: #reaches leaves
        #if reaches leaves he should go back up
    if terminal==True:   
        game_over=(agents_terminal_values[0], None)   #turn or 0
        return (abs(game_over[0]),game_over[1])  #value that will go up and the action
    #end if
    if max_depth==0:    #reached depth limit 
        game_over=(heuristic(game,state,0),None)
        return game_over
    #endif
   
    if turn==0:              #if max player
        value=(-10000000.0)
        act= None
        actions= game.get_actions(state)  #now we have list of possible actions
        for action in actions:  
            successor_child= game.get_successor(state, action)      
            expecti_value, expecti_action=expectimax(game,successor_child,heuristic,max_depth-1)  # for every action and its corresponding next state we get the expectimax value of it
            if expecti_value> value:
                value= expecti_value
                #if expecti_action==None:
                act= action
                #endif       
            #endif
        #end for
        return value,act    #action and max value
    #end if
    else: #chance npdes
        act=None
        actions= game.get_actions(state)  #now we have list of possible actions       
        sum=0                                             
        total=0      
        #we should calculate average of successors                                   
        for action in actions:
            successor_child=game.get_successor(state,action)
            expecti_value,expecti_action=expectimax(game,successor_child,heuristic,max_depth-1)
            sum+=expecti_value                #calculate the sum of successors 
            total+=1                    #increment the number of successors
            #if expecti_action==None:
            act=action
            #endif
        #end for
        value= sum/total
        return value ,act       #return average[expecti value] and action
    #end if
#end expectedminimax

        


#############################################################################################################################################
