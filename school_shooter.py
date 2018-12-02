"""
@author: jakubvasi, Wunson 
"""

"____________________________________imports__________________________________"
import pyglet
from math import cos, sin, pi, radians, degrees, atan2

"________________________________pyglet_setup_________________________________"

key = pyglet.window.key
window = pyglet.window.Window(1300, 700)
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
batch = pyglet.graphics.Batch()

objects = []

"____________________________________functions__________________________________"
def overlap(hitbox1, hitbox2):
    return max(0, min(hitbox1[1], hitbox2[1]) - max(hitbox1[0], hitbox2[0]))

def load_image(path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch = batch)
    
#Check if object is inside the area
def is_in_area(x, y, x1=0, x2=window.width, y1=0, y2=window.height):
    return x > x1 and x < x2 and y > y1 and y < y2

"____________________________________classes__________________________________"
class SpaceObject(object):

    def __init__(self, img_file, x, y, mass, max_spd):
        self.rotation = pi / 2
        self.vector = 0 + 0j
        self.x = x
        self.y = y
        self.mass = mass
        self.max_spd = max_spd
        self.drag = 0.989
        
        self.sprite = load_image(img_file)
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.hitbox = (int(self.x - self.sprite.width // 2), int(self.x + self.sprite.width // 2))
        self.hitboy = (int(self.y - self.sprite.height // 2), int(self.y + self.sprite.height // 2))
    
    def refresh(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = degrees(self.rotation - (pi /2))
    
    def burn(self, thrust, dir="y"):
        if dir == "y":
            new_vector = self.vector + complex(thrust*cos(self.rotation), thrust*sin(self.rotation))
        elif dir == "x":
            new_vector = self.vector + complex(thrust*sin(self.rotation), thrust*cos(self.rotation))
        
        if abs(new_vector) < self.max_spd:
            self.vector = new_vector
    
    def bounce(self):
        if self.x > window.width or self.x < 0:
            self.vector = complex(-self.vector.real, self.vector.imag) 
        
        if self.y > window.height or self.y < 0:
            self.vector = complex(self.vector.real, -self.vector.imag)
        
    def damper(self, drag):
        self.vector *= drag
    
    def move(self, dt):
        self.x -= dt * self.vector.real
        self.y += dt * self.vector.imag
        self.damper(self.drag)
        
class Meteor(SpaceObject):
    def __init__(self, img_file, x, y, mass, max_spd):
        super().__init__(img_file, x, y, mass, max_spd)
    
    def get_hit(self):
        pass
    
    def tick(self, dt):
        self.get_hit()
        self.move(dt)
        self.bounce()
        self.refresh()

class PlayerShip(SpaceObject):
    def __init__(self, img_file, x, y, mass, max_spd):
        super().__init__(img_file, x, y, mass, max_spd)
        
        self.rspeed = radians(9)
        
    def __str__(self):
        return str(self.x) + str(self.y)
    
    def down():
        self.burn(-10)
    def up():
        self.burn(25)
    def left():
        self.rotation -= self.rspeed
    def right():
        self.rotation += self.rspeed
    def brake():
        self.damper(0.85)
    def fire():
        objects.append(Shot("laserBlue.png", self.x, self.y, 0, 2000, self.vector, self.rotation))
    
    
    def control(self):
        print(keyboard)
        
        if keyboard[key.DOWN]:              #S, Down
            self.burn(-10)
        if keyboard[key.UP]:              #W, Up
            self.burn(25)
        if keyboard[key.LEFT]:              #A, Left
            self.rotation -= self.rspeed
        if keyboard[key.RIGHT]:           #D, Right
            self.rotation += self.rspeed
        if keyboard[key.B]:                 #B
            self.damper(0.85)
        if keyboard[key.SPACE]:             #Space
            objects.append(Shot("laserBlue.png", self.x, self.y, 0, 2000, self.vector, self.rotation))
           
    def tick(self, dt):
        self.control()
        self.move(dt)
        self.bounce()
        self.refresh()
    
        
class Shot(SpaceObject):
    def __init__(self, img_file, x, y, mass, max_spd, vector, rotation):
        super().__init__(img_file, x, y, mass, max_spd)
        self.vector = vector
        self.rotation = rotation
        
    def tick(self, dt):
        self.burn(100)
        self.move(dt)
        self.refresh()    
        

class Missile(SpaceObject):    
    def __init__(self, img_file, x, y, mass, max_spd):
        super().__init__(img_file, x, y, mass, max_spd)
        
    def aim(self):
        x = player.x - self.x
        y = player.y - self.y
        self.rotation = atan2(y, -x)
        
    def tick(self, dt):
        self.burn(35)
        self.move(dt)
        self.aim()
        self.refresh()
    
"_________________________________events______________________________________"
@window.event
def on_draw():
    window.clear()
    batch.draw()


def tick(dt):
    player.tick(dt)
    missile.tick(dt)
    
    for shot in objects:
        if is_in_area(shot.x, shot.y):
            shot.tick(dt)
        else:
            objects.remove(shot)

"_______________________________________main__________________________________"
     
player = PlayerShip("test_mini.png", window.width/2, window.height/2, 10, 750)
missile = Missile("missile.png", -1000, -1000, 10, 750)
pyglet.clock.schedule_interval(tick, 1/60)

pyglet.app.run()