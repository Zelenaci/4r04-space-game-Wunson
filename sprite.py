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
        return pyglet.image.load(path)
    
#Check if object is inside the area
def is_in_area(x, y, x1=-50, x2=window.width+50, y1=-50, y2=window.height+50):
    return x > x1 and x < x2 and y > y1 and y < y2

"____________________________________classes__________________________________"
class SpaceObject(pyglet.sprite.Sprite):

    def __init__(self, img_file, x, y, max_spd):
        self.img = load_image(img_file)
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2
        
        super().__init__(self.img, batch = batch)
        
        self.rotation = 90
        self.vector = 0 + 0j
        
        self.x = x
        self.y = y
        self.max_spd = max_spd
    
    def bounce(self):
        if self.x > window.width or self.x < 0:
            self.vector = complex(-self.vector.real, self.vector.imag) 
        
        if self.y > window.height or self.y < 0:
            self.vector = complex(self.vector.real, -self.vector.imag)
            
            
        if self.x > window.width+15 and is_in_area(self.x, self.y):
            self.x = window.width - 15
            
        if self.x < -15 and is_in_area(self.x, self.y):
            self.x = 15
        
        if self.y > window.height+15 and is_in_area(self.x, self.y):
            self.y = window.height - 15
    
        if self.y < -15 and is_in_area(self.x, self.y):
            self.y = 15
    
    def burn(self):
        angle = radians(self.rotation + 90)
        new_vector = self.vector + complex(self.thrust*cos(angle), self.thrust*sin(angle))
        
        if abs(new_vector) < self.max_spd:
            self.vector = new_vector
    
    def move(self, dt):
        self.x -= dt * self.vector.real
        self.y += dt * self.vector.imag

class PlayerShip(SpaceObject):
    def __init__(self, img_file, x, y, max_spd):
        
        super().__init__(img_file, x, y, max_spd)
        self.thrust = 25
        self.drag = 0.985
        self.rspeed = 10
        self.shoot_cooldown = 30
        self.cooldown = 0
        
    def __str__(self):
        return str(self.x) + str(self.y)
        
    
    def damper(self):
        self.vector *= self.drag
        
    def tick(self, dt):
        print(self.rotation, degrees(self.rotation))
        
        self.move(dt)
        self.damper()
        self.bounce()
    
    
def controler():
    #P1
    if keyboard[key.W]:
        p1.burn()
    
    if keyboard[key.S]:
        p1.drag = 0.95
    else:
        p1.drag = 0.985
    
    if keyboard[key.A]:
        p1.rotation -= p1.rspeed
    
    if keyboard[key.D]:
        p1.rotation += p1.rspeed
    
    if keyboard[key.SPACE]:
        p1.shoot()
    
"_________________________________events______________________________________"
@window.event
def on_draw():
    window.clear()
    batch.draw()


def tick(dt):
    controler()
    p1.tick(dt)

"_______________________________________main__________________________________"
p1 = PlayerShip("sprites/p1.png", 2*window.width/3, window.height/3, 750)
#missile = Missile("missile.png", -1000, -1000, 750)

pyglet.clock.schedule_interval(tick, 1/120)

pyglet.app.run()
