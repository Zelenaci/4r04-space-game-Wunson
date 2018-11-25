import pyglet
from math import sin, cos, radians, pi

batch = pyglet.graphics.Batch()
window = pyglet.window.Window()

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
        self.sprite.rotation = self.direction
        
    def move(self, dt):
        self.x += dt * self.speed * cos(pi/2 - radians(self.direction))
        self.y += dt * self.speed * sin(pi/2 - radians(self.direction))
        
        
class Ship(SpaceObject):
    
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.direction = 0
        self.speed = 0
        self.thrust = 5         #zrychlení
        self.rspeed = 5         #rychlost otáčení
        
        
        
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
                self.speed += self.thrust
            elif key == 115:
                self.speed -= self.thrust
            elif key == 97:
                self.direction -= self.rspeed
            elif key == 100:
                self.direction += self.rspeed
        pass
        


##############################################################################        
pes = Ship("test.png", 100, 100)
keys = []

print(str(pes))

def tick(dt):
    pes.control(keys)
    pes.move(dt)
    pes.refresh()

@window.event
def on_draw():
    window.clear()
    batch.draw()
    

@window.event
def on_key_press(symbol, modifiers):
    keys.append(symbol)
    
    
@window.event
def on_key_release(symbol, modifier):
    keys.remove(symbol)
    
pyglet.clock.schedule_interval(tick, 1/30)

pyglet.app.run()