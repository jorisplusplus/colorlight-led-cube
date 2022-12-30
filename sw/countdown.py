from sendpixel import LedScreen
from fontTools.ttLib import TTFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
from datetime import datetime
import random
import math
from firework import Fireworks


screen = LedScreen(3, 1, [[0, 1, 2]])
font_path = 'vcr.ttf'
fonts = ImageFont.truetype(font_path, 12)
font = ImageFont.truetype(font_path, 16)
fontL = ImageFont.truetype(font_path, 20)
fontXL = ImageFont.truetype(font_path, 32)

numfirework = 7
fireworks = Fireworks(screen, numfirework)

    
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

newyearcolors = [(0x5F, 0x0F, 0x40), (0x9A, 0x03, 0x1E), (0xFB, 0x8B, 0x24), (0xE3, 0x64, 0x14), (0x0F, 0x4C, 0x5C)]

targettime = datetime(2022, 12, 30, 11, 48, 30)
trigger = targettime.strftime("%H:%M:%S")
font = ImageFont.truetype(font_path, 16)

while True:
    dirty = False
    img = Image.new('RGB', (screen.width, screen.height), color = (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1"
    
    now = datetime.now()
    delta = targettime-now

    # print(now.strftime("%H:%M:%S.%f"))
    # print(delta.seconds+1)

    if now.strftime("%H:%M:%S") == trigger and flashprimed:
        flashprimed = False
        flash(screen, 0.4)
        break


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
        draw.text((24+48, 20), fullscr, font=fontXL, fill=(255, 255, 255), anchor="mm")
        draw.text((24+48+48, 20), fullscr, font=fontXL, fill=(255, 255, 255), anchor="mm")
    else:
        draw.text((24, 15), topstr, font=font, fill=(255, 0, 0), anchor="ms")
        draw.text((24, 35), botstr, font=fontL, fill=(255, 255, 255), anchor="ms")
        draw.text((2*48, 15), "Loading 2023", font=fonts, fill=(255, 0, 0), anchor="ms")
    
    if dirty:
        for i in range(0, screen.width):
            for j in range(0, screen.height):
                screen.pixel(i, j, img.getpixel((i, j)))
        screen.update()
    sleep(0.005)

for color in newyearcolors:

    img = Image.new('RGB', (screen.width, screen.height), color = (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1"

    draw.text((48+24, 15), "Happy new year", font=font, fill=color, anchor="ms")
    draw.text((48+24, 35), "Happy new year", font=font, fill=color, anchor="ms")

    for i in range(0, screen.width):
            for j in range(0, screen.height):
                screen.pixel(i, j, img.getpixel((i, j)))
    screen.update()
    sleep(0.5)

fireworks.start()