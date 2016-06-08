#!/usr/bin/env python

import rospy
import random as r
import math as m
import numpy as np
from copy import deepcopy
from std_msgs.msg import String, Bool, Float32
from read_config import read_config
from astar import runAStar
from mdp import runMDP
from qlearning import runQLearning
from cse_190_assi_3.msg import AStarPath, PolicyList
import image_util

class Robot():
    moveList = []
    rows = 0
    cols = 0

    def __init__(self):
        global rows
        global cols
	global moveList

        pathList = []

	rospy.init_node("robot")

        """Read config file and setup ROS things"""
        self.config = read_config()
	#print "Initializing robot"
	moveList = deepcopy(self.config['move_list'])
        start = self.config['start']
        goal = self.config['goal']
        walls = self.config['walls']
        pits = self.config['pits']

        rows = self.config['map_size'][0]
        cols = self.config['map_size'][1]

        print "Rows: " + str(rows)
        print "Cols: " + str(cols)

	self.path_pub = rospy.Publisher(
		"/results/path_list",
	        AStarPath,
		queue_size = 10
	)

        self.policy_pub = rospy.Publisher(
                "/results/policy_list",
                PolicyList,
                queue_size = 10,
                latch = True
        )

        self.sim_complete = rospy.Publisher(
                "/map_node/sim_complete",
                Bool,
                queue_size = 10
        )


        #A*
        #print "Starting A*"
        #pathList = runAStar(moveList, start, goal, walls, pits, rows, cols)
        #print pathList
        #for step in pathList:
        #    print step
        #    rospy.sleep(1)
        #    self.path_pub.publish(step)


        #MDP
        #mdp_policy = runMDP(self.policy_pub)
        #print mdp_policy
        #sself.policy_pub.publish(mdp_policy)

        #Qlearning
        epsilonVal = .2
        iterations = 200
        alpha = 0.5
        qlearning_policy = runQLearning(epsilonVal, alpha);
        
        for row in range(0, rows):
            for col in range (0, cols):
                for move in range (0, 3):
                    tmp_position = (row, col)
                    qVal = qlearning_policy[(tuple(tmp_position), move)]
                    print "[(" + str(row) + "," + str(col) + "), " + str(move) + "]: " + str(qVal)

        #print qlearning_policy


        rospy.sleep(1)
        self.sim_complete.publish(True)
        rospy.sleep(1)

	rospy.signal_shutdown("Finished")

if __name__ == '__main__':
	Rb = Robot()
