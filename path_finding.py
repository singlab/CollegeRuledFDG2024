from backbone_classes import *
from events.oldEvents import *
import random

from run import *


def selectEventIndex(eventList, desiredWorldState):
    if len(eventList) == 0: # TODO: Handle this before calling it, rather than after.
        print("No events left in this tree!")
        return 0, float('inf')

    currEventMinDistance = float('inf')
    equallyValubleIndexes = []
    for x in range (len(eventList)):
        reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
        currEventValue = distanceBetweenWorldstates(reachable_worldstate, desiredWorldState)

        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)


    if len(equallyValubleIndexes) >= 1:
        return random.choice(equallyValubleIndexes), currEventMinDistance # Return the index of the event with the lowest distance to the desiredWorldState
    else:
        return 0, float('inf')

def getBestIndexLookingAhead(depth, eventList, desiredWorldState, possible_events):
    if depth == 1:
        return selectEventIndex(eventList, desiredWorldState)

    if depth >= 2:
        currEventMinDistance = float('inf')
        equallyValubleIndexes = []

        for x in range (len(eventList)):
            reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
            runable_events = getRunableEvents(reachable_worldstate, possible_events)
            currWorldStateValue = getBestIndexLookingAhead(depth-1, runable_events, desiredWorldState, possible_events)

            if (currWorldStateValue[1] < currEventMinDistance):
                equallyValubleIndexes = []
                currEventMinDistance = currWorldStateValue[1]
                equallyValubleIndexes.append(x)

            if (currWorldStateValue[1] == currEventMinDistance):
                equallyValubleIndexes.append(x)

        return random.choice(equallyValubleIndexes), currEventMinDistance

def determineDramaCurveDistance(currWorldState, penalizeIncomplete = False):
    distance = 0
    #TODO: Implement function that takes in a worldstate, looks back along the curve and drama values, and sums the
    # distance from each individual worldstate in the history to the target value at that index.
    dramaTargets = currWorldState.drama_curve.drama_targets

    #print("Is this being called??")
    # First step is to assemble the current drama scores
    steps = len(currWorldState.event_history)
    currDramaScores = []
    currDramaScores.append(currWorldState.drama_score) # Grab first value
    priorWS = currWorldState.prior_worldstate
    while priorWS: #Recursively parse down the prior states and grab their drama scores
        currDramaScores.append(priorWS.drama_score)
        priorWS = priorWS.prior_worldstate
    dramaPath = list(currDramaScores)
    dramaPath.reverse()
    totalDistance = 0
    #print(dramaPath)
    for i in range(steps):
        target = dramaTargets[i]
        actual = dramaPath[i+1]
        totalDistance += round(abs(target-actual)) # Sum the distances between targets and actual values at each point
    #if totalDistance > 100:
        #print("debug!")

    # If enabled, penalize stories not reaching full length in order to push story length to match.
    if penalizeIncomplete:
        currStoryLen = len(dramaPath)
        targetStoryLen = len(dramaTargets)
        targetsToGrab = targetStoryLen - currStoryLen
        dramaPenalty = sum(dramaTargets[-targetsToGrab:])*.6
        totalDistance += dramaPenalty

    return totalDistance




def distanceBetweenWorldstates(currWorldState, newWorldState, drama_weight = 0.4, causalityWeight = 15, deadCharacterPenalty = 150, penalizeIncomplete = False):
    distance = 0

    if currWorldState.characters:
        for character in currWorldState.characters:
            for future_character in newWorldState.characters:
                if future_character.name == character.name:
                    charFound = True
                    distanceBetweenVersions = character.getDistanceToFutureState(future_character.getAttributes())
                    distance += distanceBetweenVersions

    for future_character in newWorldState.characters:
        charFound = False
        for character in currWorldState.characters:
            if future_character.name == character.name:
                charFound = True
        if charFound == False:
            distance += deadCharacterPenalty

    #if len(currWorldState.characters) != len(newWorldState.characters):
        #deadCharacterPenalty = abs(len(currWorldState.characters)-len(newWorldState.characters)) * 150 # Change this value to change weight of undesired deaths.
        #distance += deadCharacterPenalty

    determineCausalityScore(currWorldState)
    causalityScore = currWorldState.totalCausalScore
    #if causalityScore > 1:
        #print(str(causalityScore) + " -- Reduced")
    if causalityScore != 0:
        distance -= causalityScore * causalityWeight

    # Drama scores using drama curve methodology
    if currWorldState.getDramaCurve() != None:
        drama_distance = determineDramaCurveDistance(currWorldState, penalizeIncomplete)
        weightedDramaDistance = drama_distance * drama_weight
        distance += weightedDramaDistance

        if drama_weight == 0:
            # Then this is for testing purposes. We want a max-length story.
            distance -= len(currWorldState.event_history)
        return distance

    # Drama scoring using arbitrary assigned target for a waypoint
    if currWorldState.drama_score != None:
        drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * drama_weight
        weightedDramaDistance = drama_distance * drama_weight
        distance += weightedDramaDistance
        #print(drama_distance)
    return distance

def determineCausalityScore(currWorldState):
    # Look back along the path of worldstate. If along the event history, there are events that are causal
    # (ie happen immediately after they become possible), we reduce the distance heuristic from that worldstate
    # to the target worldstate for the pourposes of pathfinding selection, but not for hitting waypoints.
    # We use each worldstate's stored event history for this, in this manner:
    if len(currWorldState.event_history) == 0:
        return 0

    lastEvent = currWorldState.event_history[-1 * 1:][0]
    eventStr = str(lastEvent[0])
    charsStr = lastEvent[1]
    envStr = lastEvent[2]
    lastEventString = eventStr + charsStr + envStr

    oldPossibleEvents = None
    if currWorldState.prior_worldstate != None:
        prior = currWorldState.prior_worldstate
        if prior.prior_worldstate != None:
            oldPossibleEvents = prior.prior_worldstate.runnable_events

    if oldPossibleEvents:
        if lastEventString in oldPossibleEvents:
            #print("non-casual event.")
            currWorldState.causal = 0
            return 0
        else:
            #print("causal event.")
            currWorldState.causal = 1
            currWorldState.totalCausalScore = prior.totalCausalScore + 1
            return 1
    return 0

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possible_events: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents

def getReachableWorldstates(current_worldstate, possible_events, depthlimit = 0):
    if depthlimit == 0:
        NeighborWorldstates = []
        runableEvents = getRunableEvents(current_worldstate, possible_events)
        for x in range (len(runableEvents)):
            reachable_worldstate = runableEvents[x][0].getNewWorldState(runableEvents[x][1], runableEvents[x][2], runableEvents[x][3])
            NeighborWorldstates.append(reachable_worldstate)
        return NeighborWorldstates
    else:
        if len(current_worldstate.event_history) < depthlimit:
            NeighborWorldstates = []
            runableEvents = getRunableEvents(current_worldstate, possible_events)
            for x in range(len(runableEvents)):
                reachable_worldstate = runableEvents[x][0].getNewWorldState(runableEvents[x][1], runableEvents[x][2],
                                                                            runableEvents[x][3])
                NeighborWorldstates.append(reachable_worldstate)
            return NeighborWorldstates
        return []
