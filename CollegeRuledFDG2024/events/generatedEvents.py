from backbone_classes import *
import copy
import random

import random

class BreakingPointDuel(PlotFragment):
    def __init__(self):
        self.drama = -20  # Higher negative drama score for an intense event & final resolution

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        # Define the threshold for a significant negative relationship
        significant_negative_threshold = -50  # Adjust as needed

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                significant_negative_threshold >= character.relationships[character2] >= -100
                        ):
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
            print(
                "{} and {} finally reach their breaking point. Their relationship has deteriorated to the point of no return.".format(
                    characters[0].name, characters[1].name
                )
            )
            print(
                "{} accuses {} of betrayal, and {} fires back with anger in their eyes.".format(
                    characters[0].name, characters[1].name, characters[1].name
                )
            )
            print(
                "Their voices rise in a heated argument, each word more hurtful than the last. The tension in the air is unbearable."
            )
            print(
                "{} and {} decide to settle their differences with a tragic duel.".format(
                    characters[0].name, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        # Duel results in one character being tragically wounded
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        # Simulate the duel and its consequences deterministically
        duel_winner, duel_loser = self.simulateDuel(char_one, char_two, print_event)

        # Apply injuries to the duel loser
        duel_loser.updateHealth(-40)  # Adjust injury severity as needed

        # Set relationship values to the lowest point, representing irreparable damage
        char_one.updateRelationship(char_two, -100)  # Irreparable damage
        char_two.updateRelationship(char_one, -100)  # Irreparable damage

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

    def simulateDuel(self, character1, character2, print_event):
        # Use initial health and relationship values as seed for deterministic outcome
        seed = hash((character1.health, character2.health, character1.relationships[character2]))

        # Initialize random seed for deterministic randomness
        random.seed(seed)

        # Define the characters' weapons and their respective strengths
        weapon1 = "sword"
        weapon2 = "dagger"
        strength1 = 70  # Adjust weapon strength as needed
        strength2 = 50  # Adjust weapon strength as needed

        # Determine the order of attack based on characters' speed (randomly in this example)
        if random.random() < 0.5:
            attacker = character1
            defender = character2
        else:
            attacker = character2
            defender = character1

        # Simulate the duel with specific details

        if print_event:
            print(
                "{} wields a {}, while {} defends with a {}.".format(
                    attacker.name, weapon1, defender.name, weapon2
                )
            )

        # Determine the outcome of the duel
        if attacker == character1:
            # Character 1 attacks first
            if print_event:
                print(
                    "{} strikes first with a powerful swing of their {}. They catch {} off guard.".format(
                        attacker.name, weapon1, defender.name
                    )
                )
            if strength1 > strength2:
                if print_event:
                    print(
                        "{}'s attack overwhelms {}. They manage to disarm {} and land a critical blow.".format(
                            attacker.name, defender.name, defender.name
                        )
                    )
                return character1, character2
            else:
                if print_event:
                    print(
                        "{}'s attack is strong, but {} manages to parry and counter, landing a hit on {}.".format(
                            attacker.name, defender.name, attacker.name
                        )
                    )
                return character2, character1
        else:
            # Character 2 attacks first
            if print_event:
                print(
                    "{} lunges forward with their {}. {} narrowly avoids the attack.".format(
                        attacker.name, weapon2, defender.name
                    )
                )
            if strength2 > strength1:
                if print_event:
                    print(
                        "{} manages to regain control and swiftly strikes back, disarming {} and injuring them.".format(
                            attacker.name, defender.name
                        )
                    )
                return character2, character1
            else:
                if print_event:
                    print(
                        "{} retaliates with a swift move, but {}'s defense holds. They engage in a fierce exchange of blows.".format(
                            attacker.name, defender.name
                        )
                    )
                return character1, character2

class BreakingPoint(PlotFragment):
    def __init__(self):
        self.drama = 10  # Higher drama score for an intense event

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        # Define the threshold for a significant negative relationship
        significant_negative_threshold = -50  # Adjust as needed

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                            character.relationships[character2] <= significant_negative_threshold
                            and character.relationships[character2] >= -100
                        ):
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
            print(
                "{} and {} finally reach their breaking point. Their relationship has deteriorated to the point of no return.".format(
                    characters[0].name, characters[1].name
                )
            )
            print(
                "{} accuses {} of betrayal, and {} fires back with anger in their eyes.".format(
                    characters[0].name, characters[1].name, characters[1].name
                )
            )
            print(
                "Their voices rise in a heated argument, each word more hurtful than the last. The tension in the air is unbearable."
            )
            print(
                "{} and {} decide that it's best to part ways, and they no longer wish to be in each other's presence.".format(
                    characters[0].name, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        # Set relationship values to the lowest point, representing irreparable damage
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, -100)  # Irreparable damage
        char_two.updateRelationship(char_one, -100)  # Irreparable damage

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class IrritateMild(PlotFragment):
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
                        if character.relationships[character2] >= -10:  # Ensure the relationship isn't too strained
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
            print("{} irritates {} with their constant complaining and negativity. The atmosphere becomes tense.".format(characters[0].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, -5)  # Mild irritation
        char_two.updateRelationship(char_one, -5)  # Mild irritation
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class IrritateIncreasing(PlotFragment):
    def __init__(self):
        self.drama = 9

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if character.relationships[character2] >= -15:  # Ensure the relationship isn't too strained
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
            print("Tensions rise as {} and {} clash over their differing opinions. Their irritation with each other grows.".format(characters[0].name, characters[1].name))
            print("{} criticizes {}'s choices, and {} responds with frustration.".format(characters[0].name, characters[1].name, characters[1].name))
            print("{} and {} find it increasingly difficult to get along.".format(characters[0].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, -10)  # Increasing irritation
        char_two.updateRelationship(char_one, -10)  # Increasing irritation
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class IrritateStrong(PlotFragment):
    def __init__(self):
        self.drama = 12

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if character.relationships[character2] >= -20:  # Ensure the relationship isn't too strained
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
            print("The situation between {} and {} escalates as they exchange harsh words and glares. Their dislike for each other is palpable.".format(characters[0].name, characters[1].name))
            print("Their argument intensifies, and they both decide it's best to keep their distance for now.".format(characters[0].name, characters[1].name))
            print("It's clear that {} and {} have developed a strong dislike for each other.".format(characters[0].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, -15)  # Strong dislike
        char_two.updateRelationship(char_one, -15)  # Strong dislike
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class BefriendSlight(PlotFragment):
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
                        character.updateRelationship(character2, 0)  # if no relationship, add to the relationship table
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
            print("{} approaches {} and strikes up a casual conversation. They enjoy each other's company, chatting about various topics.".format(characters[0].name, characters[1].name))
            print("They discuss hobbies, with {} mentioning their interest in {} and {} talking about their recent experiences with {}.".format(characters[0].name, "photography", characters[1].name, "gardening"))
            print("Both {} and {} find common ground in their love for nature.".format(characters[0].name, characters[1].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 15)  # Slight friendliness
        char_two.updateRelationship(char_one, 15)  # Slight friendliness
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class BefriendModerate(PlotFragment):
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
                        character.updateRelationship(character2, 0)  # if no relationship, add to the relationship table
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
            print("{} approaches {} and strikes up a friendly conversation. They quickly hit it off, sharing stories and interests.".format(characters[0].name, characters[1].name))
            print("{} mentions their love for {} and {} excitedly talks about their recent experiences in {}.".format(characters[0].name, "cooking", characters[1].name, "traveling"))
            print("{} compliments {} on their sense of humor, and {} appreciates {}'s warm personality.".format(characters[0].name, characters[1].name, characters[1].name, characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 20)  # Moderate friendliness
        char_two.updateRelationship(char_one, 20)  # Moderate friendliness
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class BefriendStrong(PlotFragment):
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
                        character.updateRelationship(character2, 0)  # if no relationship, add to the relationship table
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
            print("{} warmly approaches {} and strikes up a heartfelt conversation. They quickly become best friends, sharing stories and laughter.".format(characters[0].name, characters[1].name))
            print("{} shares a childhood memory, and {} responds with a funny anecdote from their own past. They find common interests in hobbies and discover that they both love {}.".format(characters[0].name, characters[1].name, "baking"))
            print("{} praises {}'s sense of humor, and {} admires {}'s kindness.".format(characters[0].name, characters[1].name, characters[1].name, characters[0].name))
            self.appendAnimationCommand(worldstate, characters, environment)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 25)  # Increased friendliness
        char_two.updateRelationship(char_one, 25)  # Increased friendliness
        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class MildIgnorantAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 3  # Mild annoyance, lower drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -10  # Adjust as needed

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] <= annoyance_threshold
                                and character.relationships[character2] >= -100
                        ):
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

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "constant tapping of a pen"  # Adjust as needed
        char_one.updateRelationship(char_two, -5)  # Mild worsening of relationship due to annoyance

        if print_event:
            print(
                "{} finds {}'s {} mildly annoying, but {} remains completely unaware of their impact.".format(
                    characters[0].name, characters[1].name, annoyance_source, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class ModerateIgnorantAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 7  # Moderate annoyance, medium drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -15  # Adjust as needed

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] <= annoyance_threshold
                                and character.relationships[character2] >= -100
                        ):
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

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "constant loud music"  # Adjust as needed
        char_one.updateRelationship(char_two, -12)  # Moderate worsening of relationship due to annoyance

        if print_event:
            print(
                "{} finds {}'s {} increasingly annoying, and tension simmers, but {} remains completely unaware of their impact.".format(
                    characters[0].name, characters[1].name, annoyance_source, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class SevereIgnorantAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 10  # Severe annoyance, higher drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -20  # Adjust as needed

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments
        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] <= annoyance_threshold
                                and character.relationships[character2] >= -100
                        ):
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

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "incessant complaining"  # Adjust as needed
        char_one.updateRelationship(char_two, -18)  # Severe worsening of relationship due to annoyance

        if print_event:
            print(
                "{} finds {}'s {} unbearably annoying, and their patience wears thin, but {} remains completely unaware of their impact.".format(
                    characters[0].name, characters[1].name, annoyance_source, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class MildIntentionalAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 3  # Mild annoyance, lower drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -10  # Threshold for mild annoyance

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments

        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] >= annoyance_threshold
                                and character.relationships[character2] <= 0
                        ):
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "constant jokes and playful teasing"  # Adjust as needed
        char_one.updateRelationship(char_two, -5)  # Mild worsening of relationship due to teasing

        if print_event:
            print(
                "{} intentionally annoys {} with {} to get a reaction, but {} tries to take it in stride.".format(
                    characters[0].name, characters[1].name, annoyance_source, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class ModerateIntentionalAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 7  # Moderate annoyance, medium drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -15  # Threshold for moderate annoyance

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments

        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] >= annoyance_threshold
                                and character.relationships[character2] <= 0
                        ):
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "persistent mocking and sarcastic remarks"  # Adjust as needed
        char_one.updateRelationship(char_two, -12)  # Moderate worsening of relationship due to teasing

        if print_event:
            print(
                "{} intentionally annoys {} with {} to provoke a reaction, and {} struggles to maintain composure.".format(
                    characters[0].name, characters[1].name, annoyance_source, characters[1].name
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)

class SevereIntentionalAnnoyance(PlotFragment):
    def __init__(self):
        self.drama = 10  # Severe annoyance, higher drama score

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        annoyance_threshold = -20  # Threshold for severe annoyance

        if not self.withinRepeatLimit(worldstate, 3):
            return False, None, environments

        for character in worldstate.characters:
            for character2 in worldstate.characters:
                if character != character2:
                    if character.sameLoc(character2):
                        if (
                                character.relationships[character2] >= annoyance_threshold
                                and character.relationships[character2] <= 0
                        ):
                            valid_characters.append([character, character2])
                            environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1

        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]

        annoyance_source = "merciless taunting and personal attacks"  # Adjust as needed
        char_one.updateRelationship(char_two, -18)  # Severe worsening of relationship due to teasing

        if print_event:
            print(
                "{} intentionally annoys {} with {} to provoke a reaction, and the tension escalates to the breaking point.".format(
                    characters[0].name, characters[1].name, annoyance_source
                )
            )
            self.appendAnimationCommand(worldstate, characters, environment)

        reachable_worldstate.drama_score += self.drama
        reachable_worldstate.prior_worldstate = worldstate
        return self.updateEventHistory(reachable_worldstate, characters, environment)






