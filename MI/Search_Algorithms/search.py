from argparse import Action
import queue
from typing import Counter
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils
from queue import PriorityQueue, Queue




#TODO: Import any modules you want to use
#class queue.Queue(maxsize=0)

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #in bfs we do level by level-- 
    # we use FIFO queue for frontier to put the expanded nodes
    # all nodes at certain level are expanded before going to the other
    #we check on goals when expansion 
    #we would need an is visited 
    #it takes the problem as state and action "go to which node" and its initial state is s "start node" and returns solution which is a list of actions "my path"
    #the successor function is going to the nodes to be expanded putting them in frontier 
    #no cost here

    # dic for backtracking the path "it will include as key child and value as parent" because key must be unique and one parent can have many children but a child has one parent
    sol={initial_state: ('null', initial_state)}   #the root's parent is null
    #list for the solution
    path=[]
    
    #1. make a node that has state = problem.initial state    ----->here this is the Problem[S,A]
   
    #2. if problem.goal "node and state" then return solution "node"
    if problem.is_goal(initial_state):   #initial state 
        return path
    
    #3. a fifo queue with node as the only element
    fqueue=[initial_state]   

    #4. explored as an empty set
    explored_set= set() 
    
    #5.loop till frontier is empty and return false
    while len(fqueue)!=0: 
        # keep popping from frointier -->add node.state to explored set --> 
        #after popping current node it is now a parent and should be put as a value later
        currentnode= fqueue.pop(0)  #fifo   # we want the current node to be looking at the first left child
        explored_set.add(currentnode)
    
        # then "each node supposed to have children so going to any of them is considered an action" 
        # do a for loop for each action in  problem.actions(node.state)
        for i in problem.get_actions(currentnode):        #   initialize a child node = child.node(problem, node, acrion)
            child_node= problem.get_successor(currentnode, i)
            if child_node==i:
                flag=0 #graph
            else:
                flag=1 #dungeon
            #checking if its a dungeon game or graph
            #   if child.state is not in frontier or explored set 
            if child_node not in explored_set and child_node not in fqueue:
                #then check if its the goal--- if problem.goaltest(child.state) then return solution
                if problem.is_goal(child_node):   #initial state 

                 if flag==0:
                    sol[child_node]=(currentnode,i) # ti put in dic  "childnode is key its parent is the currentnode"
                     #backtracking to get the solution path
                     #looping around the dic from child node i am at till traversing back to root
                     #say we have {s:a , s: b , S:c, a:g} ->then loop in each key in sol 
                
                    path.append(child_node)  #the goal "child" "key"
                    #loop till key is null   #key is child and parent is value sol[key]= value
                    node=path[0]    #make the node= to the goal  child
                    parent_tuple=sol[node] #parent of that child
                    parent=parent_tuple[0]
                 
                    while parent!= 'null':
                            path.append(parent)  #getting parent of the node called parent "originally was child"
                            parent_tuple=sol[parent]  
                            parent=parent_tuple[0]
                    #end of while
                 else:
                    #path.append(child_node)  #the goal "child" "key"
                    #loop till key is null   #key is child and parent is value sol[key]= value
                    #node=path[0]    #make the node= to the goal  child
                    path.append(i)
                    parent_tuple=sol[currentnode] #parent of that child
                    parent=parent_tuple[0]
                    actionn=parent_tuple[1]
                 
                    while parent!= 'null':
                            path.append(actionn)  #getting parent of the node called parent "originally was child"
                            parent_tuple=sol[parent]  
                            parent=parent_tuple[0]
                            actionn=parent_tuple[1]
                    #end of while
                 path.reverse()
                 if flag==0:
                    path.pop(0)
                 return path
                #endif
            #else we insert in frontier 
                else:
                    #putting in frontier the children          #left to right   #first in is left then first out is left
                    fqueue.append(child_node) 
                    #putting the children as key to their parent the current node
                    sol[child_node]=(currentnode,i)

                 
            #end of first if
        #end of for loop
    #end of while
#end of bfs fn


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # dic for backtracking the path "it will include as key child and value as parent" because key must be unique and one parent can have many children but a child has one parent
    sol={initial_state: ('null', initial_state)}   #the root's parent is null
    #list for the solution
    path=[]
    
    #1. make a node that has state = problem.initial state    ----->here this is the Problem[S,A]

    #3. a LIFO stack with node as the only element
    frontier=[initial_state]       #last in first out so when pop pop last element

    #4. explored as an empty set
    explored_set= set() 
    
    #5.loop till frontier is empty and return false
    while len(frontier)!=0: 
        # keep popping from frointier -->add node.state to explored set --> 
        #after popping current node it is now a parent and should be put as a value later
        currentnode= frontier.pop(len(frontier)-1)  #fifo   # we want the current node to be looking at the first left child
        
        if currentnode not in explored_set: #check if it is already in explored set or not "case there is no goal ever"
            explored_set.add(currentnode)
        else:
            continue
        #end of if

        #check if the current node is goal 
        
        if problem.is_goal(currentnode):   #initial state 

          if flag==0:
            #sol[child_node]=currentnode # ti put in dic  "childnode is key its parent is the currentnode"
            #backtracking to get the solution path
            path.append(currentnode)  #the goal "child" "key"

            #loop till key is null   #key is child and parent is value sol[key]= value
            node=path[0]    #make the node= to the goal  child
            parent_tuple=sol[node]  #{key: (value,action)  child:parent}
             #parent of that child
            parent=parent_tuple[0] #state
            #action=parent_tuple[1]

            while parent!= 'null':
                path.append(parent)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]
                parent=parent_tuple[0]
            #end of while

          else:
            parent_tuple=sol[currentnode]
            parent=parent_tuple[0]
            actioon=parent_tuple[1]
            #path.append(parent)
            while parent!= 'null':
                path.append(actioon)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]
                parent=parent_tuple[0]
                actioon=parent_tuple[1]
            #end of while

          #end of if
                
          path.reverse()
          if flag==0:
            path.pop(0)

                    
          return path
        #end of if
    
        # then "each node supposed to have children so going to any of them is considered an action" 
        # do a for loop for each action in  problem.actions(node.state)
        for i in problem.get_actions(currentnode):        #   initialize a child node = child.node(problem, node, acrion)
            child_node= problem.get_successor(currentnode, i)  #child node is a state
           
            if child_node==i:
                flag=0 #graph
            else:
                flag=1 #dung

            #   if child.state is not in frontier or explored set 
            if child_node not in explored_set: #not visited
                #putting in frontier the children          #left to right   #first in is left then first out is left
                frontier.append(child_node) 
                #putting the children as key to their parent the current node
                # we should actually put the i not the childnode
                sol[child_node]=(currentnode,i)
                
            #end of first if
        #end of for loop
    #end of while
#end of dfs fn


    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #Algo: 
    # we have problem having the initial state from thr agrs & path cost
    #we keep track of cummulative cost
    #we remove initial state from frontier and put the actions "the children" amd their cost
    #we see which has less cummulative cost and remove from frontier then put its children "Actions" and put it itself in explored set
    #we put the dictionary also to help in the backtracking "we put in the dic whatever we put in the frontier"
    #keep doing this till goal is found or frontier is empty 
    #when putting in frontier you can find more than one goal so check if its not in explored set or not in fqueue or if its the goal and in frontier then see if it has lesser cost then remove te previous goal from frontier and add the new one

    #steps:
    #1. we have a current node that has initial state and cost=0
    #we need a path list and a sol dict
    sol={initial_state: ('null', initial_state)}  #parent is value and child is key 
    path=[]
   
    #2. priority queue by cost with initial state as the only element
    frontier= queue.PriorityQueue() #pr 1 is cost and if we have 2 nodes having sam pr1 we compare by pr2 "FIFO" which is a counter
    order=0
    frontier.put((0, order, initial_state)) #pr1 pr2 node      TUPLE
    #higher prio. is the lesser cost and the lesser counter

    #3. explored as an empty set # we want it to contain prio too so it will be  a dic instead of set
    # the key will be node and valye will be  priorities
    #explored_set= {initial_state: 0} #"s:0"
    explored_set= {} #empty 
    explored_set[initial_state]=0  

    #another explored_set for order
    explored_set2={}
    explored_set2[initial_state]=0


    #4.loop till frontier is empty and return 
    while not frontier.empty():
        #we will pop the node from the frontier according to prio
        current_node=frontier.get()[2]  #to get the state which has index 2 in the tuple

        #check if its the goal or not
        if problem.is_goal(current_node): #it is a child

            #we want to backtrack the dictionary:
            #sol[child_node]=current_node # to put in dic  "childnode is key "first one in tuple" its parent is the currentnode"
            
          if flag==0:
            path.append(current_node)  #the goal "child" "key"

            node=path[0]    #make the node= to the goal  child
            parent_tuple=sol[node] #parent of that child
            parent=parent_tuple[0]

            while parent!= 'null':
                path.append(parent)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
            #end of while
          else:
            parent_tuple=sol[current_node] #parent of that child
            parent=parent_tuple[0]
            actioon=parent_tuple[1]
            while parent!= 'null':
                path.append(actioon)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
                actioon=parent_tuple[1]
            #end of while

            
        
          path.reverse()
          if flag==0:
            path.pop(0)
                    
          return path
        #end of if

        

        #looping around each action "children" of the current parent node
        for i in problem.get_actions(current_node):        #   initialize a child node = child.node(problem, node, acrion)
            child_node= problem.get_successor(current_node, i)
            if child_node==i:
                flag=0 #graph
            else:
                flag=1 #dung
            
            #note that we want to put the childnode with its path+path of its parent
            #get cost between state elana wa2fa 3ndha wel actions fa yb2a between parent and its child
            #cost_between_nodes= problem.get_cost(current_node, child_node)
            #ex: from S to A (1) and S to B (12) then B to D (4) so we want to add 4+12 "in its path"
           
            #we want to calculate cummulative cost
            # we want to backtrack the path to keep getting cost of its parent
            #now we want D as child to get its parent so D will be a key
            parent=current_node #this is the parent of the chikd_node actions
            child=child_node #a child
            #say we have {S:A, S:B, B:D, D:F}  S to A(1) S to B(12), B to D(4) and D to f(1)
            #each time we have the cost between nodes
            cummulative_cost=0
            #we will loop on dic till we reach null parent and keep getting cost between them
            while parent!='null':
                #getting cost:
                cummulative_cost+=problem.get_cost(child, parent) #between parent "as child" and his parent
                #for iteration:
                child=parent #child became a parent
                parent_tuple=sol[child] #we want to get the parent of the new parent who was a child [key]=value key is child and value is parent
                parent=parent_tuple[0]
            #end of while

            #a list to check on elements of p.q
            frontierlist= list(frontier.queue)


            #check if the child node is not in explored set or fromtier
            if child_node not in explored_set and not frontier.queue.__contains__(child_node):
                 
                #add the node to explored set #with cummulative cost "S:0, A:1, B:2"
                explored_set[child_node]=cummulative_cost
                

                 #increase order
                order+=1
                explored_set2[child_node]= order

                #add in frontier with cummulative cost
                frontier.put((cummulative_cost,order, child_node))

                #add to dic
                sol[child_node]=(current_node,i)  #child as key and value is its parent #in the sec element of tuple put the cost_betn_nodes


            #else child node is in frontier with less/higher cost
            elif does_exist(frontierlist, child_node):
            #child_node in frontier.queue[:][2]:
            #does_exist(frontierlist, child_node):
                
                #if this child have less cost than one in frontier remove from frontier and add new one
                if cummulative_cost < explored_set[child_node]:
                    
                    #exchange
                    frontier.queue.remove((explored_set[child_node], explored_set2[child_node], child_node))
                    frontier.put((cummulative_cost,order, child_node))
                    
                    #add to dic
                    sol[child_node]=(current_node,i)  #child as key and value is its parent
                #end of sec if

            #end of first if

        #end of for loop
    #end of while loop
#end of UCS function



#function that checks if an element exists in a list of tuples # it takes list
def does_exist(flist: list, child_node: S) ->bool:
    #check
    for item in flist:
        if item[2]==child_node:
            return True
        else:
           continue
    return False
#end of does_exist function




def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
     #Algo:  exactly similar to UCS but the cost is cost+heursitic function
     # note that cost is exactly similar to UCS "cummulative" 
     # while heurstic is the h(n) of the end node "so basically the children" not the parent 
     
    #steps:
    #1. we have a current node that has initial state and cost=0
    #we need a path list and a sol dict
    sol={initial_state: ('null',initial_state)}  #parent is value and child is key 
    path=[]
   
    #2. priority queue by cost with initial state as the only element
    frontier= queue.PriorityQueue() #pr 1 is cost and if we have 2 nodes having sam pr1 we compare by pr2 "FIFO" which is a counter
    order=0
    frontier.put((0, order, initial_state)) #pr1 pr2 node      TUPLE
    #higher prio. is the lesser cost and the lesser counter

    #3. explored as an empty set # we want it to contain prio too so it will be  a dic instead of set
    # the key will be node and valye will be  priorities
    #explored_set= {initial_state: 0} #"s:0"
    explored_set= {} #empty 
    explored_set[initial_state]=0  

    #another explored_set for order
    explored_set2={}
    explored_set2[initial_state]=0


    #4.loop till frontier is empty and return 
    while not frontier.empty():
        #we will pop the node from the frontier according to prio
        current_node=frontier.get()[2]  #to get the state which has index 2 in the tuple

        #check if its the goal or not
        if problem.is_goal(current_node): #it is a child

            #we want to backtrack the dictionary:
            #sol[child_node]=current_node # to put in dic  "childnode is key "first one in tuple" its parent is the currentnode"
          if flag==0:
            path.append(current_node)  #the goal "child" "key"

            node=path[0]    #make the node= to the goal  child
            parent_tuple=sol[node] #parent of that child
            parent=parent_tuple[0]

            while parent!= 'null':
                path.append(parent)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
            #end of while
          else:
            parent_tuple=sol[current_node] #parent of that child
            parent=parent_tuple[0]
            actionn=parent_tuple[1]

            while parent!= 'null':
                path.append(actionn)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
                actionn=parent_tuple[1]
            #end of while
        
          path.reverse()
          if flag==0:
            path.pop(0)
                    
          return path
        #end of if

        

        #looping around each action "children" of the current parent node
        for i in problem.get_actions(current_node):        #   initialize a child node = child.node(problem, node, acrion)
            child_node= problem.get_successor(current_node, i)
            if child_node==i:
                flag=0 #graph
            else:
                flag=1 #dung
            
            #note that we want to put the childnode with its path+path of its parent
            #we want to calculate cummulative cost first:
            parent=current_node #this is the parent of the chikd_node actions
            child=child_node #a child
           
            cummulative_cost=0
            #we will loop on dic till we reach null parent and keep getting cost between them
            while parent!='null':
                #getting cost:
                cummulative_cost+=problem.get_cost(child, parent) #between parent "as child" and his parent
                #for iteration:
                child=parent #child became a parent
                parent_tuple=sol[child] #we want to get the parent of the new parent who was a child [key]=value key is child and value is parent
                parent=parent_tuple[0]
            #end of while

            #now we want to get the total cost which is cost+ heuristic:
            total_cost= cummulative_cost+ heuristic(problem,child_node)

            #a list to check on elements of p.q
            frontierlist= list(frontier.queue)


            #check if the child node is not in explored set or fromtier
            if child_node not in explored_set and not frontier.queue.__contains__(child_node):
                 
                #add the node to explored set #with cummulative cost "S:0, A:1, B:2"
                explored_set[child_node]=total_cost
                

                 #increase order
                order+=1
                explored_set2[child_node]= order

                #add in frontier with cummulative cost
                frontier.put((total_cost,order, child_node))

                #add to dic
                sol[child_node]=(current_node,i)  #child as key and value is its parent #in the sec element of tuple put the cost_betn_nodes


            #else child node is in frontier with less/higher cost
            elif does_exist(frontierlist, child_node):
            #child_node in frontier.queue[:][2]:
            #does_exist(frontierlist, child_node):
                
                #if this child have less cost than one in frontier remove from frontier and add new one
                if total_cost < explored_set[child_node]:
                    
                    #exchange
                    frontier.queue.remove((explored_set[child_node], explored_set2[child_node], child_node))
                    frontier.put((total_cost,order, child_node))
                    
                    #add to dic
                    sol[child_node]=(current_node,i)  #child as key and value is its parent
                #end of sec if

            #end of first if

        #end of for loop
    #end of while loop
#end of A* function
    

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #Algo:  exactly similar to UCS but the cost is heursitic function "NOT CUMMULATIVE"
     # while heurstic is the h(n) of the end node "so basically the children" not the parent 
     
    #steps:
    #1. we have a current node that has initial state and cost=0
    #we need a path list and a sol dict
    sol={initial_state: ('null', initial_state)}  #parent is value and child is key 
    path=[]
   
    #2. priority queue by cost with initial state as the only element
    frontier= queue.PriorityQueue() #pr 1 is cost and if we have 2 nodes having sam pr1 we compare by pr2 "FIFO" which is a counter
    order=0
    frontier.put((0, order, initial_state)) #pr1 pr2 node      TUPLE
    #higher prio. is the lesser cost and the lesser counter

    #3. explored as an empty set # we want it to contain prio too so it will be  a dic instead of set
    # the key will be node and valye will be  priorities
    #explored_set= {initial_state: 0} #"s:0"
    explored_set= {} #empty 
    explored_set[initial_state]=0  

    #another explored_set for order
    explored_set2={}
    explored_set2[initial_state]=0


    #4.loop till frontier is empty and return 
    while not frontier.empty():
        #we will pop the node from the frontier according to prio
        current_node=frontier.get()[2]  #to get the state which has index 2 in the tuple

        #check if its the goal or not
        if problem.is_goal(current_node): #it is a child
         if flag==0:
            #we want to backtrack the dictionary:
            #sol[child_node]=current_node # to put in dic  "childnode is key "first one in tuple" its parent is the currentnode"
            
            path.append(current_node)  #the goal "child" "key"

            node=path[0]    #make the node= to the goal  child
            parent_tuple=sol[node] #parent of that child
            parent=parent_tuple[0]

            while parent!= 'null':
                path.append(parent)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
            #end of while
         else:
            
            parent_tuple=sol[current_node] #parent of that child
            parent=parent_tuple[0]
            actionn=parent_tuple[1]

            while parent!= 'null':
                path.append(actionn)  #getting parent of the node called parent "originally was child"
                parent_tuple=sol[parent]   #parent is a key tuple and we want it equal to first element only
                parent=parent_tuple[0]
                actionn=parent_tuple[1]
            #end of while

         path.reverse()
         if flag==0:
            path.pop(0)
                    
         return path
        #end of if

        

        #looping around each action "children" of the current parent node
        for i in problem.get_actions(current_node):        #   initialize a child node = child.node(problem, node, acrion)
            child_node= problem.get_successor(current_node, i)
            #here there will be no cummulative cost or total cost, we would only have heurtsic cost
            if child_node==i:
                flag=0 #graph
            else:
                flag=1 #dung
            
            h_cost=heuristic(problem, child_node)

            #a list to check on elements of p.q
            frontierlist= list(frontier.queue)


            #check if the child node is not in explored set or fromtier
            if child_node not in explored_set and not frontier.queue.__contains__(child_node):
                 
                #add the node to explored set #with cummulative cost "S:0, A:1, B:2"
                explored_set[child_node]=h_cost
                

                 #increase order
                order+=1
                explored_set2[child_node]= order

                #add in frontier with cummulative cost
                frontier.put((h_cost,order, child_node))

                #add to dic
                sol[child_node]=(current_node,i) #child as key and value is its parent #in the sec element of tuple put the cost_betn_nodes


            #else child node is in frontier with less/higher cost
            elif does_exist(frontierlist, child_node):
            #child_node in frontier.queue[:][2]:
            #does_exist(frontierlist, child_node):
                
                #if this child have less cost than one in frontier remove from frontier and add new one
                if h_cost < explored_set[child_node]:
                    
                    #exchange
                    frontier.queue.remove((explored_set[child_node], explored_set2[child_node], child_node))
                    frontier.put((h_cost,order, child_node))
                    
                    #add to dic
                    sol[child_node]=(current_node,i)  #child as key and value is its parent
                #end of sec if

            #end of first if

        #end of for loop
    #end of while loop
#end of greedy function
    