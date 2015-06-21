# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

secret_number = 0
set_range = 100
remain_count = 0

# helper function to start and restart the game
def new_game():
    """
        initializes a global variable secret_number to be
        a random number in the appropriate range,
        reset the game
        """
    # initialize global variables used in your code here
    global secret_number
    global set_range
    global remain_count
    secret_number = random.randrange(0, set_range)
    remain_count = int(math.ceil(math.log(set_range+1, 2)))
    print "New game. Range is from 0 to "+str(set_range)
    print "the number of remaining guesses", remain_count
    print

# define event handlers for control panel
def range100():
    """
        choose ranges [0, 100) for the secret number.
        """
    # button that changes the range to [0,100) and starts a new game
    global set_range
    set_range = 100
    new_game()

def range1000():
    """
        choose ranges [0, 1000) for the secret number.
        """
    # button that changes the range to [0,1000) and starts a new game
    global set_range
    set_range = 1000
    new_game()

def input_guess(guess):
    """
        event handler that takes the input string
        covert to int and print
        """
    # main game logic goes here
    global secret_number
    global remain_count
    print "Guess was " + guess
    print "the number of remaining guesses", remain_count-1
    try:
        guess = int(guess)
        if guess > secret_number:
            print "Lower\n"
        elif guess < secret_number:
            print "Higher\n"
        else:
            print "Correct\n"
            new_game()
    except:
        print "Please input a integer!\n"
    remain_count -= 1
    if remain_count <= 0:
        print "the end of the game...\n"
        new_game()

# create frame
frame = simplegui.create_frame("Guess the number", 300, 200)

# register event handlers for control elements and start frame
frame.add_button('Range: 0 - 100', range100)
frame.add_button('Range: 0 - 1000', range1000)
frame.add_input('Guess a number', input_guess, 200)


# call new_game
new_game()


# always remember to check your completed program against the grading rubric
