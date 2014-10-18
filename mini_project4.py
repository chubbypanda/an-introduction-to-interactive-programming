# Mini-project 4 for An Introduction to Interactive Programming in Python class, by k., 10/18/2014
# "Pong"
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/31/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# template available at http://www.codeskulptor.org/#examples-pong_template.py


import random
import simplegui

# abudance of global variables (forced onto), don't do this in real life!

# initialize global constants (pos and vel encode vertical info for paddles)
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
RIGHT = True
LEFT = not RIGHT


# initialize ball_position and ball_velocity for new ball in middle of canvas
def spawn_ball(direction):
    global ball_position, ball_velocity # these are vectors stored as lists
    # spawns a ball in the middle of the table...
    ball_position = [WIDTH / 2, HEIGHT / 2]
    # ...and assigns the ball random velocity (pixels per update (1/60 seconds))...
    ball_velocity = [0, 0]
    ball_velocity[0] = random.randrange(120, 240) / 60
    ball_velocity[1] = random.randrange(60, 180) / 60
    # ...and a direction based on LEFT boolean, velocity upwards and towards the right
    if not direction:
        ball_velocity[0] = - ball_velocity[0]
        ball_velocity[1] = - ball_velocity[1]
    # velocity of the ball should be upwards and towards the left
    else:
        ball_velocity[1] = - ball_velocity[1]
        
        
# define event handlers
def new_game():
    global paddle1_position, paddle2_position, paddle1_velocity, paddle2_velocity  # these are numbers
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    paddle1_velocity, paddle2_velocity = 0, 0
    paddle1_position = HEIGHT / 2
    paddle2_position = HEIGHT / 2

    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_position, paddle2_position, ball_position, ball_velocity
    # draw a mid line... 
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, 'white')
    # ... and left&right gutters
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, 'white')
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, 'white')
        
    # update ball
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]
    
    # collide and reflect off of the upper side of canvas
    if ball_position[1] <= BALL_RADIUS:
        ball_velocity[1] = - ball_velocity[1]
    # collide and reflect off of the lower side of canvas
    if ball_position[1] >= HEIGHT - BALL_RADIUS:
        ball_velocity[1] = - ball_velocity[1]
        
    # ball hit the left side
    if ball_position[0] <= PAD_WIDTH + BALL_RADIUS:
        # check whether the ball is actually striking a paddle when it touches a gutter
        if (paddle1_position - HALF_PAD_HEIGHT <= ball_position[1] <= paddle1_position + HALF_PAD_HEIGHT):
            ball_velocity[0] = - ball_velocity[0]
            # increase the difficulty of your game, increase the velocity of the ball by 10% each time
            ball_velocity[0] *= 1.1
            ball_velocity[1] *= 1.1
        # collide with the left gutter, the opposite player receives a point, start new game in opposite direction
        else:
            score2 += 1
            spawn_ball(RIGHT)
     
    # ball hit the right side
    if ball_position[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
        # check whether the ball is actually striking a paddle when it touches a gutter
        if (paddle2_position - HALF_PAD_HEIGHT <= ball_position[1] <= paddle2_position + HALF_PAD_HEIGHT):
            ball_velocity[0] = - ball_velocity[0]
            # increase the difficulty of your game, increase the velocity of the ball by 10% each time
            ball_velocity[0] *= 1.1
            ball_velocity[1] *= 1.1
        # collide with the right gutter, the opposite player receives a point, start new game in opposite direction
        else:
            score1 += 1
            spawn_ball(LEFT)
            
    # draw ball
    canvas.draw_circle(ball_position, BALL_RADIUS, 2, 'red', 'white')
    
    # update paddle's vertical position, keep paddle on the screen
    global paddle1_velocity, paddle2_velocity
    # both paddles restricted to stay entirely on the canvas when moving up/down
    if HEIGHT - HALF_PAD_HEIGHT >= paddle1_position + paddle1_velocity >= HALF_PAD_HEIGHT:
        paddle1_position += paddle1_velocity
    if HEIGHT - HALF_PAD_HEIGHT >= paddle2_position + paddle2_velocity >= HALF_PAD_HEIGHT:
        paddle2_position += paddle2_velocity
      
    # draw left&right paddles
    canvas.draw_line((0, paddle1_position + HALF_PAD_HEIGHT), (0, paddle1_position - HALF_PAD_HEIGHT), PAD_WIDTH * 2, 'red')
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_position + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_position - HALF_PAD_HEIGHT), PAD_WIDTH, 'blue')
        
    # draw scores for both players
    canvas.draw_text(str(score1), [100, 50], 40, 'red')
    canvas.draw_text(str(score2), [500, 50], 40, 'blue')

def keydown(key):
    global paddle1_velocity, paddle2_velocity
    # for both players, paddle moves up at a constant velocity if the key is pressed
    vel = 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_velocity -= vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_velocity += vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_velocity -= vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_velocity += vel
   
def keyup(key):
    global paddle1_velocity, paddle2_velocity
    # for both players, paddle is motionless if neither key is pressed
    if key == simplegui.KEY_MAP['w']:
        paddle1_velocity = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_velocity = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_velocity = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_velocity = 0
    

# create frame
frame = simplegui.create_frame('Pong', WIDTH, HEIGHT)
# "Restart" button that calls new_game to reset the score and relaunch the ball.
frame.add_button('Restart', new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
