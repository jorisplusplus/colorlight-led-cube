import math
import random
from time import sleep

FRAMERATE = 30
FRAMETIME = 1/FRAMERATE

launchvalues = [-5.6*((i*FRAMETIME)**2)+28*(i*FRAMETIME)-35 for i in range(0, int(FRAMERATE*2.5))]
print(launchvalues)

palette = [0x5F0F40, 0x9A031E, 0xFB8B24, 0xE36414, 0x0F4C5C]

class Fireworks():
    def __init__(self, screen, numfireworks=3) -> None:
        self.screen = screen
        self.fireworks = list()
        for i in range(0, numfireworks):
            self.fireworks.append(Firework(random.randint(5, screen.width-5)))
        
    def start(self):
        while True:
            self.screen.clear()
            for i in range(0, len(self.fireworks)):
                self.fireworks[i].render(self.screen)
                if self.fireworks[i].done:
                    self.fireworks[i] = Firework(random.randint(5, self.screen.width-5)) 
            self.screen.update()
            sleep(1/30)

class Firework():
    def __init__(self, x, num_particles=15):
        self.height = int(random.random()*30+5)
        self.particles = list()
        self.exploded = False
        self.iteration = 1
        #Prime launch
        while self.height - launchvalues[self.iteration] > 40:
            self.iteration += 1
        for i in range(0, num_particles):
             self.particles.append((x, self.height, random.random()*0.7, random.random()*2*math.pi))
        self.color = palette[random.randint(0, 4)]
        self.x = x
        self.done = False
        print(f"Firework created explode @ {self.x},{self.height}")

    def render(self, screen):
        if self.exploded and self.iteration < 20:
            brightness = (int(100*(20-self.iteration)/20))
            #print(brightness)
            for startx, starty, velo, dir in self.particles:
                x = int(startx+math.cos(dir)*velo*self.iteration)
                y = int(starty+math.sin(dir)*velo*self.iteration)
                screen.pixel(x, y, self.color)
        elif self.exploded == False:
            y = int(self.height - launchvalues[self.iteration])
            screen.pixel(self.x, y, 0xFFFFFF)
            if self.iteration == (len(launchvalues)-1):
                self.iteration = 0
                self.exploded = True
        else:
            self.done = True            
        self.iteration += 1
        