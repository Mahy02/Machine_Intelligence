from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
import copy


###########################################################################################################################
# This function should apply 1-Consistency to the problem.
# In other words, it should modify the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints should be removed from the problem (they are no longer needed).
# The function should return False if any domain becomes empty. Otherwise, it should return True.
def one_consistency(problem: Problem) -> bool:      #working
    new_domain_values=[] #where we will store the new domains after applying the constrains then replace it inside the domains diction
    #we have some variables , their domains, their constraints 
    #for example if we have A,B variables and their domain is from 1-10 
    #constrains are A!=10 and B<5 
    #we loop around the constraints:
    for constraint in problem.constraints:
        #check its a unary
        new_domain_values=[]
        if isinstance(constraint, UnaryConstraint):
            #then see the variable of that constraint
            cons_var=constraint.variable
            current_domain_set= problem.domains[cons_var]    #set containing the domain values of the current variable
            #now loop around its values :
            for value in current_domain_set:
                if constraint.condition(value): #if satsified then update new set
                    new_domain_values.append(value)
                #endif
            #end for
            if not new_domain_values: #empty
                return False
            else: #replace
                problem.domains[cons_var]=set(new_domain_values)
            #end if
        #end if
    #end for
    return True
#end of one_consistency fn

###########################################################################################################################

###########################################################################################################################

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:   #WOrking
    #TODO: Write this function
    #domains are all the domains of the unassigned variables
    #we have the assigned variable and its assigned value
    #loop around the constrains binary and get the neighbor variable and remove the assigned value from it
    for const in problem.constraints:
         # and see the other end "neighbors" #by function get other  and check that the variable is on the other side of the const
        if isinstance(const, BinaryConstraint) and assigned_variable in const.variables:
            other_var=const.get_other(assigned_variable)
            other_var_domain_set=[]
            #check first that the variable exsists in the domain [unassigned]
            if other_var not in domains.keys():
                continue
            else:
                #other var domain variables:
                other_var_domain_set= list(domains[other_var])
                #now loop on the other domain's set and remove if exists
                if assigned_value in other_var_domain_set:
                     other_var_domain_set.remove(assigned_value)
                    #endif
                #end for

            #check if empty or not
            #if empty return false
            if not other_var_domain_set: #empty 
                return False
            else:
                #change/modify the domain
                domains[other_var]= set(other_var_domain_set)
            #end if
        #end if
    #end for
    return True
#end forward_checking

###########################################################################################################################

###########################################################################################################################

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:   #only one test case in solve
    #TODO: Write this function
    #choosing the value that gives me more domain for the other neighbors 
    
    #we have a variale to be assigned: for example A
    #then we need to loop around its values for example {red,green, blue}
    
    #now after looping on all values we sort descen. order 
    #it can be done by a dictionary where keys are values and items are the domain_sum_length
    #dictionary to keep track of order of values by their domain_sum_length
    ordered_values={}

    for value_to_assign in domains[variable_to_assign]:
        #then we need to assign every value to this variable and do forward checking:
        #we wont actually assign we will just assume we assigned:
        #variable to sum all the domain length of the neighbors of this particular value
        domain_sum_length=0
        prev=domain_sum_length
        isequal=True
        #counter=0
        #loop around the constrains binary
        for const in problem.constraints :
         #and see the other end "neighbors" #by function get other 
            if isinstance(const, BinaryConstraint) and variable_to_assign in const.variables:
                other_var=const.get_other(variable_to_assign)
                #now get other var domain set and check if values= values then count ++
                other_var_domain_set=[]
                #check first that the variable exsists in the domain [unassigned]
                if other_var not in domains.keys():
                    continue
                else :
                    #other var domain variables:
                    other_var_domain_set=list(domains[other_var])
                    #If the other variable has no domain (in other words, it is already assigned), skip this constraint.
                    if not other_var_domain_set:
                        continue
                    #endif
                    if value_to_assign in other_var_domain_set:
                        other_var_domain_set.remove(value_to_assign)
                        #counter+=1
                    #now remove from it the values assigned
                    #Update the other variable's domain in a new list to only include the values that satisfy the binary constraint with the assigned variable.
                    #endif
                   
                    #now we want to sum this set's length
                    variable_length=len(other_var_domain_set)  #length of the set
                    #sum all the lengths of these variables domain
                    domain_sum_length+= variable_length
                #endif
            #end if
        #end for
        #now we have domain_sum_length for specific value
        ordered_values[value_to_assign]=domain_sum_length 
        #we want to check that this domain_sum_length is similar to the one before it or not
    #end for



    #now we want to order the domainsum length in a decs order:   and then by asc order of the values which are keys => lambada  x[1],-x[0]
    reverse_sorted_by_value= sorted(ordered_values.items(), key= lambda x: (x[1],-x[0]), reverse=True)
    reverse_sorted_by_value_dict= dict(reverse_sorted_by_value)
    #now we have it reverse sorted by value

    #now we should have a dic that contain value:domain length 
    #we should loop and see if 2 domains are equal then sort by asc of values(keys)

    #then we want to extract the keys only [which are values to assign]
    ordered_values_list=list(reverse_sorted_by_value_dict) #getting keys only

    return ordered_values_list
#end of LRV


###########################################################################################################################

###########################################################################################################################

# This function should return the variable that should be picked based on the MRV heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
# IMPORTANT: If multiple variables have the same priority given the MRV heuristic, 
#            order them in the same order in which they appear in "problem.variables".

def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:   #working
    #loop around the varia#bles [keys] and see length of the set
    #the one with the least length will be the one chosen  and returned
    min_length=1000000000
    min_variable='' 
    for variable in domains:
        #prev= min_length
        variable_length=len(domains[variable])  #length of the set
        if variable_length< min_length:
            min_length= variable_length
            min_variable=variable 
        #end if
    #end for
    return min_variable
#end of MRV


###########################################################################################################################

###########################################################################################################################

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.

# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.

# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #1.checking the one consistency:
    is_one_cons=one_consistency(problem)
    
    domains=problem.domains 
    assig={}
    if is_one_cons==True:
        assig=backtrack(assig, problem, domains) #check if can be assigned
        #if can be assigned then assig size will be same size as the problem's domain size 
        if len(assig.keys())==len(problem.domains.keys()): 
            return assig
        else:
            return None
    else:
        return None
    #endif
#end of Solve

def backtrack(assig:Assignment, problem: Problem, domains:dict)->Optional[Assignment]:
    #2.exit condition: "reaching a complete assig"
    if problem.is_complete(assig):
        return assig
    #endif

    #3.calling the MRV to choose variable:
    #var= minimum_remaining_values(problem, problem.domains)    
    var= minimum_remaining_values(problem, domains)    

    #4.calling LRV to choose the order of the values on the chosen var:
    #values= least_restraining_values(problem, var, problem.domains)
    values= least_restraining_values(problem, var, domains)

   
    #5.looping around the values then Forward chacking to see if true or false: "inference"
    for value in values:
        #current_domains=copy.deepcopy(problem.domains[var])
        current_domains=copy.deepcopy(domains)
        current_domains.pop(var)
        #is_solvable=forward_checking(problem, var, value, problem.domains)
        is_solvable=forward_checking(problem, var, value, current_domains)
        if(is_solvable):
            assig[var]= value #assignment
            #6. calling recusrively:
            assig= backtrack(assig, problem, current_domains)
            if len(assig.keys())==len(problem.domains.keys()): #all values assigned can be solved "no constrains"
                return assig
            else:
                continue
    return assig

#end of backtrack


###########################################################################################################################

###########################################################################################################################

