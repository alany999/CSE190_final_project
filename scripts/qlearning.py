from read_config import read_config
from operator import itemgetter
from copy import deepcopy
import math
import random

qValues = {}
epsilon = 0.0

#def init_policy(wall_list, pit_list, goal, width, height):

# def init_reward(wall_list, pit_list, goal_loc, pit, goal, wall, width, height):
#     for y in range(0,height):
#         temp = []
#         for x in range(0,width):
#             temp_list = [y,x]
#             if [y,x] in pit_list:
#                 temp.append(pit)
#             elif cmp(temp_list, goal_loc) == 0:
#                 temp.append(goal)
#             elif [y,x] in wall_list:
#                 temp.append('WALL')
#             else:
#                     temp.append(0.0)
#
#         if (y == 0):
#             reward = [temp]
#         else:
#             reward.append(temp)
#     return reward

#def init_qValues

def ValidLocation(new_position):

    config = read_config()
    goal = config['goal']
    rows = config['map_size'][0]
    cols = config['map_size'][1]
    walls = config['walls']

    if new_position[0] < 0 or new_position[0] > rows-1 or new_position[1] < 0 or new_position[1] > cols-1:
        return False

    #Check if in wall or pit
    if list(new_position) in walls:
        return False

    return True

def validMove(curr_position, move):

    config = read_config()
    goal = config['goal']
    rows = config['map_size'][0]
    cols = config['map_size'][1]
    walls = config['walls']

    if cmp(list(curr_position), goal) == 0:
        return False

    new_position = getLocationAfterMove(curr_position, move)

    #Check if out of bounds
    if new_position[0] < 0 or new_position[0] > rows-1 or new_position[1] < 0 or new_position[1] > cols-1:
        return False

    #Check if in wall or pit
    if list(new_position) in walls:
        return False

    return True

def getLocationAfterMove(curr_position, move):
    #move up
    if (move == 0):

        # move up
        return (curr_position[0]-1, curr_position[1]+0)

    # move down
    elif (move == 1):

        # move down
        return (curr_position[0]+1, curr_position[1]+0)

    # move right
    elif (move == 2):

        # move right
        return (curr_position[0], curr_position[1]+1)

    # move left
    elif (move == 3):

        # move left
        return (curr_position[0], curr_position[1]-1)

    # unrecognized move
    else:
        print('Illegal Move')


def getLocationAfterMoveWithProb(curr_position, move, p_forward, p_backward, p_left, p_right):
    rng = random.random()

    #Random move
    legalActions = []
    new_position = curr_position[0]-1, curr_position[1]
    if(ValidLocation(new_position)):
        legalActions.append(new_position)
    new_position = curr_position[0], curr_position[1]+1
    if (ValidLocation(new_position)):
        legalActions.append( new_position)
    new_position = curr_position[0], curr_position[1]-1
    if (ValidLocation(new_position)):
        legalActions.append(new_position)
    new_position = curr_position[0]+1, curr_position[1]
    if (ValidLocation(new_position)):
        legalActions.append( new_position)
     # If random value between 0 and 1.0 is less than epsilon, return random action
    if random.random() < epsilon and len(legalActions) > 0:
        return random.choice(legalActions)

    # move up
    if (move == 0):

        # move up
        if (rng <= p_forward):
            new_position = curr_position[0]-1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move right
        elif (rng <= p_right + p_forward):
            new_position = curr_position[0], curr_position[1]+1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move left
        elif (rng <= p_left + p_right + p_forward):
            new_position = curr_position[0], curr_position[1]-1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move down
        else:
            new_position = curr_position[0]+1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

    # move down
    elif (move == 1):

        # move down
        if (rng <= p_forward):
            new_position = curr_position[0]+1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move right
        elif (rng <= p_left + p_forward):
            new_position = curr_position[0], curr_position[1]+1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move left
        elif (rng <= p_left + p_right + p_forward):
            new_position = curr_position[0], curr_position[1]-1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move down
        else:
            new_position = curr_position[0]-1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position


    # move right
    elif (move == 2):

        # move right
        if (rng <= p_forward):
            new_position = curr_position[0], curr_position[1]+1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move up
        elif (rng <= p_left + p_forward):
            new_position = curr_position[0]-1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move down
        elif (rng <= p_left + p_right + p_forward):
            new_position = curr_position[0]+1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move left
        else:
            new_position = curr_position[0], curr_position[1]-1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

    # move left
    elif (move == 3):

        # move left
        if (rng <= p_forward):
            new_position = curr_position[0], curr_position[1]-1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move down
        elif (rng <= p_left + p_forward):
            new_position = curr_position[0]+1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move up
        elif (rng <= p_left + p_right + p_forward):
            new_position = curr_position[0]-1, curr_position[1]
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

        # move right
        else:
            new_position = curr_position[0], curr_position[1]+1
            if (ValidLocation(new_position)):
                return new_position
            else:
                return curr_position

    # unrecognized move
    else:
        print('Illegal Move')
        return curr_position



def computeValueFromQValues(curr_position):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    # Set max value to negative infinity
    max_value = float("-inf")
    config = read_config()
    move_list = config['move_list']
    legalActions = []

    for move in move_list:
        if validMove(curr_position, move):
            legalActions.append(move)
    if len(legalActions) == 0:
        return 0.0
    else:
        # Compute max Q-Value
        for action in legalActions:
            qValue = getQValue(curr_position, action)
            if qValue > max_value:
                max_value = qValue

    # Return max Q-Value
    return max_value


def computeActionFromQValues(curr_position):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    # Set max value to negative infinity
    max_value = float("-inf")
    config = read_config()
    move_list = config['move_list']
    rows = config['map_size'][0]
    cols = config['map_size'][1]
    walls = config['walls']
    pits = config['pits']
    # Default action is None
    bestAction = 4
    actionList = []
    legalActions = []



    for move in move_list:
        if validMove(curr_position, move):
            legalActions.append(move)


    if len(legalActions) == 0:
        return None
    # Compute max Q-Value and best action
    else:
        for action in legalActions:
            qValue = getQValue(curr_position, action)
            if qValue > max_value:
                max_value = qValue
                bestAction = action
                actionList.append(action)
            elif qValue == max_value:
                actionList.append(action);


    # Return best Action
    if(actionList):
        return random.choice(actionList)
    else:
        return None


# def getAction(curr_position, epsilon):
#     """
#       Compute the action to take in the current state.  With
#       probability self.epsilon, we should take a random action and
#       take the best policy action otherwise.  Note that if there are
#       no legal actions, which is the case at the terminal state, you
#       should choose None as the action.
#
#       HINT: You might want to use util.flipCoin(prob)
#       HINT: To pick randomly from a list, use random.choice(list)
#     """
#     # Pick Action
#     legalActions = []
#     for move in moveList:
#         if validMove(curr_position, move, rows, cols, walls, pits):
#             legalActions.append(move)
#     action = None
#     # If legal action doesnt exist, return None
#     if len(legalActions) == 0:
#         return action
#
#     # If random value between 0 and 1.0 is less than epsilon, return random action
#     elif random.random() < epsilon):
#         return random.choice(legalActions)
#     # Else, return best action
#     else:
#         return self.computeActionFromQValues(curr_position)


def getQValue(curr_position, action):
    """
      Return the reward? TODO: Validate moves and return 0 if goal state
    """

    # print action
    # print curr_position
    qValue = qValues[tuple(curr_position), action]
    # TODO: check if qvalue is null?

    return qValue

def getMaxQValue(curr_position):
    """
      Return the reward? TODO: Validate moves and return 0 if goal state
    """
    config = read_config()
    move_list = config['move_list']
    max_value = float("-inf")

    for move in move_list:
        qValue = qValues[(tuple(curr_position), move)]
        if (qValue > max_value):
            max_value = qValue
    return max_value


def runQLearning(epsilonVal, alpha):
    config = read_config()
    height = config['map_size'][0]
    width = config['map_size'][1]
    wall_list = config['walls']
    pit_list = config['pits']
    danger_zone_list = config['danger_zone']
    goal = config['goal']
    start = config['start']
    move_list = config['move_list']

    reward_goal = config['reward_for_reaching_goal']
    reward_pit = config['reward_for_falling_in_pit']
    reward_wall = config['reward_for_hitting_wall']
    reward_step = config['reward_for_each_step']
    reward_danger_zone = config['reward_for_danger_zone']

    discount_factor = config['discount_factor']

    max_iterations = config['max_iterations']
    threshold_difference = config['threshold_difference']

    p_forward = config['prob_move_forward']
    p_backward = config['prob_move_backward']
    p_left = config['prob_move_left']
    p_right = config['prob_move_right']

    global epsilon
    epsilon = epsilonVal

    # Intialize policy map and reward map
    #policy = init_policy(wall_list, pit_list, goal, width, height)
    #reward = init_reward(wall_list, pit_list, goal, reward_pit, reward_goal, reward_wall, width, height)


    # Initialize q-value dictionary
    for row in range(0, height):
        for col in range(0, width):
            curr_position = [row,col]
            for move in move_list:
                key = (tuple(curr_position), move)
                '''
                if curr_position in pit_list:
                    print "pit"
                    qValues[key] = reward_pit
                elif cmp(curr_position, goal) == 0:
                    print "goal"
                    qValues[key] = reward_goal
                elif curr_position in wall_list:
                    print "wall"
                    qValues[key] = reward_wall
                else:
        	    qValues[key] = 0.0
                '''
                qValues[key] = 0.0
                '''
                #Incorrect implementation of danger_zone
                elif curr_position in danger_zone_list:
                    print "danger zone"
                    qValues[key] = reward_danger_zone
                '''

    curr_position = tuple(start)
    
    robot_health = 100;

    for iteration in range(0, max_iterations):

        # From current position, find the q-value maximizing action
        action = computeActionFromQValues(curr_position)

        # Get position after the move
        new_position = getLocationAfterMoveWithProb(curr_position, action, p_forward, p_backward, p_left, p_right)
        #new_position = getLocationAfterMove(curr_position, action)

        # update q-value
        # u_i = (reward_step + discount_factor * (max Q value from new position) )
        # Q_new(S,a) = (1-alpha)Q_old(s,a)+ alpha * temp
       
        additional_reward = 0.0
        if list(new_position) in wall_list:
            additional_reward += reward_wall
        elif list(new_position) in danger_zone_list:
            additional_reward += reward_danger_zone
            #print "in danger"
            robot_health -= 50;
        elif list(new_position) in pit_list:
            additional_reward += reward_pit
        elif cmp(new_position, goal):
            additional_reward += reward_goal
        
        print robot_health
        #Check if robot has been shot down. If so, terminal state equivalent to pit
        if robot_health <= 0:
            #print "robot shot down"
            additional_reward += reward_pit;


        u_i = reward_step + additional_reward + discount_factor * (getMaxQValue((new_position)))
        new_qValue = (1-alpha) * getQValue(curr_position,action) + alpha * u_i


        # calculate
        # action_prime = computeActionFromQValues(new_position)
        # qValue_prime = computeValueFromQValue(curr_position, action_prime)
        # qValue_prime = float(qValue_prime) * float(discount_factor)
        # qValue = qValues{(curr_position, action_prime)}
        # state_reward = reward[action[0]][action[1]]
        # updatedQValue = (1-alpha) * qValue + alpha * (state_reward + qValue_prime - qValue)

        # Put the update Q-Value to the Q-Values list
        #self.qValues.remove((state, action, qValue))
        qValues[(tuple(curr_position),action)] = new_qValue
        curr_position = new_position

        # If reached an terminal position, return to start
        if list(curr_position) in pit_list:
            curr_position = start
            robot_health = 100;
        elif cmp(list(curr_position), goal) == 0:
            curr_position = start
            robot_health = 100;
        elif robot_health <= 0:
            robot_health = 100;
            curr_position = start


    return qValues
