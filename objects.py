#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:14:23 2018

@author: svo35103
"""
import pyglet
from math import sin, cos, radians, pi
fps = 144
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(1200, 800)

'''
class Window(object):

    def __init__(self, width, height):
        pass
'''


class SpaceObject(object):

    def __init__(self, img_file, x, y):
        self.x = x # globalni souradnice
        self.y = y  # -//-

        self.winx = 0 # v okne
        self.winy = 0 # -//-
        self.sprite = self.load_image(img_file)
        # self.hitbox = range((self.x - self.sprite.width // 2), (self.x + self.sprite.width // 2))
        # self.hitboy = range((self.y - self.sprite.height // 2), (self.y + self.sprite.height // 2))

    def load_image(self, path):
        load = pyglet.image.load(path)
        load.anchor_x = load.width // 2
        load.anchor_y = load.height // 2
        return pyglet.sprite.Sprite(load, batch=batch)
    
    def refresh(self):
        self.sprite.x = self.winx
        self.sprite.y = self.winy
        self.sprite.rotation = self.direction
        
    def move(self, dt):
        self.x += dt * self.speed * cos(pi/2 - radians(self.direction))
        self.y += dt * self.speed * sin(pi/2 - radians(self.direction))

    def render(self):
        self.winx = self.x - (player.x - window.width / 2)
        self.winy = self.y - (player.y - window.height / 2)

        
class Ship(SpaceObject):
    
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.direction = 0
        self.speed = 0
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
            elif key == 100:
                self.direction += self.rspeed

    def tick(self, dt):
        self.control()
        self.move(dt)
        self.render()
        self.refresh()


class Meteor(SpaceObject):

    def __init__(self, img_file, x, y, speed=0, rspeed=0):
        super().__init__(img_file, x, y)
        self.direction = 0
        self.speed = speed
        self.rspeed = rspeed
        pyglet.clock.schedule_interval(self.tick, 1 / fps)

    def tick(self, dt):
        self.move(dt)
        self.render()
        self.refresh()

@window.event
def on_key_press(symbol, modifiers):
    player.keys.append(symbol)


@window.event
def on_key_release(symbol, modifier):
    player.keys.remove(symbol)


'''           TEST             '''


player = Ship("test.png", 100, 100)
meteority = [Meteor('/home/roman/git/4r04-space-game-Wunson/PNG/Meteors/meteorBrown_big1.png', 200, 100, 3, 3), Meteor('/home/roman/git/4r04-space-game-Wunson/PNG/Meteors/meteorBrown_big1.png', 300, 300, 3, 3)]
keys = []


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
