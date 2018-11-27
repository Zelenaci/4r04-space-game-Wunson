"____________________________________imports__________________________________"
import pyglet
from math import cos, sin, pi, radians, degrees, atan2

"________________________________pyglet_setup_________________________________"
window = pyglet.window.Window(1300, 700)
batch = pyglet.graphics.Batch()
keys = []

"____________________________________functions__________________________________"
def overlap(hitbox1, hitbox2):
    return max(0, min(hitbox1[1], hitbox2[1]) - max(hitbox1[0], hitbox2[0]))

def load_image(path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch = batch)
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
    
    def burn(self, thrust):
        new_vector = self.vector + complex(thrust*cos(self.rotation), thrust*sin(self.rotation)) 
        if abs(new_vector) < self.max_spd:
            self.vector = new_vector
    
    def bounce(self):
        if self.x > window.width or self.x < 0:
            self.vector = complex(-self.vector.real, self.vector.imag) 
        
        if self.y > window.height or self.y < 0:
            self.vector = complex(self.vector.real, -self.vector.imag)
            
        if self.x > window.width+15:
            self.x = 1
        
        if self.x < -15:
            self.x = window.width - 1
        
        if self.y > window.height+15:
            self.y = 1
        
        if self.y < -15:
            self.y = window.height - 1
        
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
    
    def control(self, keys):
        
        """W = 119
           S = 115
           A = 97
           D = 100
           spc = 32"""
         
        for key in keys:
            if key == 115 or key == 65364:
                self.burn(-10)    
            elif key == 119 or key == 65362: #W
                self.burn(25)   
            elif key == 97 or key == 65361:
                self.rotation -= self.rspeed
            elif key == 100 or key == 65363:
                self.rotation += self.rspeed
            elif key == 32:
                self.damper(0.8)
                
    def tick(self, dt):
        self.control(keys)
        self.move(dt)
        self.bounce()
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
    
@window.event
def on_key_press(key, mod):
    print(key)
    keys.append(key)    

@window.event
def on_key_release(key, mod):
    keys.remove(key)

def tick(dt):
    player.tick(dt)
    missile.tick(dt)
    
    

"_______________________________________main__________________________________"    
        
player = PlayerShip("test_mini.png", window.width/2, window.height/2, 10, 750)
missile = Missile("missile.png", -1000, -1000, 10, 750)
pyglet.clock.schedule_interval(tick, 1/60)

pyglet.app.run()