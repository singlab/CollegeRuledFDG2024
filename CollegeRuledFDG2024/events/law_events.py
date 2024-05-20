from backbone_classes import *
import copy


class VentThroughAirlock(PlotFragment):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.location.has_airlock:
                for character2 in character.relationships:
                    if (character.relationships[character2] < 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])
                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = reachable_worldstate.environments[worldstate.environments.index(environment)] #Change this in the future, environment is a copy (bc deepcopy)
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class Steal(PlotFragment):
    def __init__(self):
        self.drama = 7

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
            if character.happiness < 6:
                for character2 in character.relationships:
                    if character != character2:
                        character.updateRelationship(character2, 0)
                        if character.relationships[character2] <= 0:
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        thief_idx = worldstate.characters.index(characters[0])
        victim_index = worldstate.characters.index(characters[1])
        thief = reachable_worldstate.characters[thief_idx]
        victim = reachable_worldstate.characters[victim_index]
        if print_event:
            print("{} notices {} forgot to lock up when they left their bunker.".format(thief.name, victim.name),
            "{} breaks in and steals all their valuables.".format(thief.name))
        thief.stole = True
        thief.updateHappiness(4)
        victim.updateHappiness(-4)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class GoToSpaceJail(PlotFragment):
    def __init__(self):
        self.drama = 10

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
            if (character.stole or character.exploited or character.murderer or character.fugitive) and not character.in_jail:
                characters = [character]
                environment = []
                if self.withinRecentHistoryLimit(worldstate, characters, environment, 5):
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
        char.updateHappiness(-5)
        if print_event:
            print("The law finally caught up with {}. They are in space jail.".format(characters[0].name))
        self.sendCharacterToJail(char, reachable_worldstate)
        char.in_jail = True
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)
        
    def sendCharacterToJail(self, character, worldstate):
        jail = False
        for location in worldstate.environments:
            if location.name == "Space Jail":
                jail = location
        if not jail:
            jail = Environment("Space Jail", -2)
            worldstate.environments.append(jail)
        character.location = jail


class SoloJailbreak(PlotFragment):
    def __init__(self):
        self.drama = 15
        #print("solo jailbreak drama:")
        #print(self.drama)

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.in_jail:
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
        char.updateHappiness(3)
        if print_event:
            print("{} spent months chipping at a crack in the circuit panel.".format(characters[0].name), \
                "They finally succeed at shutting down space jail long enough to make a break for it.", \
                "{} returns to their home planet, Higgins.".format(characters[0].name))
        char.in_jail = False
        char.fugitive = True
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class AssistedJailBreak(PlotFragment):
    def __init__(self):
        self.drama = 15

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.in_jail:
                for character2 in worldstate.characters:
                    character.updateRelationship(character2, 0) # Init relationship if need be
                    if character2.relationships[character] > 50:
                        valid_characters.append([character, character2])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char2_index = worldstate.characters.index(characters[1])
        char2 = reachable_worldstate.characters[char2_index]
        if print_event:
            line1 = "{} visits {} in Space Jail.".format(char2.name, char.name)
            line2 = "When the guards aren't looking, {} smuggles {} a screwdriver".format(char2.name, char.name)
            line3 = "{} uses the screwdriver to get into a high security docking port, where {} picks them up.".format(char.name, char2.name)
            line4 = "They speed off back to Higgins!"
            print(line1, line2, line3, line4)
        char.in_jail = False
        char.fugitive = True
        char2.fugitive = True
        char.updateRelationship(char2, 50)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class SabotagedJailBreak(PlotFragment):
    def __init__(self):
        self.drama = 9

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.in_jail:
                for character2 in worldstate.characters:
                    if character2.relationships[character] < 10:
                        if character != character2:
                            if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 5):
                                valid_characters.append([character, character2])
                                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char2_index = worldstate.characters.index(characters[1])
        char2 = reachable_worldstate.characters[char2_index]
        if print_event:
            line1 = "{} spent months chipping at a crack in the circuit panel.".format(char.name)
            line2 = "Just as they are about to escape, {} sees them and calls the guards!".format(char2.name)
            print(line1, line2)
        char.updateRelationship(char2, -50)
        char2.updateRelationship(char, -25)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)