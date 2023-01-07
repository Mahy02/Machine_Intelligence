from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json

from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor

##########################################################################################################################  
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        ################################################################
        #U(s) = \max_{a} \sum_{s'} P(s'|s,a) [ R(s,a,s') + \gamma U(s')]$$
        #gamma is discount factor
        #u(s') self.utilities
        #reward
        #probability [get successor(state and action)] where it returns dictionary {states, values of probability}=>we need prob of next
        #sum all this
        #we iterate on actions
            #for one action we sum all successors by the eqn
            #we iterate on successors of each action
                #calculate the eqn on each successor   (sum+=)
            #we see if the summation>max or not cause we want max summation
        ####################################################################

        #first check if a state is a terminal state => then utility=0
        if self.mdp.is_terminal(state):
            return 0
        #get all actions of current state
        actions= self.mdp.get_actions(state)

        #identify a max 
        max=float("-inf")

        #loop around action and for each action sum all successors by the bellman eqn
        for action in actions:
            #since P(s' |s,a) gets all successors given an action and the current state
            #so get all successors for this action & their probabilities
            #Get successor:
            # Given a state and an action, this function returns 
            # all possible next states "s'" and their corresponding probabilities P(s'|s, a) as a dictionary 
            prob=self.mdp.get_successor(state, action)  #prob is a dictionary {s', probability}

            #sum=0 at beg and then we want to sum over the ==>P(s'|s,a) * [ R(s,a,s') + \gamma U(s') ]
            sum=0

            #we want to get probabilities of next state where key is next state (sd) and value is prob (p)
            for sd in prob.keys():
                #now compute bellman
                #note that u(s') is a dictionary where {state, utility} ==>we want utility so give it s' and we should convert to string as the key is a string representation of state
                sum+= prob[sd]*(self.mdp.get_reward(state, action, sd)+ (self.discount_factor* self.utilities[sd]))
            #endfor
            #now compare sum with max
            if sum>max:
                max=sum
            #endif
        #endfor
        #we want at the end to return utility of the state "max of summations"
        return max
    #end of compute bellman
    
 ##########################################################################################################################  
  
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        #we want to update our utility till it converges 
        #we will loop around each state to calculate:
            # 1.utility change: abs( u(s) "gotten from states" - the new utility from bellman self.compute bellman (u(s')))
                 #after each iteration we get max utility change
            #2. for each state we want to update its utility so make a dict where key is state and value is new computed bellman utility
                #at the end we assign self.utilities with new utilities
        updated=dict()
        max=float("-inf")
        utility_change=0
        states=self.mdp.get_states()
        for state in states:
            utility_d= self.compute_bellman(state)
            utility_change=abs(utility_d- self.utilities[state])
            updated[state]=utility_d             #updating utility value for each state
        
            if utility_change>max:
                max=utility_change
            #endif
        #endfor

        #update:
        self.utilities=updated  
        #self.utilities=updated.copy()             

        #compare max utility change by tolerance 
        #if max<tolreance return true
        if max<tolerance:
            return True
        else:
            return False
        #endif

    #end_update
##########################################################################################################################

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update(tolerance):
                break
        return iteration
##########################################################################################################################

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        
         #first check if a state is a terminal state => then action is none
        if self.mdp.is_terminal(state):
            return None
        
        #we will do exactly what we did in bellman but instead of returning the max utility of summmations ww wull return optima; action

        #get all actions of given environment  instead of the mdp
        optimal_action:A

        #actions= env.actions(state)
        actions= self.mdp.get_actions(state)
        #identify a max 
        max=float("-inf")

        #loop around action and for each action sum all successors by the bellman eqn
        for action in actions:
            #since P(s' |s,a) gets all successors given an action and the current state
            #so get all successors for this action & their probabilities
            #Get successor:
            # Given a state and an action, this function returns 
            # all possible next states "s'" and their corresponding probabilities P(s'|s, a) as a dictionary 
            prob=self.mdp.get_successor(state, action)  #prob is a dictionary {s', probability}

            #sum=0 at beg and then we want to sum over the ==>P(s'|s,a) * [ R(s,a,s') + \gamma U(s') ]
            sum=0

            #we want to get probabilities of next state where key is next state (sd) and value is prob (p)
            for sd in prob.keys():
                #now compute bellman
                #note that u(s') is a dictionary where {state, utility} ==>we want utility so give it s' and we should convert to string as the key is a string representation of state
                #sum+= p*(self.mdp.get_reward(state, action, sd)+ (self.discount_factor* p))
                sum+= prob[sd]*(self.mdp.get_reward(state, action, sd)+ (self.discount_factor* self.utilities[sd]))
                #self.utilities[sd]
            #endfor
            #now compare sum with max
            if sum>max:
                max=sum
                #define optimal action to be max action
                optimal_action=action #get the optimal action that got the max summation 
            #endif
        #endfor
        #we want optimal action
        return optimal_action
    #end act
##########################################################################################################################
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
