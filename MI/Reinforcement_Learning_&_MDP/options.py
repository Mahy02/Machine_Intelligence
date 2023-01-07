# This file contains the options that you should modify to solve Question 2



# disc factor: if we want to reach closer terminal then small number (0.1) but if further terminal then big (1)

#noise: if further (0.2,0.3) but if closer with terminals -ve rewards (-10) then let it very small like 0.01

#reward: its alwasy negative in some kind of range accoridng to what i need however the 2 extremes is that if i want to stay inside forever its positive and if i wanna go to any terminal quickly then -ve big number



# For question2_1, we want the policy to seek the near terminal state (reward +1) via the short dangerous path (moving besides the row of -10 state).
def question2_1():  #DONE
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0.002,    #since its vey risky to go to -10 so noise should be very small to avoid going to the -10 oenalty
        "discount_factor": 0.1,     #small number as we want a closer path to the goal node or terminal node
        "living_reward": -5.0       #to go faster to the terminal state and exit quickly
    }


# For question2_2, we want the policy to seek the near terminal state (reward +1) via the long safe path (moving away from the row of -10 state).
def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,  #since long path so noise can be average (not too small and not too big)
        "discount_factor": 0.3,    #since longst path so medium disc factor
        "living_reward": -0.17    #terminal -1/6
    }


# For question2_3, we want the policy to seek the far terminal state (reward +10) via the short dangerous path (moving besides the row of -10 state).
def question2_3():   #DONE
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,  #small noise as high risk
        "discount_factor": 0.9,   #big disc factor as shorter path
        "living_reward": -1       #negative small reward
    }

# For question2_4, we want the policy to seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state).
def question2_4():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,   #medium noise is good
        "discount_factor": 0.99,   #big disc factor as further path
        "living_reward": 0.0  #reward is zero so it can take the longest route to reach the +10 terminal state
    }

# For question2_5, we want the policy to avoid any terminal state and keep the episode going on forever.
def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,   #we dont want it to go to any exits so less noise
        "discount_factor": 0.9,      #very long route as we dont even want an exit so big disc factor
        "living_reward": 5.0     #we need a very big reward to avoid any exists
    }

# For question2_6, we want the policy to seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possi
def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,     #less noise to move in the right direction towards the exit quickly
        "discount_factor": 0.1,   #less disc factor as we want shortest path
        "living_reward": -12     #very big penalty to let teh agent escape and commit sucide at any exit
    }



#note:::: that most of the numbers i knew wether it should be small or big but i kept debugging till i got the most accurate one, however it was in the expected range
