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
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
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
        self.drama = 4

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if not character.has_job:
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} got a job flying transport shuttles for interplanet exports. It's a releif to have a stable income again, even it if is a more dangerous trade".format(characters[0].name))
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



class CoffeeSpill(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            for character2 in character.relationships:
                if character.sameLoc(character2):
                    if character != character2:
                        valid_characters.append([character, character2])
                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} is walking along with a fresh cup of hydrozine, and loses their footing right as they would pass by {}, spilling their drink all over them! \"Oh goodness, sorry about that!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, 3)
        char_two.updateRelationship(char, -5)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class DoNothing(PlotFragment):
    def __init__(self):
        self.drama = 0

    def checkPreconditions(self, worldstate):
        if self.withinRecentHistoryLimit(worldstate, [], [], 3):
            return True, [[]], [[]]
        return False, [[]], [[]]

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event == True:
            print(".")
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

