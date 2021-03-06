# Mini-project 7 for An Introduction to Interactive Programming in Python class, by k., 11/018/2014
# Spaceship
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/34/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# template available at http://www.codeskulptor.org/#examples-spaceship_template.py

import math
import random
import simplegui

# global variables for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = 0.03
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png')

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png')

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png')

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png')

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png')

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png')

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png')

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3')
missile_sound = simplegui.load_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3')
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3')
explosion_sound = simplegui.load_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3')

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        # forward vector when the ship is thrusting
        self.forward = angle_to_vector(self.angle)
        
    def get_angle_vel(self):
        '''helper method to obtain current angle velocity'''
        return self.angle_vel
        
    def set_angle_vel(self, angle_velocity):
        '''helper method to adjust angle velocity'''
        self.angle_vel = angle_velocity
        
    def set_thrust(self, enabled):
        '''helper method to manipulate ship thrusters'''
        self.thrust = False
        if enabled:
            self.thrust = True
                   
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.forward = angle_to_vector(self.angle)
        if self.thrust:
            # apply an offset 90 (as in self.image_center[0] + self.image_size[0])
            self.image_center[0] = 45 + 90
            self.vel[0] += self.forward[0] * (FRICTION * 10)
            self.vel[1] += self.forward[1] * (FRICTION * 10)
        else:
            self.image_center[0] = 45
        
        # update the position of the ship based on its velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # ship's position wraps around the screen when it goes off the edge
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # increment its angle by its angular velocity
        self.angle += self.angle_vel
        
        # each component of the velocity by a number slightly less than 1 during each update
        self.vel[0] *= 1 - FRICTION
        self.vel[1] *= 1 - FRICTION
        
    def shoot(self):
        '''spawn a new missile'''
        global a_missile
        # velocity is the sum of the ship's velocity and a multiple (x5) of the ship's forward vector
        a_missile = Sprite([self.pos[0] + self.forward[0] * self.radius, 
                            self.pos[1] + self.forward[1] * self.radius],
                           [self.vel[0] + self.forward[0] * 5, 
                            self.vel[1] + self.forward[1] * 5],
                           0, 0, missile_image, missile_info, missile_sound)
    
     
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # update the position of the rock based on its velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # rock's position wraps around the screen when it goes off the edge
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # increment its angle by its angular velocity
        self.angle += self.angle_vel

           
def draw(canvas):
    global time
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw two messages, shows the number of lives remaining and the score
    canvas.draw_text('Score: ' + str(score), (10, 20), 20, 'white')
    canvas.draw_text('Lives: ' + str(lives), (WIDTH - 75, 20), 20, 'white')
                
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], 
                    [-0.5 + random.random(), -0.5 + random.random()], 
                    2 * math.pi * random.random(), (-0.5 + random.random()) / 5, 
                    asteroid_image, asteroid_info)

# keydown handler
def keydown(key):
    velocity = 0.1
    current_velocity = my_ship.get_angle_vel()
    if key == simplegui.KEY_MAP['left']:
        current_velocity += velocity
        my_ship.set_angle_vel(current_velocity)
    elif key == simplegui.KEY_MAP['right']:
        current_velocity -= velocity
        my_ship.set_angle_vel(current_velocity)
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
        ship_thrust_sound.play()
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

# keyup handler
def keyup(key):                               
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(0)
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        ship_thrust_sound.rewind()
    
# initialize frame
frame = simplegui.create_frame('Asteroids', WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
# once every second in the timer handle
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
