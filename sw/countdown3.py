from sendpixel import LedScreen
from fontTools.ttLib import TTFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
from datetime import datetime
import random
import math
from firework import Firework


screen = LedScreen(3, 1, [[0, 1, 2]])
font_path = 'vcr.ttf'
font = ImageFont.truetype(font_path, 16)
fontL = ImageFont.truetype(font_path, 20)
fontXL = ImageFont.truetype(font_path, 32)

numfirework = 7
fireworks = list()
for i in range(0, numfirework):
    fireworks.append(Firework(random.randint(5, screen.width-5)))
while True:
    screen.clear()
    for i in range(0, len(fireworks)):
        fireworks[i].render(screen)
        if fireworks[i].done:
            fireworks[i] = Firework(random.randint(5, screen.width-5)) 
    screen.update()
    sleep(1/30)
    

while True:
    points = list()
    for i in range(0, 15):
        points.append((24, 20, random.random()*0.7, random.random()*2*math.pi))
    
    for i in range (1, 20):
        screen.clear()
        brightness = (int(100*(20-i)/20))
        print(brightness)
        for startx, starty, velo, dir in points:
            x = int(startx+math.cos(dir)*velo*i)
            y = int(starty+math.sin(dir)*velo*i)
            screen.pixel(x, y, (0, brightness, 0))
        screen.update()
        sleep(1/30)
    screen.clear()
    screen.update()
    sleep(1)


flashprimed = False
if datetime.now().strftime("%Y") == "2022":
    print("Flash primed")
    flashprimed = True

def flash(screen, duration=0.4):
    for i in range(0, screen.width):
            for j in range(0, screen.height):
                screen.pixel(i, j, 0xFFFFFF)
    screen.update()
    sleep(duration)
    for i in range(0, screen.width):
            for j in range(0, screen.height):
                screen.pixel(i, j, 0)
    screen.update()

topstr = ""
botstr = ""
fullscr = ""


trigger = "00:24:00"
targettime = datetime(2022, 12, 30, 00, 24, 00)

font = ImageFont.truetype(font_path, 16)

while True:
    dirty = False
    img = Image.new('RGB', (48, 40), color = (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1"
    
    now = datetime.now()
    delta = targettime-now

    # print(now.strftime("%H:%M:%S.%f"))
    # print(delta.seconds+1)

    if now.strftime("%H:%M:%S") == trigger and flashprimed:
        flashprimed = False
        flash(screen, 0.4)


    if topstr != now.strftime("%H:%M"):
        topstr = now.strftime("%H:%M")
        dirty = True
    
    if botstr != now.strftime("%S"):
        botstr = now.strftime("%S")
        dirty = True
    
    if fullscr != str(delta.seconds+1):
        fullscr = str(delta.seconds+1)
        dirty = True
    
    if (delta.seconds+1) <= 10:
        draw.text((24, 20), fullscr, font=fontXL, fill=(255, 255, 255), anchor="mm")
    else:
        draw.text((24, 15), topstr, font=font, fill=(255, 0, 0), anchor="ms")
        draw.text((24, 35), botstr, font=fontL, fill=(255, 255, 255), anchor="ms")
    
    if dirty:
        for i in range(0, 48):
            for j in range(0, 40):
                screen.pixel(i, j, img.getpixel((i, j)))
        screen.update()
    sleep(0.005)