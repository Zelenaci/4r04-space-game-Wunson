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
def is_in_area(x, y, x1=-50, x2=window.width+50, y1=-50, y2=window.height+50):
    return x > x1 and x < x2 and y > y1 and y < y2

"____________________________________classes__________________________________"
class SpaceObject(object):

    def __init__(self, img_file, x, y, max_spd):
        self.rotation = pi / 2
        self.vector = 0 + 0j
        self.x = x
        self.y = y
        self.max_spd = max_spd
        
        self.sprite = load_image(img_file)
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.hitbox = range(int(self.x - self.sprite.width // 2), int(self.x + self.sprite.width // 2))
        self.hitboy = range(int(self.y - self.sprite.height // 2), int(self.y + self.sprite.height // 2))
    
    def refresh(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = degrees(self.rotation - (pi /2))
        self.hitbox = range(int(self.x - self.sprite.width // 2), int(self.x + self.sprite.width // 2))
        self.hitboy = range(int(self.y - self.sprite.height // 2), int(self.y + self.sprite.height // 2))
    
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
        new_vector = self.vector + complex(self.thrust*cos(self.rotation), self.thrust*sin(self.rotation))
        
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
        self.rspeed = radians(7)
        self.shoot_cooldown = 60
        self.cooldown = 0
        
    def __str__(self):
        return str(self.x) + str(self.y)
        
    
    def damper(self):
        self.vector *= self.drag
    
    def shoot(self):
        if not self.cooldown:
            objects.append(Projectile("sprites/projectile.png", self.x, self.y, 1500, self.vector, self.rotation))
            self.cooldown = self.shoot_cooldown
    
    def get_hit(self):    #not work
        for a in objects:
            distance = (((a.x - self.x)**2) + ((a.y - self.y)**2))**(.5)
            
            if self. cooldown > self.shoot_cooldown-10:
                self.invincible = True
            else:
                self.invincible = False
                

            if distance < self.sprite.width and not self.invincible:
                print(type(a))
                self.x, self.y = 10000, 10000
                
        
    def tick(self, dt):
        if self.cooldown:
            self.cooldown -=1
        
        self.get_hit()
        self.move(dt)
        self.damper()
        self.bounce()
        self.refresh()
        
class Projectile(SpaceObject):
    def __init__(self, img_file, x, y, max_spd, vector, rotation):
        super().__init__(img_file, x, y, max_spd)
        self.vector = vector
        self.rotation = rotation
        self.thrust = 500
        
    def tick(self, dt):
        self.burn()
        self.move(dt)
        self.refresh()    
        

class Missile(SpaceObject):    
    def __init__(self, img_file, x, y, max_spd):
        super().__init__(img_file, x, y, max_spd)
        
    def aim(self):
        x = player.x - self.x
        y = player.y - self.y
        self.rotation = atan2(y, -x)
        
    def tick(self, dt):
        self.burn()
        self.move(dt)
        self.aim()
        self.refresh()
    
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
    
    #P2
    
    if keyboard[key.UP]:
        p2.burn()
    
    if keyboard[key.DOWN]:
        p2.drag = 0.95
    else:
        p2.drag = 0.985
    
    if keyboard[key.LEFT]:
        p2.rotation -= p2.rspeed
    
    if keyboard[key.RIGHT]:
        p2.rotation += p2.rspeed
    
    if keyboard[key.M]:
        p2.shoot()
"_________________________________events______________________________________"
@window.event
def on_draw():
    window.clear()
    batch.draw()


def tick(dt):
    controler()
    p1.tick(dt)
    p2.tick(dt)
    for a in objects:
        if is_in_area(a.x, a.y):
            a.tick(dt)
        else:
            objects.remove(a)

"_______________________________________main__________________________________"
p1 = PlayerShip("sprites/p1.png", window.width/3, window.height/3, 750)
p2 = PlayerShip("sprites/p2.png", 2*window.width/3, 2*window.height/3, 750)
#missile = Missile("missile.png", -1000, -1000, 750)

pyglet.clock.schedule_interval(tick, 1/120)

pyglet.app.run()