import RandomPopHeapQ
from backbone_classes import *
from events.oldEvents import *
from events.restaurantEvents import *
from events.events import *
from events.health_events import *
from events.law_events import *
from events.love_events import *
from events.generatedEvents import *

from path_finding import *
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from run import SciFiwaypointTestEnvironmentAlt


class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state  # The current state of the node
        self.parent = parent  # The parent node
        self.cost = cost  # Cost to reach this node from the start node
        self.heuristic = heuristic  # Estimated cost to reach the goal from this node

    def total_cost(self):
        return self.cost + self.heuristic

    def __lt__(self, other):
        return (self.total_cost() < other.total_cost())

    def __gt__(self, other):
        return (self.total_cost() > other.total_cost(other))

def print_story(path):
    storyLength = len(path)
    startState = path[0]
    for i in range(storyLength-1):
        PriorState = path[i]
        CurrentState = path[i+1]
        EventTuple = CurrentState.event_history[i]
        EventType = EventTuple[0]
        eventCharacters = EventTuple[3]
        eventEnvironments = EventTuple[4]
        eventInstance = EventType()
        eventInstance.doEvent(worldstate=PriorState, characters=eventCharacters, environment=eventEnvironments)

def astar_search(start_state, goal_state, get_neighbors, heuristic, events, depthLimit = 15, alpha = 0.5, drama_weight = 0.4, causalityWeight = 15, deadCharacterPenalty = 150, penalizeIncomplete = False):
    open_set = []  # Priority queue for nodes to be evaluated
    closed_set = set()  # Set to keep track of visited nodes

    # Create the initial node
    start_node = Node(state=start_state, cost=0, heuristic=heuristic(start_state, goal_state, drama_weight, causalityWeight, deadCharacterPenalty, penalizeIncomplete))
    RandomPopHeapQ.heappush(open_set, (start_node.total_cost(), start_node))

    minDistance = None

    while open_set:
        if random.random() < alpha:
            #_, current_node = RandomPopHeapQ.heappop(open_set)
            _, current_node = RandomPopHeapQ.pop_random_min_entry(open_set)
        else:
            _, current_node = RandomPopHeapQ.heaprandpop(open_set)

        distanceToTarget = heuristic(current_node.state, goal_state, drama_weight, causalityWeight, deadCharacterPenalty, penalizeIncomplete)
        print(distanceToTarget)
        if distanceToTarget < 100:
            print(distanceToTarget)
        if distanceToTarget < goal_state.radius:
            # Found the goal, reconstruct the path
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent


            # Completed story should be formed. Now we wish to print it.
            path = list(path)
            path.reverse()
            #print_story(path)
            ExaminedWorldstates = len(open_set) + len(closed_set)
            print("Waypoint Hit!")
            return path, ExaminedWorldstates

        closed_set.add(current_node.state)

        if not minDistance:
            minDistance = distanceToTarget
            bestPath = []
        if distanceToTarget <= minDistance: # If we haven't found the desired path, but we are better than the current best route, store it in bestPath.
            bestPath = []
            minDistance = distanceToTarget
            tempNode = current_node
            while tempNode:
                bestPath.append(tempNode.state)
                tempNode = tempNode.parent
                bestPath = list(bestPath)
                bestPath.sort(key=lambda x: len(x.event_history), reverse=False)
                #if len(bestPath) > 5:
                #    print("debug")
                #print("Best path stored.")
                #print(bestPath)
        ExaminedWorldstates = len(open_set) + len(closed_set)
        if ExaminedWorldstates >= 15000: # If we haven't found the desired path, in a large number of iterations, store the best route found.
            print("Loosening Constraints due to difficulty discovering path. Consider adjusting story waypoints.")
            return bestPath, ExaminedWorldstates



        for neighbor_state in get_neighbors(current_node.state, events, depthLimit):
            if neighbor_state in closed_set:
                continue

            # TODO: Investigate how this cost affects length of final constructed stories.
            # Calculate the cost to reach the neighbor node
            #new_cost = current_node.cost + 5
            new_cost = current_node.cost

            # Check if the neighbor is already in the open set
            neighbor_node = next((node for _, node in open_set if node.state == neighbor_state), None)

            if not neighbor_node or new_cost < neighbor_node.cost:
                if neighbor_node:
                    open_set.remove((neighbor_node.total_cost(), neighbor_node))

                neighbor_node = Node(
                    state=neighbor_state,
                    parent=current_node,
                    cost=new_cost,
                    heuristic=heuristic(neighbor_state, goal_state, drama_weight, causalityWeight, deadCharacterPenalty, penalizeIncomplete)
                )
                RandomPopHeapQ.heappush(open_set, (neighbor_node.total_cost(), neighbor_node))

    # If no path is found, return an empty list
    print("No path found! Returning closest path.")
    ExaminedWorldstates = len(open_set) + len(closed_set)
    if bestPath:
        return [bestPath, ExaminedWorldstates]
    else:
        return [[], ExaminedWorldstates]

def get_neighbors(state, possible_events, depthLimit):
    state.getRunableEvents(possible_events)
    return getReachableWorldstates(state, possible_events, depthLimit)

#def heuristic(state, goal_state):
#    return distanceBetweenWorldstates(state, goal_state)

def heuristic(state, goal_state, dramaWeight, causalityWeight, deadCharWeight, penalizeIncomplete):
    return distanceBetweenWorldstates(state, goal_state, dramaWeight, causalityWeight, deadCharWeight, penalizeIncomplete)

def chained_astar_search(start_state, waypoints, get_neighbors, heuristic, events, depthLimit = 15, alpha = 0.5, drama_weight = 0.4, causalityWeight = 15, deadCharacterPenalty = 150, penalizeIncomplete = False):
    InitialState = start_state
    TotalWorldstatesVisited = 0
    FinalPath = []
    InitialState = start_state
    firstPath = True
    for waypoint in waypoints:
        if penalizeIncomplete & (waypoint == waypoints[len(waypoints)-1]):
                pathChunk, ExaminedStates = astar_search(InitialState, waypoint, get_neighbors, heuristic, events,
                                                         depthLimit, alpha, drama_weight, causalityWeight,
                                                         deadCharacterPenalty, True)
                TotalWorldstatesVisited += ExaminedStates
        else:
            pathChunk, ExaminedStates = astar_search(InitialState, waypoint, get_neighbors, heuristic, events, depthLimit, alpha, drama_weight, causalityWeight, deadCharacterPenalty, False)
            TotalWorldstatesVisited += ExaminedStates
        if firstPath:
            FinalPath = pathChunk
            firstPath = False
        else:
            skip = True
            for i in pathChunk:
                if skip:
                    skip = False
                else:
                    FinalPath.append(i)
        InitialState = pathChunk[len(pathChunk) - 1]
        depthLimit -= len(pathChunk)
    print(len(FinalPath))
    print_story(FinalPath)
    return FinalPath, TotalWorldstatesVisited

'''
NoRestaurantPossibleEvents = [CoffeeSpill(), DoNothing(), ThrowDrink(), Befriend(), HitOnAccepted(), HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(), IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(), BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(), SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(), SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                      GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                      HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                      AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]

initWorldState, waypoints = SciFiwaypointTestEnvironment()
start_state = initWorldState
goal_state = waypoints[0]
#path = astar_search(start_state, goal_state, get_neighbors, heuristic, NoRestaurantPossibleEvents)
path2, VisitedStates = chained_astar_search(start_state, waypoints, get_neighbors, heuristic, NoRestaurantPossibleEvents)
print(path2)
print(VisitedStates)
'''