# template for "Stopwatch: The Game"

# general import
import simplegui

# define global variables
time = 0
stop_counter = 0
stop_sucess_counter = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t/600
    milliseconds = "%03d" %(t%600)
    return "%s:%s%s:%s" %(minute, milliseconds[0],milliseconds[1],milliseconds[2])

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_stopwatch():
    timer.start()

def stop_stopwatch():
    global time, stop_counter, stop_sucess_counter
    if timer.is_running():
        stop_counter += 1
        if not time%10:
            stop_sucess_counter += 1
    timer.stop()

def reset_stopwatch():
    global time, stop_counter, stop_sucess_counter
    timer.stop()
    time = 0
    stop_counter = 0
    stop_sucess_counter = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    global time
    canvas.draw_text(format(time), (100, 120), 40, 'white')
    canvas.draw_text("%s/%s" %(stop_sucess_counter, stop_counter), (250, 40), 30, 'green')

# create frame
frame = simplegui.create_frame("Stopwatch", 300,200)
timer = simplegui.create_timer(100,timer_handler)

# register event handlers
frame.add_button("Start", start_stopwatch, 100)
frame.add_button("Stop", stop_stopwatch, 100)
frame.add_button("Reset", reset_stopwatch, 100)
frame.set_draw_handler(draw_handler)


# start frame
frame.start()

# Please remember to review the grading rubric
