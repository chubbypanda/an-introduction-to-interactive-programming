# Mini-project 3 for An Introduction to Interactive Programming in Python class, by k., 10/09/2014
# "Stopwatch: The Game"
#https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/30/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# template available at http://www.codeskulptor.org/#examples-stopwatch_template.py


import simplegui

# abudance of global variables (forced onto), don't do this in real life!

# global variables
BEAT = 0
SUCCESS_STOP = 0
FAIL_STOP = 0

# helper function format 
def format(t):
    '''
    converts time in tenths of seconds into formatted string A:BC.D
    
    examples:
    format(0) = 0:00.0
    format(11) = 0:01.1
    format(321) = 0:32.1
    format(613) = 1:01.3
    '''
    tenth_second = t % 10
    t //= 10
    second = t % 60
    t //= 60
    minute = t
    # Codeskultor supports only obsolote formatting method
    #return '{}:{:02d}.{}'.format(minute, second, tenths_second)
    return '%d:%02d.%d' % (minute, second, tenth_second)

# event handler for timer with 0.1 sec interval
def start():
    global BEAT
    timer.start()
    BEAT += 1

def stop():
    global SUCCESS_STOP, FAIL_STOP
    timer.stop()
    # the "Stop" button correctly updates these success/attempts numbers
    if BEAT % 10 == 0:
        SUCCESS_STOP += 1
    FAIL_STOP += 1
        
def reset():
    '''
    "Reset" button that stops the timer (if running) and resets the timer to 0
    '''
    timer.stop()
    global BEAT
    global SUCCESS_STOP, FAIL_STOP
    BEAT = 0
    # the "Reset" button clears the success/attempts numbers
    SUCCESS_STOP, FAIL_STOP = 0, 0
    
# handler to draw on canvas
def draw(canvas):
    canvas.draw_text(format(BEAT), [50, 90], 36, 'white')
    # draws the number of successful stops at a whole second versus the total number of stops
    canvas.draw_text(str(SUCCESS_STOP) + '/' + str(FAIL_STOP), [150, 20], 18, 'green')

# create a frame 
frame = simplegui.create_frame('"Stopwatch: The Game"', 200, 150)

# register event handlers
frame.add_button('Start', start, 70)
frame.add_button('Stop', stop, 70)
frame.add_button('Reset', reset, 70)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, start)

# start the frame animation
frame.start()
