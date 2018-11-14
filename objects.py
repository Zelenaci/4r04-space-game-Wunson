import pyglet
from math import sin, cos, radians, pi
from random import randint

fps = 60
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(1200, 800)

"""______________________________OBJECT_____________________________________"""
class SpaceObject(object):

    def __init__(self, img_file, x, y):
        self.x = x # globalni souradnice
        self.y = y  # -//-

        self.winx = 0 # v okne
        self.winy = 0 # -//-
        self.sprite = self.load_image(img_file)
        self.rotation = 0

        self.hitbox = range((self.x - self.sprite.width // 2), (self.x + self.sprite.width // 2))
        self.hitboy = range((self.y - self.sprite.height // 2), (self.y + self.sprite.height // 2))

    def load_image(self, path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch=batch)
    
    def refresh(self):
        self.winx = self.x - (player.x - window.width // 2)
        self.winy = self.y - (player.y - window.height // 2)
        self.sprite.x = self.winx
        self.sprite.y = self.winy
        self.sprite.rotation = self.rotation

    def move(self, dt):
        self.speed = self.maxspeed if self.speed > self.maxspeed else self.speed
        self.speed = 0 if self.speed < 0 else self.speed
        self.x += dt * self.speed * cos(pi/2 - radians(self.direction))
        self.y += dt * self.speed * sin(pi/2 - radians(self.direction))

"""_______________________________PLAYER____________________________________"""
class PlayerShip(SpaceObject):
    
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.direction = 0
        self.speed = 0
        self.maxspeed = 500
        self.thrust = 5         # zrychlení
        self.deceleration = 1   # zpomalení
        self.rspeed = 5         # rychlost otáčení
        self.keys = []
        pyglet.clock.schedule_interval(self.tick, 1 / fps)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)
    
    def control(self):
        
        """W = 119
           S = 115
           A = 97
           D = 100
           spc = 32"""
           
        for key in self.keys:
            if key == 119:
                self.speed += self.thrust
            elif key == 115:
                self.speed -= self.thrust
            elif key == 97:
                self.direction -= self.rspeed
                self.rotation -= self.rspeed
            elif key == 100:
                self.direction += self.rspeed
                self.rotation += self.rspeed

    def hit(self):
        for meteor in meteors:
            print(".", end = "")
            if (set(self.hitbox) and set(meteor.hitbox)) or (set(self.hitboy) and set(meteor.hitboy)):
                print("AAAAAAAAAAAAAAAAAAA")
    
    def drag(self):
        self.speed -= 50/fps
    
    def tick(self, dt):
        self.control()
        self.hit()
        self.move(dt)
        self.drag()
        self.refresh()

"""______________________________________ENEMY______________________________"""
class EnemyShip(SpaceObject):
    pass

"""__________________________________________METEOR_________________________"""
class Meteor(SpaceObject):

    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        pyglet.clock.schedule_interval(self.tick, 1 / fps)

    def tick(self, dt):
        self.refresh()

"""_______________________________EVENTS____________________________________"""
@window.event
def on_key_press(symbol, modifiers):
    player.keys.append(symbol)


@window.event
def on_key_release(symbol, modifier):
    player.keys.remove(symbol)

@window.event
def on_draw():
    window.clear()
    batch.draw()
  
"""_________________________________MAIN____________________________________"""
player = PlayerShip("test.png", 100, 100)
keys = []

meteors = []
for x in range(0, 100):
    x = randint(0, 1000)
    y = randint(0, 1000)
    meteor = Meteor('PNG/Meteors/meteorBrown_big1.png', x, y)
    
pyglet.app.run()