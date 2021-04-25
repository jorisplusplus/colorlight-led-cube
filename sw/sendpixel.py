import socket

UDP_IP = "192.168.178.50"
UDP_PORT_1 = 26177
UDP_PORT_2 = 26178
UDP_PORT_3 = 26180
UDP_PORT_4 = 26184
UDP_PORT_5 = 26192

pixel = (127, 0, 0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(0, 128*3):

    data = (pixel[0] >> 2) | (pixel[1] >> 2) << 6 | (pixel[2] >> 2) << 12 | i << 18

    payload = data.to_bytes(4, byteorder="big")

    print(payload)


    
    sock.sendto(payload, (UDP_IP, UDP_PORT_1))
    sock.sendto(payload, (UDP_IP, UDP_PORT_2))
    sock.sendto(payload, (UDP_IP, UDP_PORT_3))
    sock.sendto(payload, (UDP_IP, UDP_PORT_4))
    sock.sendto(payload, (UDP_IP, UDP_PORT_5))