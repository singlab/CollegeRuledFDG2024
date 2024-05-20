from backbone_classes import *
import copy

"""
Actions Characters Can Take / Events:
Character Arrives in scene
Character leaves the scene
Character A shake hands with Character B
Character A talks to Character B
Character A hits on Character B
Character A Insults Character B
Character A Attacks Character B
Character A Plays a game with Character B
Character A sits down at a table
Character A eats food.
Character A orders food.
Host delivers food to the table. 
Host slips and throws food on Character B
Character A throws drink in Character B’s face

Jessica, Walk_In
Jessica, Walk_Out
Jessica, Approach_Dylan
Jessica, Chat_Dylan
Jessica, React_Positive
Jessica, React_Negative
Jessica, Throw_Drink
Dylan, Walk_In
Dylan, Walk_Out
Dylan, Approach_Jessica
Dylan, Chat_Jessica
Dylan, React_Positive
Dylan, React_Negative
Dylan, Throw_Drink
"""

class ArrivesInRestaurant(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
                if character.location != (worldstate.getEnvironmentByName("Restaurant")):
                    valid_characters.append([character])
                    environments.append([worldstate.getEnvironmentByName("Restaurant")])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print(
                "{} arrives in the restaurant".format(
                    characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)

        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index] # Grab the character in the reachable worldstate.
        env_index = worldstate.environments.index(environment[0])
        newEnv = reachable_worldstate.environments[env_index] # Grab the environment
        char.location = newEnv # Update character in the new environment
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment) # Pass back new worldstate.

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        f.write(character + ", Walk_In\n")
        return

class LeavesRestaurant(PlotFragment):
    def __init__(self):
        self.drama = -15

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 4):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.location != (worldstate.getEnvironmentByName("Street")):
                if character.name != "Waiter":
                    valid_characters.append([character])
                    environments.append([worldstate.getEnvironmentByName("Street")])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print(
                "{} leaves the restaurant".format(
                    characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)

        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index] # Grab the character in the reachable worldstate.
        env_index = worldstate.environments.index(environment[0])
        newEnv = reachable_worldstate.environments[env_index] # Grab the environment
        char.location = newEnv # Update character in the new environment
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment) # Pass back new worldstate.

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        f.write(character + ", Walk_Out\n")
        return

class AquireBeverage(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 4):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.location == (worldstate.getEnvironmentByName("Restaurant")):
                if character.has_beverage == False:
                    valid_characters.append([character])
                    environments.append([worldstate.getEnvironmentByName("Restaurant")])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print(
                "{} grabs a drink from the table".format(
                    characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)

        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index] # Grab the character in the reachable worldstate.
        env_index = worldstate.environments.index(environment[0])
        newEnv = reachable_worldstate.environments[env_index] # Grab the environment
        char.has_beverage = True
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment) # Pass back new worldstate.

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        # f.write(character + ", Grab_Drink\n")
        # Not currently implemented
        return


class CoffeeSpill(PlotFragment):
    def __init__(self):
        self.drama = 15

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, []
        valid_characters = []
        environments = []

        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    character.updateRelationship(character2, 0)  # if no relationship, add to relationship table
                    if (character.relationships[character2] >= -15):
                        if character.sameLoc(character2):
                            if character.has_beverage:
                                if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                                    if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
                                        valid_characters.append([character, character2])
                                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} is walking along with a fresh cup of coffee, and loses their footing right as they would pass by {}, spilling their drink all over them! \"Oh goodness, sorry about that!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, 3)
        char_two.updateRelationship(char, -5)
        char.has_beverage = False
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        f.write(character + ", Spill_Drink\n")
        return

class ThrowDrink(PlotFragment):
    def __init__(self):
        self.drama = 20

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, []
        valid_characters = []
        environments = []

        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    character.updateRelationship(character2, 0)  # if no relationship, add to relationship table
                    if (character.relationships[character2] <= -15):
                        if character.sameLoc(character2):
                            if character.has_beverage:
                                if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                                    if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
                                        valid_characters.append([character, character2])
                                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} intentionally dumps their drink all over {}! \"Get stuffed, twerp!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, -5)
        char_two.updateRelationship(char, -55)
        reachable_worldstate.drama_score += self.drama
        char.has_beverage = False
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        character2 = characters[1].name
        f.write(character + ", Approach_" + character2 + "\n")
        f.write(character + ", Throw_Drink\n")
        f.write(character2 + ", React_negative\n")
        return

class Befriend(PlotFragment):
    def __init__(self):
        self.drama = 6

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        character.updateRelationship(character2, 0)  # if no relationship, add to relationship table
                        if (character.relationships[character2] >= 0):
                            if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                                if self.withinRecentHistoryLimit(worldstate, [character2, character], [], 2):
                                    if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
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
            print("{} approaches {} and strikes up a conversation. Good conversation ensues".format(characters[0].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 15)
        char_two.updateRelationship(char_one, 15)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        character2 = characters[1].name
        f.write(character + ", Approach_" + character2 + "\n")
        f.write(character + ", Chat_" + character2 + "\n")
        return

class HitOnAccepted(PlotFragment):
    def __init__(self):
        self.drama = 6

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        character.updateRelationship(character2, 0)  # if no relationship, add to relationship table
                        if (character.relationships[character2] >= 25):
                            if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                                if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
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
            print("{} flirts with {}, and {} blushes.".format(characters[0].name, characters[1].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 5)
        char_two.updateRelationship(char_one, 20)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        character2 = characters[1].name
        f.write(character + ", Approach_" + character2 + "\n")
        f.write(character + ", Chat_" + character2 +"\n")
        f.write(character2 + ", React_Positive\n")
        return

class HitOnRejected(PlotFragment):
    def __init__(self):
        self.drama = 11

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        character.updateRelationship(character2, 0)  # if no relationship, add to relationship table
                        if (character.relationships[character2] >= 25):
                            if (character2.relationships[character] <= 5):
                                if self.withinRecentHistoryLimit(worldstate, [character, character2], [], 3):
                                    if self.withinInstanceLimit(worldstate, [character, character2], [], 2):
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
            print("{} slings a pickup line at {}, and {} is not amused. They glare in response".format(characters[0].name, characters[1].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, -15)
        char_two.updateRelationship(char_one, -15)
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def appendAnimationCommand(self, worldstate, characters, environment):
        f = open("testStory.txt", "a")
        character = characters[0].name
        character2 = characters[1].name
        f.write(character + ", Approach_" + character2 + "\n")
        f.write(character + ", Chat_" + character2 +"\n")
        f.write(character2 + ", React_Negative\n")
        return


class DoNothing(PlotFragment):
    # Purely exists to allow some flexibility in pacing.
    def __init__(self):
        self.drama = 0

    def checkPreconditions(self, worldstate):
        if self.withinRecentHistoryLimit(worldstate, [], [], 3):
            return True, [[]], [[]]
        return False, [[]], [[]]

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        #if print_event == True:
        #    print(".")
        self.appendAnimationCommand(worldstate, characters, environment)
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)