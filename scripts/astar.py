# astar implementation needs to go here

import Queue
from itertools import izip

def makePair(move):
    return (move[0],move[1])

def makeList(move):
    return [move[0], move[1]]

def manhattanDistance(current, goal):
    (x1, y1) = current
    (x2, y2) = goal
    return abs(x1-x2)+abs(y1-y2)

def validMove(curr_position, move, rows, cols, walls, pits):
    new_position = [curr_position[0]+move[0], curr_position[1]+move[1]]

    #Check if out of bounds
    if new_position[0] < 0 or new_position[0] > rows or new_position[1] < 0 or new_position[1] > cols:
        return False

    #Check if in wall or pit
    if new_position == walls or new_position == pits:
        return False

    return True



def runAStar(moveList, start, goal, walls, pits, rows, cols):
    
    '''
    print "Move list: " + str(moveList)
    print "Start: " + str(start)
    print "Goal: " + str(goal)
    print "Walls: " + str(walls)
    print "Pits: " + str(pits)
    '''

    possible_moves = Queue.PriorityQueue()
    possible_moves.put(makePair(start), 0)

    previous_move = {}
    path_cost = {}

    print makePair(start)

    previous_move[makePair(start)] = None
    path_cost[makePair(start)] = 0

    while not possible_moves.empty():
        curr_position = possible_moves.get()
        print curr_position

        if curr_position == makePair(goal):
            print "GOAL REACHED!"
            shortest_path = []
            while previous_move[curr_position] != None:
                shortest_path.append(makeList(curr_position))
                curr_position = previous_move[curr_position]
            shortest_path.append(makeList(curr_position))
            return shortest_path[::-1]
        
        for move in moveList:
            if validMove(curr_position, move, rows, cols, walls, pits):
                new_position = (curr_position[0]+move[0], curr_position[1]+move[1])
                move_cost = path_cost[curr_position] + 1
                if new_position not in path_cost or move_cost < path_cost[new_position]:
                    path_cost[new_position] = move_cost
                    fx = move_cost + manhattanDistance(new_position, goal)
                    possible_moves.put(new_position, fx)
                    previous_move[new_position] = curr_position

    return []
 

