import pyglet as p
from random import randint
from math import sin, cos, radians, pi

window = p.window.Window(640, 480)
batch = p.graphics.Batch()

@window.event
def on_draw():
    window.clear()
    batch.draw()

def load_image(path):
    load = p.image.load(path)
    
    load.anchor_x = load.width // 2
    load.anchor_y = load.height // 2
    
    return p.sprite.Sprite(load, batch = batch)
    
class Meteor():
    def __init__(self, x = None,
                       y = None,
                       speed = None,
                       direction = None):
        
        self.x = x if x != None else randint(0, window.width)
        self.y = y if y != None else randint(0, window.height)
        self.direction = direction if direction != None else randint(0, 360)
        self.speed = speed if speed != None else randint(30, 150)
        
        path = str("meteors/" + str(randint(0,19)) + ".png")
        self.sprite = load_image(path)

        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.bounce_x = 1
        self.bounce_y = 1
        
    def move(self, dt):
        self.x += dt * self.speed * cos(pi/2 - radians(self.direction)) * self.bounce_x
        self.y += dt * self.speed * sin(pi/2 - radians(self.direction)) * self.bounce_y
        
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.bounce()
        
    def bounce(self):
        if self.x > window.width or self.x < 0 :
            self.bounce_x *= -1
            
        if self.y > window.height or self.y < 0 :
            self.bounce_y *= -1

def tick(dt):
    for rock in meteors:
        rock.move(dt)

meteors = []
for _ in range(30):
    rock = Meteor()

    meteors.append(rock)

p.clock.schedule_interval(tick, 1/30)
p.app.run()