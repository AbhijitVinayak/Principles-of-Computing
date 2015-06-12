"""
    Rock-paper-scissors-lizard-Spock game.
    """
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    """
        A helper function convert name to number.
        """
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print "Error Message: Incorrect name!"
        print "Input is", name
        print "A correct name should be: 'rock', 'Spock', 'paper', 'lizard', or 'scissors'. "


def number_to_name(number):
    """
        A helper function convert number back to name.
        """
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print "Error Message: Incorrect number!"
        print "Input is", number
        print "A correct number should be in [0,4]. "


def rpsls(player_choice):
    """
        take input "rock", "paper", "scissors", "lizard", or "Spock",
        simulates playing a round of Rock-paper-scissors-lizard-Spock
        by generating its own random choice.
        """
    # print a blank line to separate consecutive games
    print
    # print out the message for the player's choice
    print "Player chooses", player_choice
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print "Computer chooses", comp_choice
    # compute difference of comp_number and player_number modulo five
    results = (player_number - comp_number)%5
    # use if/elif/else to determine winner, print winner message
    if results > 2:
        print "Computer wins!"
    elif results == 0:
        print "Player and Computer tie!"
    else:
        print "Player wins!"

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


