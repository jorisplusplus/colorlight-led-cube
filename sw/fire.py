from sendpixel import LedPanel, LedScreen
from pythonic_doom_fire.doom_fire import DoomFire
import time

class DoomFirePanel(DoomFire):
    def render(self, panel):
        for i in range(self.height):
            for j in range(self.width):
                pixel_index = i * self.width + j
                color_intensity = self.pixels_array[pixel_index]
                color = self.color_palette.get_color(color_intensity)
                panel.pixel(j, i, (color[1], color[2], color[0]))

output = LedScreen(3, 1, [[0, 1, 2]])

doom_fire = DoomFirePanel(48*3, 40, 1, 3, 7, (4, 6))

while True:
    time.sleep(1/30-0.006)
    start = time.time()
    doom_fire.update()
    doom_fire.render(output)
    fire = time.time()
    output.update()
    print(F"fire render: {fire-start}, send {time.time()-fire}, total {time.time()-start}")