# implementation of card game - Memory

import simplegui
import random

# cards
deck = [ str(dummy_x) for dummy_x in range(8) for dummy_id in range (2)  ] 
# expose
exposed = [ False for dummy_x in range(16)  ] 
# clicked cards, last 2 cards
clicked = []
# turn
turn = 0

# helper function to initialize globals
def new_game():
    global state, exposed, turn
    state = 0
    turn = 0
    exposed = [ False for dummy_x in range(16)  ] 
    random.shuffle(deck)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, clicked, turn
    num = pos[0]//50 # the positon idx of card
    if state == 0:
        state = 1
        exposed[num] = True
        clicked.append(num)
        
    elif state == 1:
        if exposed[num] == False:
            state = 2
            exposed[num] = True
            clicked.append(num)
            if deck[clicked[0]]  == deck[num]:   # check cards
                clicked = []
 
    else:
        if exposed[num] == False:
            state = 1
            turn += 1
            exposed[num] = True
            if len(clicked) == 2:
                exposed[clicked[0]] = False
                exposed[clicked[1]] = False
                clicked = []
            clicked.append(num)
    label.set_text("Turns = "+str(turn))
            

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for idx in range(16):
        canvas.draw_text(deck[idx], (12.5+idx*50, 62.5), 50, 'white')
        if exposed[idx] == False:
            canvas.draw_polygon([[0+idx*50, 0], [0+idx*50, 100], [50+idx*50, 100], [50+idx*50, 0]], 1, 'Red', 'green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric