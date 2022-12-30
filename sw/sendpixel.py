import socket
import time

class LedScreen():
    def __init__(self, width, height, map):
        self.PANELWIDTH = 48
        self.PANELHEIGHT = 40
        self.screenwidth = self.PANELWIDTH*width
        self.width = self.screenwidth
        self.screenheight = self.PANELHEIGHT*height
        self.height = self.screenheight
        
        if len(map) != height:
            raise ValueError("Invalid map")
        for row in map:
            if len(row) != width:
                raise ValueError("Invalid map")
        
        self.panelmap = list()
        for row in map:
            panelrow = list()
            for panelid in row:
                if panelid >= 0:
                    panelrow.append(LedPanel(panel=panelid))
                else:
                    panelrow.append(None)
            self.panelmap.append(panelrow)
        print(self.panelmap)

    def pixel(self, x, y, color):
        panelx = x // self.PANELWIDTH
        panely = y // self.PANELHEIGHT
        internalx = x % self.PANELWIDTH
        internaly = y % self.PANELHEIGHT
        #print(f"{x}, {y} : {panelx}, {panely} : {internalx}, {internaly}")

        if panelx < 0:
            return
        if panely < 0:
            return
        if x < 0 or x >= self.screenwidth:
            return
        if y < 0 or y >= self.screenheight:
            return

        if self.panelmap[panely][panelx] != None:
            self.panelmap[panely][panelx].pixel(internalx, internaly, color)
    
    def update(self):
        for row in self.panelmap:
            for panel in row:
                if panel != None:
                    panel.update()
    
    def clear(self):
        for row in self.panelmap:
            for panel in row:
                if panel != None:
                    for i in range(0, self.PANELWIDTH):
                        for j in range(0, self.PANELHEIGHT):
                            panel.pixel(i, j , 0)
    



class LedPanel():
    def __init__(self, ip="192.168.178.50", panel=0):

        self.ip = ip

        self.width = 48
        self.height = 40

        self.numleds = self.width*self.height
        port_offset = panel << 8
        self.UDP_PORT = [1+port_offset, 2+port_offset, 4+port_offset, 8+port_offset, 16+port_offset]
        print(self.UDP_PORT)
        self.framebuffer = list()

        
        for y in range(0, self.height):
            self.framebuffer.append(list())
            for x in range(0, self.width):
                self.framebuffer[y].append((0,0,0))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def memory_address(self, x, y):
        start_address = [1, 9, 17, 25, 2, 10, 18, 26]
        
        alias_y = y % 8
        
        cord_x = int(x / 4)
        pos_x = x % 4

        address = start_address[alias_y]+cord_x*32+pos_x*2
        
        return address
    
    def pixel_data(self, color):

        return (color[0] >> 2) | ((color[1] >> 2) << 6) | ((color[2] >> 2) << 12)

    def command(self, x, y):

        color = self.pixel_data(self.framebuffer[y][x])
        addr = self.memory_address(x, y)
        data = color | addr << 18
        return data.to_bytes(4, byteorder="big")

    def update(self):
        for y in range(0, 5):
            y_offset = y * 8
            
            payload = b''
            for ylocal in range(0, 4):
                for x in range(0, self.width):
                    payload += self.command(x, ylocal+y_offset)
            self.sock.sendto(payload, (self.ip, self.UDP_PORT[y]))
            #time.sleep(0.1)
            payload = b''
            for ylocal in range(4, 8):
                for x in range(0, self.width):
                    payload += self.command(x, ylocal+y_offset)
            self.sock.sendto(payload, (self.ip, self.UDP_PORT[y]))
            #time.sleep(0.1)

    def pixel(self, x, y, color):
        if type(color) is int:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = (color >> 0) & 0xFF
            self.framebuffer[y][x] = (g, b, r)
        elif type(color) is tuple:
            self.framebuffer[y][x] = color

    def fill(self, color=0):
        if type(color) is int:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = (color >> 0) & 0xFF
            for y in range(0, self.height):
                for x in range(0, self.width):
                    self.framebuffer[y][x] = (g, b, r)
        elif type(color) is tuple:
            for y in range(0, self.height):
                for x in range(0, self.width):
                    self.framebuffer[y][x] = color

if __name__ == "__main__":
    panel0 = LedPanel(panel=0)
    # for i in range(0, panel0.width):
    #     for j in range(0, panel0.height):
    #         panel0.pixel(i, j, 0xFFFFFF)
    # panel0.update()

    panel1 = LedPanel(panel=1)
    panel2 = LedPanel(panel=2)
    iter = 0
    trip = 0
    options = [0xFF0000, 0x00FF00, 0x0000FF]
    while True:
        for i in range(0, 48):
            panel0.pixel(i, iter, 0x000000)
            panel1.pixel(i, iter, 0x000000)
            panel2.pixel(i, iter, 0x000000)
        iter += 1
        if iter == 40:
            iter = 0
            trip += 1
        for i in range(0, 48):
            panel0.pixel(i, iter, options[trip % 3])
            panel1.pixel(i, iter, options[(trip+1) % 3])
            panel2.pixel(i, iter, options[(trip+2) % 3])
        panel0.update()
        panel1.update()
        panel2.update()
        time.sleep(0.05)