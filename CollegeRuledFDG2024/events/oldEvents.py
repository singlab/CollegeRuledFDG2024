from backbone_classes import *
import copy


class MoneyProblems(PlotFragment):
    def __init__(self):
        self.drama = 12

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 5):
            return False, None, environments
        for character in worldstate.characters:
            if not (character.has_job):
                if self.withinRecentHistoryLimit(worldstate, [character], [], 3):
                    if self.withinInstanceLimit(worldstate, [character], [], 2):
                        valid_characters.append([character])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("After paying for a meal", \
                  "{} closes their wallet and grimaces. They're dangerously low on cash and don't know how much longer "\
                  "than can survive like this.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-2)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class GetMiningJob(PlotFragment):
    def __init__(self):
        self.drama = -10

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 5):
            return False, None, environments
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
                if self.withinRecentHistoryLimit(worldstate, [character], [], 3):
                    if self.withinInstanceLimit(worldstate, [character], [], 2):
                        valid_characters.append([character])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("After visiting the open market every day and getting increasingly desperate", \
                "{} got a mining job. They sigh in relief.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(2)
        char.has_job = True
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class GetRejectedFromJob(PlotFragment):
    def __init__(self):
        self.drama = 7

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 5):
            return False, None, environments
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
                if self.withinRecentHistoryLimit(worldstate, [character], [], 3):
                    if self.withinInstanceLimit(worldstate, [character], [], 2):
                        valid_characters.append([character])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("Despite their best efforts,", \
                  "{} can't seem to catch a break in the job hunt. They purse their lips while they wordlessly discard another rejection lettter.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-1)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)



class GetSpaceShuttleJob(PlotFragment):
    def __init__(self):
        self.drama = -4

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if not character.has_job:
                if self.withinRecentHistoryLimit(worldstate, [character], [], 3):
                    if self.withinInstanceLimit(worldstate, [character], [], 1):
                        valid_characters.append([character])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} got a job flying transport shuttles for interplanet exports. It's a relief to have a stable income again, even it if is a more dangerous trade".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(5)
        char.has_job = True
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class LoseJob(PlotFragment):
    def __init__(self):
        self.drama = 11

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if character.has_job:
                if self.withinRecentHistoryLimit(worldstate, [character], [], 3):
                    if self.withinInstanceLimit(worldstate, [character], [], 2):
                        valid_characters.append([character])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("The empire decreases exports from Higgins and the economy takes a hit. {} loses their job.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-5)
        char.has_job = False
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


