# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

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
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_set, canvas):
    """
    This function should take a set and a canvas 
    and call the update and draw methods for each sprite in the group.
    """
    for sprite_id in rock_group:
        sprite_id.draw(canvas)
        sprite_id.update()
        
    for sprite_id in set(missile_group):
        sprite_id.draw(canvas)
        if sprite_id.update():
            missile_group.remove(sprite_id)
        else:
            sprite_id.update()
            
    for sprite_id in set(explosion_group):
        if sprite_id.draw(canvas):
            explosion_group.remove(sprite_id)
        
        
def group_collide(group, other_object):
    """
    This function should take a set group and a sprite other_object 
    and check for collisions between other_object and elements of the group.
    """
    global explosion_group
    for items in set(group):
        if items.collide(other_object):
            group.remove(items)
            a_explosion = Sprite(items.get_position(), [0, 0], 
                           0, 0, explosion_image, explosion_info)
            explosion_sound.play()
            explosion_group.append(a_explosion)
            return True
    return False

def group_group_collide(group, other_group):
    """
    return the number of elements in the first group that collide with the second group 
    as well as delete these elements in the first group. 
    """
    num_collide = 0
    for items in set(group):
        if group_collide(other_group, items):
            num_collide += 1
            group.remove(items)
    return num_collide
            


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        #position update
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH 
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT
        #friction update
        self.vel[0] *= 0.9
        self.vel[1] *= 0.9

        #trust update
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]
            self.image_center = [ship_info.get_center()[0] + ship_info.get_size()[0], 
                                 ship_info.get_center()[1]]   
            ship_thrust_sound.play()
        else:
            self.image_center = [ship_info.get_center()[0], ship_info.get_center()[1]]
            ship_thrust_sound.rewind()
    
    def shoot(self):
        global missile_group
        micelle_pos = angle_to_vector(self.angle)
        mvector = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0]+micelle_pos[0]*self.image_size[0]*0.4, self.pos[1]+micelle_pos[1]*self.image_size[0]*0.4], 
                           [self.vel[0]+mvector[0]*4, self.vel[1]+mvector[1]*4], 
                           0, 0, missile_image, missile_info, missile_sound)
        missile_group.append(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
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
        if self.animated:
            self.age += 1
            canvas.draw_image(self.image, [self.image_center[0]+self.age*self.image_size[0], self.image_center[1]], 
                              self.image_size, self.pos, self.image_size)  
            return self.age > self.lifespan
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        self.age += 1    
        self.angle += self.angle_vel
        #position update
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH 
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT 
        if self.age > 250:
            return True
        else:
            return False
        
        
    def collide(self, other_object):
        """
        take an other_object as an argument
        return True if there is a collision or False otherwise. 
        """
        if dist(self.pos, other_object.get_position()) > self.radius + other_object.get_radius():
            return False
        else:
            return True
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
        
def draw(canvas):
    global time, lives, score, started, my_ship, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    score += group_group_collide(rock_group, missile_group)
    my_ship.update()
    if started and group_collide(rock_group, my_ship):
        lives -= 1
    process_sprite_group(rock_group, canvas)
    
    if lives <= 0 : #the game is reset and the splash screen appears
        started = False
        lives = 3
        score = 0
        rock_group = []
        missile_group = []
        explosion_group = []
        
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
def keydown_handler(key):    
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= 0.05
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += 0.05
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship
    if started and len(rock_group) <= 12:
        a_rock = Sprite([random.random()*WIDTH, random.random()*HEIGHT], [random.random()*2.0-1.0, random.random()*2.0-1.0], 
                    0, random.random()*0.2, asteroid_image, asteroid_info)
        if not a_rock.collide(my_ship):
            rock_group.append(a_rock)
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
missile_group = []
rock_group = []
explosion_group = []
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_mouseclick_handler(click)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
soundtrack.play()

