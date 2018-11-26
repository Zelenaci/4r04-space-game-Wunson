"____________________________________imports__________________________________"
import pyglet
from math import cos, sin, pi, radians, degrees, atan2

"________________________________pyglet_setup_________________________________"
window = pyglet.window.Window(1300, 700)
batch = pyglet.graphics.Batch()
keys = []

"____________________________________classes__________________________________"
class SpaceObject(object):

    def __init__(self, img_file, x, y, mass):
        self.rotation = pi / 2
        self.vector = 0 + 0j
        self.x = x
        self.y = y
        self.mass = mass
        
        self.sprite = self.load_image(img_file)
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.hitbox = range(int(self.x - self.sprite.width // 2), int(self.x + self.sprite.width // 2))
        self.hitboy = range(int(self.y - self.sprite.height // 2), int(self.y + self.sprite.height // 2))

    def load_image(self, path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch = batch)
    
    def refresh(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = degrees(self.rotation - (pi /2))
    
    def bounce(self):
        if self.x > window.width or self.x < 0:
            self.vector = complex(-self.vector.real, self.vector.imag) 
        
        if self.y > window.height or self.y < 0:
            self.vector = complex(self.vector.real, -self.vector.imag)
            
        if self.x > window.width+15 or self.x < -15:
            self.x = window.width -15  
        
        if self.y > window.height+15 or self.y < -15:
            self.y = window.height - 15
        
    def move(self, dt):
        self.vector *= 0.98
        self.x -= dt * self.vector.real
        self.y += dt * self.vector.imag
        
    def get_coordinates(self):
        return [self.x, self.y]
        
class Meteor(SpaceObject):
    def __init__(self, img_file, x, y, mass):
        super().__init__(img_file, x, y, mass)
    
    def get_hit(self):
        if abs(self.x - player.x) < self.sprite.width and abs(self.y - player.y) < self.sprite.height:
            mass = self.mass + player.mass
            
            force = abs(self.vector + player.vector) / mass
            
            temp = player.vector * force * self.mass 
            
            player.vector = self.vector * force * player.mass
            
            self.vector = temp
    
    def tick(self, dt):
        self.get_hit()
        self.move(dt)
        self.bounce()
        self.refresh()


class PlayerShip(SpaceObject):
    
    def __init__(self, img_file, x, y, mass):
        
        super().__init__(img_file, x, y, mass)
        
        self.thrust = 25
        self.rspeed = radians(9)
        
    def __str__(self):
        return str(self.x) + str(self.y)
    
    def control(self, keys):
        
        """W = 119
           S = 115
           A = 97
           D = 100
           spc = 32"""
           
        for key in keys:
            if key == 119: #W
                new_vector = self.vector + complex(self.thrust*cos(self.rotation), self.thrust*sin(self.rotation)) 
                
                if abs(new_vector) < 750:
                    self.vector = new_vector
            
            elif key == 115:
                pass
            elif key == 97:
                self.rotation -= self.rspeed
            elif key == 100:
                self.rotation += self.rspeed
                
    def tick(self, dt):
        self.control(keys)
        self.move(dt)
        self.bounce()
        self.refresh()
        
class Missile(SpaceObject):
    def __init__(self, img_file, x, y, mass):
        super().__init__(img_file, x, y, mass)
        
    def aim(self, coordinates):
        x = coordinates[0] - self.x
        y = coordinates[1] - self.y
        self.rotation = atan2(y, -x)
        print(degrees(self.rotation))
        
    def tick(self, dt):
        self.move(dt)
        self.aim(player.get_coordinates())
        self.refresh()
    
"_________________________________events______________________________________"
@window.event
def on_draw():
    window.clear()
    batch.draw()
    
@window.event
def on_key_press(key, mod):
    keys.append(key)    

@window.event
def on_key_release(key, mod):
    keys.remove(key)

def tick(dt):
    player.tick(dt)
    missile.tick(dt)

"_______________________________________main__________________________________"    
        
player = PlayerShip("test_mini.png", window.width/2, window.height/2, 10)
#meteor = Meteor("test.png", 100, 100, 10)
missile = Missile("missile.png", 600, 300, 10)

pyglet.clock.schedule_interval(tick, 1/60)

pyglet.app.run()