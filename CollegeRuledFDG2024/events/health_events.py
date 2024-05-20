from backbone_classes import *
import copy


class HitBySpaceCar(PlotFragment):
    """ 
    My roommates say if they hit someone with a spacecar, they'd
    be more inclined towards being kind to that person. So the driver's
    relationship to the victim will go up, and the victim's relationship to
    the driver will go down.
    """
    def __init__(self):
        self.drama = 14

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
                for character2 in worldstate.characters:
                    if character != character2:
                        valid_characters.append([character, character2])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 2)
        char_two.updateRelationship(char_one, -10)
        char_two.updateHealth(-6)
        if print_event:
            self.drama = 14
            print("{} hits {} with their spacecar.".format(char_one.name, char_two.name))
        if char_two.isDead():  # kill character
            self.drama = 19  # more dramatic if character dies
            reachable_worldstate.removeCharacter(char_two)
            if print_event:
                print("As {} lay there on the spaceway, they stared up at two moons rising over the dusky" \
                    " horizon. Then they closed their eyes for the last time.".format(char_two.name)) 
            char_one.murderer = True

        #print("Drama score before change")
        #print(reachable_worldstate.drama_score)
        #print("Drama score incremented by:")
        #print(self.drama)
        reachable_worldstate.drama_score += self.drama
        #print("New drama:")
        #print(reachable_worldstate.drama_score)
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class HospitalVisit(PlotFragment):
    def __init__(self):
        self.drama = -6
    
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            if character.health < 3:
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHealth(5)
        if print_event:
            print("{} goes to the hospital to recover their health.".format(char.name))
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)
