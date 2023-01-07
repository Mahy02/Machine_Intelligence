from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
#import numpy as np

from helpers.utils import NotImplemented

# This is a class for a generic Policy Iteration agent
class PolicyIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training
    policy: Dict[S, A]
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # This initial policy will contain the first available action for each state,
        # except for terminal states where the policy should return None.
        self.policy = {
            state: (None if self.mdp.is_terminal(state) else self.mdp.get_actions(state)[0])
            for state in self.mdp.get_states()
        }
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor

#####################################################################################################################
    # Given the utilities for the current policy, compute the new policy
    def update_policy(self):
        #TODO: Complete this function

        #actions= env.actions(state)
        actions= self.mdp.get_actions(self)
        #identify a max 
        max=float("-inf")

        #loop around action and for each action sum all successors by the bellman eqn
        for action in actions:
            #since P(s' |s,a) gets all successors given an action and the current state
            #so get all successors for this action & their probabilities
            #Get successor:
            # Given a state and an action, this function returns 
            # all possible next states "s'" and their corresponding probabilities P(s'|s, a) as a dictionary 
            prob=self.mdp.get_successor(self, action)  #prob is a dictionary {s', probability}

            #sum=0 at beg and then we want to sum over the ==>P(s'|s,a) * [ R(s,a,s') + \gamma U(s') ]
            sum=0

            #we want to get probabilities of next state where key is next state (sd) and value is prob (p)
            for sd in prob.keys():
                #now compute bellman
                #note that u(s') is a dictionary where {state, utility} ==>we want utility so give it s' and we should convert to string as the key is a string representation of state
                #sum+= p*(self.mdp.get_reward(state, action, sd)+ (self.discount_factor* p))
                sum+= prob[sd]*(self.mdp.get_reward(self, action, sd)+ (self.discount_factor* self.utilities[sd]))
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
    #end update policy
    ####################################################################################################################
    
    # Given the current policy, compute the utilities for this policy
    # Hint: you can use numpy to solve the linear equations. We recommend that you use numpy.linalg.lstsq
    def update_utilities(self):
        #TODO: Complete this function
        NotImplemented()
    
    # Applies a single utility update followed by a single policy update
    # then returns True if the policy has converged and False otherwise
    def update(self) -> bool:
        #TODO: Complete this function
        NotImplemented()

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update():
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        NotImplemented()
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            policy = {
                self.mdp.format_state(state): (None if action is None else self.mdp.format_action(action)) 
                for state, action in self.policy.items()
            }
            json.dump({
                "utilities": utilities,
                "policy": policy
            }, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in data['utilities'].items()}
            self.policy = {
                self.mdp.parse_state(state): (None if action is None else self.mdp.parse_action(action)) 
                for state, action in data['policy'].items()
            }
