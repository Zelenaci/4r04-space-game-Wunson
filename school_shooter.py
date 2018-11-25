"____________________________________imports__________________________________"
import pyglet
from math import cos, sin, pi, radians, degrees

"________________________________pyglet_setup_________________________________"
window = pyglet.window.Window(1300, 700)
batch = pyglet.graphics.Batch()
keys = []

"____________________________________classes__________________________________"
class SpaceObject(object):

    def __init__(self, img_file, x, y):
        self.x = x
        self.y = y
        self.sprite = self.load_image(img_file)

    def load_image(self, path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch = batch)
    
    def refresh(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = degrees(self.rotation - (pi /2))
        
    def move(self, dt):
        self.x += dt * self.vector.real
        self.y += dt * self.vector.imag
        
        
class Ship(SpaceObject):
    
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.rotation = pi / 2
        self.thrust = 1
        self.rspeed = radians(5)
        self.vector = 0 + 0j
        
        
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
                
                if abs(new_vector) < 20:
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
    pes.tick(dt)

"_______________________________________main__________________________________"    
        
pes = Ship("test.png", window.width/2, window.height/2)
pyglet.clock.schedule_interval(tick, 1/30)

pyglet.app.run()