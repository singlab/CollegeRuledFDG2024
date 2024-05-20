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

if __name__ == "__main__":

    NoRestaurantPossibleEvents = [CoffeeSpill(), ThrowDrink(), Befriend(), HitOnAccepted(),
                                  HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(),
                                  IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(),
                                  BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(),
                                  SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(),
                                  SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                                  GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                                  HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                                  AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]


    numStories = 5
    dramaValList = []
    for z in range(numStories):
        f = open("testStory.txt", "w")
        # Drama curve Initialization
        #params = [[5.5, 8], [2.5, 13]]
        #testCurve = DramaCurve(2, params, 16, 70)

        # Drama curve Initialization
        params = [[2.6, 6], [2, 13]]
        testCurve = DramaCurve(2, params, 16, 70)
        initWorldState, waypoints = SciFiwaypointTestEnvironmentParam(testCurve)
        start_state = initWorldState
        #initWorldState, waypoints = RandomWalkEnvironment()
        #start_state = initWorldState
        storyPath, VisitedStates = chained_astar_search(start_state, waypoints, get_neighbors, heuristic,
                                                        NoRestaurantPossibleEvents, depthLimit=15, alpha=.2, drama_weight=2, causalityWeight=20, deadCharacterPenalty=150, penalizeIncomplete=False)
        dramaVals = extract_drama_vals(storyPath)
        f.close()

        # Ensure the list has 15 values by appending zeros
        if len(dramaVals) < 15:
            dramaVals.extend([0] * (15 - len(dramaVals)))

        # Specify the existing CSV file name
        #csv_filename = "dramaValues_1_15_70_penalize_incomplete_no_cost.csv"
        #csv_filename = "dramaValues_2_15_70_penalize_incomplete_no_cost_0.6_highalpha.csv"
        csv_filename = "FDG2024Demo.csv"
        # Append the list to the existing CSV file
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(dramaVals)