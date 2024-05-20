from backbone_classes import *
from events.oldEvents import *
from events.restaurantEvents import *
from events.events import *
from events.health_events import *
from events.law_events import *
from events.love_events import *
from events.generatedEvents import *

from path_finding import *
from AStar_Path_Finding import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import csv

def extract_drama_vals(path):
    # From a completed story path, pull out all the drama values in a list format.
    dramaVals = []
    for worldstate in path:
        dramaVals.append(worldstate.drama_score)
    return dramaVals
'''
if __name__ == "__main__":

    NoRestaurantPossibleEvents = [CoffeeSpill(), DoNothing(), ThrowDrink(), Befriend(), HitOnAccepted(),
                                  HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(),
                                  IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(),
                                  BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(),
                                  SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(),
                                  SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                                  GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                                  HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                                  AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]


    numStories = 10
    alphaValues = [1]
    alphaValues.reverse()
    ## Leaving out 0 and 1.0 values as 1.0 is pure random exploration and 0 is going to get stuck in local minimum and take *forever* to resolve.
    for i in range (10):
        for alphaVal in alphaValues:
            #initWorldState, waypoints = SciFiwaypointTestEnvironment()
            initWorldState, waypoints = SciFiwaypointTestEnvironmentSimple()
            start_state = initWorldState
            storyPath, VisitedStates = chained_astar_search(start_state, waypoints, get_neighbors, heuristic,
                                                            NoRestaurantPossibleEvents, alpha=alphaVal)
            searchLength = [alphaVal, VisitedStates] # Alpha value, and length of search
            # Specify the existing CSV file name
            csv_filename = "alpha+visitedStatesCorrectedSimple.csv"
            # Append the list to the existing CSV file
            with open(csv_filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(searchLength)

'''

if __name__ == "__main__":

    NoRestaurantPossibleEvents = [CoffeeSpill(), DoNothing(), ThrowDrink(), Befriend(), HitOnAccepted(),
                                  HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(),
                                  IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(),
                                  BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(),
                                  SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(),
                                  SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                                  GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                                  HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                                  AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]


    numStories = 10
    alphaValues = [0.6, 0.7, 0.8, 0.9, 1]
    #alphaValues.reverse()
    ## Leaving out 0 and 1.0 values as 1.0 is pure random exploration and 0 is going to get stuck in local minimum and take *forever* to resolve.
    for i in range (10):
        for alphaVal in alphaValues:
            initWorldState, waypoints = SciFiwaypointTestEnvironment()
            #initWorldState, waypoints = SciFiwaypointTestEnvironmentSimple()
            start_state = initWorldState
            storyPath, VisitedStates = chained_astar_search(start_state, waypoints, get_neighbors, heuristic,
                                                            NoRestaurantPossibleEvents, alpha=alphaVal)
            searchLength = [alphaVal, VisitedStates] # Alpha value, and length of search
            # Specify the existing CSV file name
            csv_filename = "Saved Drama Data/alpha+visitedStatesHighComplexity.csv"
            # Append the list to the existing CSV file
            with open(csv_filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(searchLength)