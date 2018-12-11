"____________________________________imports__________________________________"
import pyglet
from math import cos, sin, radians, degrees, atan2

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

    def __init__(self, img_file, x, y):
        self.img = load_image(img_file)
        self.img.anchor_x = self.img.width // 2
        self.img.anchor_y = self.img.height // 2

        super().__init__(self.img, batch = batch)
        
        self.rotation = 0
        self.x = x
        self.y = y
    
    def get_hit(self):
        for a in objects:
            distance = (((a.x - self.x)**2) + ((a.y - self.y)**2))**(.5)
            
            if self. cooldown > self.shoot_cooldown-10:
                self.invincible = True
            else:
                self.invincible = False

            if distance < self.height and not self.invincible and type(a) in self.hittable:
                self.x, self.y = 10000, 10000


class MoveObject(SpaceObject):
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        
        self.vector = 0 + 0j
        
    def damper(self):
        self.vector *= self.drag
        
    def burn(self):
        angle = radians(self.rotation + 90)
        new_vector = self.vector + complex(self.thrust*cos(angle), self.thrust*sin(angle))
        
        if abs(new_vector) < self.max_spd:
            self.vector = new_vector
            
    def bounce(self):
        if self.x > window.width or self.x < 0:
            self.vector = complex(-self.vector.real, self.vector.imag) 
        
        if self.y > window.height or self.y < 0:
            self.vector = complex(self.vector.real, -self.vector.imag)           
            
        if self.x > window.width + 15 and is_in_area(self.x, self.y):
            self.x = window.width - 15
            
        if self.x < -15 and is_in_area(self.x, self.y):
            self.x = 15
        
        if self.y > window.height + 15 and is_in_area(self.x, self.y):
            self.y = window.height - 15
    
        if self.y < -15 and is_in_area(self.x, self.y):
            self.y = 15
        
    def move(self, dt):
        self.x -= dt * self.vector.real
        self.y += dt * self.vector.imag




class PlayerShip(MoveObject):
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.thrust = 25
        self.max_spd = 750
        self.drag = 0.985
        self.rspeed = 7
        self.shoot_cooldown = 30
        self.cooldown = 0
        self.hittable = [Projectile]    #Add missile
    
    def shoot(self):
        if not self.cooldown:
            objects.append(Projectile("sprites/projectile.png", self.x, self.y, self.vector, self.rotation))
            self.cooldown = self.shoot_cooldown                
        
    def tick(self, dt):
        if self.cooldown:
            self.cooldown -=1
        
        self.get_hit()
        self.move(dt)
        self.damper()
        self.bounce()

class Projectile(MoveObject):
    def __init__(self, img_file, x, y, vector, rotation):
        super().__init__(img_file, x, y)
        self.vector = vector
        self.rotation = rotation
        self.thrust = 500
        self.max_spd = 1500
        self.hittable = None
        
    def tick(self, dt):
        self.burn()
        self.move(dt)

class Missile(MoveObject):    
    def __init__(self, img_file, x, y, target):
        super().__init__(img_file, x, y)
        self.target = target
        self.thrust = 50
        self.max_spd = 1000
        self.drag = 0.98
        self.hittable = [Projectile, PlayerShip]
        
    def aim(self):
        x = self.target.x - self.x
        y = self.target.y - self.y
        self.rotation = atan2(y, -x)
        
    def tick(self, dt):
        self.burn()
        self.damper()
        self.move(dt)
        self.get_hit()
        self.aim()

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
p1 = PlayerShip("sprites/p1.png", window.width/3, window.height/3)
p2 = PlayerShip("sprites/p2.png", 2*window.width/3, 2*window.height/3)

pyglet.clock.schedule_interval(tick, 1/120)

pyglet.app.run()