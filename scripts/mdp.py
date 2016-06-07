from read_config import read_config
from operator import itemgetter
from copy import deepcopy
import math

def init_policy(wall_list, pit_list, goal, width, height):
    for y in range(0,height):
    	temp = []
    	for x in range (0,width):
            temp_list = [y,x]
            if [y,x] in pit_list:
                temp.append('PIT')
            elif cmp(temp_list, goal) == 0:
                temp.append('GOAL')
            elif [y,x] in wall_list:
                temp.append('WALL')
            else:
    		    temp.append('N/A')

    	if (y == 0):
    		policy = [temp]
    	else:
    		policy.append(temp)
    return policy

def init_reward(wall_list, pit_list, goal_loc, pit, goal, wall, width, height):
    for y in range(0,height):
        temp = []
        for x in range(0,width):
            temp_list = [y,x]
            if [y,x] in pit_list:
                temp.append(pit)
            elif cmp(temp_list, goal_loc) == 0:
                temp.append(goal)
            elif [y,x] in wall_list:
                temp.append('WALL')
            else:
    		    temp.append(0.0)

        if (y == 0):
            reward = [temp]
        else:
            reward.append(temp)
    return reward

def getMoves(move, p_forward, p_backward, p_left, p_right):
    retVal = []
    # move up
    if (move == [1,0]):
      prob_move_up = p_forward
      prob_move_down = p_backward
      prob_move_right = p_right
      prob_move_left = p_left

      retVal.append(([1,0], prob_move_up))
      retVal.append(([-1,0], prob_move_down))
      retVal.append(([0,-1], prob_move_left))
      retVal.append(([0,1], prob_move_right))
      return retVal

    # move down
    elif (move == [-1,0]):
      prob_move_up = p_backward
      prob_move_down = p_forward
      prob_move_right = p_left
      prob_move_left = p_right

      retVal.append(([1,0], prob_move_up))
      retVal.append(([-1,0], prob_move_down))
      retVal.append(([0,-1], prob_move_left))
      retVal.append(([0,1], prob_move_right))
      return retVal

    # move right
    elif (move == [0,1]):
      prob_move_up = p_left
      prob_move_down = p_right
      prob_move_right = p_forward
      prob_move_left = p_backward

      retVal.append(([1,0], prob_move_up))
      retVal.append(([-1,0], prob_move_down))
      retVal.append(([0,-1], prob_move_left))
      retVal.append(([0,1], prob_move_right))
      return retVal

    # move left
    elif (move == [0,-1]):
      prob_move_up = p_right
      prob_move_down = p_left
      prob_move_right = p_backward
      prob_move_left = p_forward

      retVal.append(([1,0], prob_move_up))
      retVal.append(([-1,0], prob_move_down))
      retVal.append(([0,-1], prob_move_left))
      retVal.append(([0,1], prob_move_right))
      return retVal

    # unrecognized move
    else:
        print('Illegal Move')


def runMDP(policy_pub):
    config = read_config()
    height = config['map_size'][0]
    width = config['map_size'][1]
    wall_list = config['walls']
    pit_list = config['pits']
    goal = config['goal']
    start = config['start']
    move_list = config['move_list']

    reward_goal = config['reward_for_reaching_goal']
    reward_pit = config['reward_for_falling_in_pit']
    reward_wall = config['reward_for_hitting_wall']
    reward_step = config['reward_for_each_step']

    discount_factor = config['discount_factor']

    max_iterations = config['max_iterations']
    threshold_difference = config['threshold_difference']

    p_forward = config['prob_move_forward']
    p_backward = config['prob_move_backward']
    p_left = config['prob_move_left']
    p_right = config['prob_move_right']


    # Intialize policy map and reward map
    policy = init_policy(wall_list, pit_list, goal, width, height)
    reward = init_reward(wall_list, pit_list, goal, reward_pit, reward_goal, reward_wall, width, height)

    #print reward
    #print policy


    # Start Value Iteration
    for k in range(0,max_iterations):
        next_reward = deepcopy(reward)
        print k
        print ""
        for y in range(0,height):
            for x in range(0,width):
                sum_list = []

                if [y,x] == goal:
                    next_reward[y][x] = reward[y][x]
                elif [y,x] in wall_list:
                    next_reward[y][x] = reward[y][x]
                elif [y,x] in pit_list:
                    next_reward[y][x] = reward[y][x]
                else:

                    for move in move_list:
                        chance_moves, chance_probs = zip(*getMoves(move, p_forward, p_backward, p_left, p_right))
                        sum = 0.0
                        for i in range(0,len(chance_moves)):
                            curr_x = x + chance_moves[i][1]
                            curr_y = y + chance_moves[i][0]
                            if chance_moves[i] == 0:
                                sum = sum
                            elif ([curr_y,curr_x] in wall_list) or curr_y > height-1 or curr_y < 0 or curr_x > width-1 or curr_x < 0:
                                sum = sum + ( chance_probs[i] * ( (discount_factor * (reward[y][x]) ) + reward_wall) )
                            else:
                                sum = sum + ( chance_probs[i] * ( (discount_factor * reward[curr_y][curr_x] ) + reward_step) )
                        sum_list.append((sum, move))
                    max_value, max_move = max(sum_list, key=lambda item:item[0])
                    next_reward[y][x] = max_value

                    #print str(y) + ", " + str(x) + ":"
                    #print sum_list
                    if (max_move == [-1,0]):
                        best_action = 'N'
                    if (max_move == [1,0]):
                        best_action = 'S'
                    if (max_move == [0,-1]):
                        best_action = 'W'
                    if (max_move == [0,1]):
                        best_action = 'E'
                    #print best_action
                    policy[y][x]= best_action


        if (k != 0):
            sumOfDifference = 0.0
            for y in range(0, height):
                for x in range(0, width):
                    if [y,x] not in wall_list and [y,x] not in pit_list:
                        sumOfDifference = sumOfDifference + abs(reward[y][x] - next_reward[y][x])

            if (sumOfDifference < threshold_difference) or k == max_iterations-1:
                #print sumOfDifference
                #print k
                #print rewardj
                print ""
                print next_reward
                print policy
                return policy


        #publish policy
        flat_policy = []
        for y in range(0,height):
            for x in range(0,width):
                flat_policy.append(policy[y][x])

        policy_pub.publish(flat_policy)

        reward = next_reward
