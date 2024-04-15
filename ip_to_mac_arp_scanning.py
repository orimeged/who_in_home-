
from datetime import datetime
import time
import platform

import scapy.all
from scapy.all import ARP, Ether, srp
import pygame

#WINDOW_WIDTH = 1024
#WINDOW_HEIGHT = 768
target_ip = "192.168.1.1/24"
pygame.init()
#size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode()
pygame.display.set_caption("Who in home:")
pygame.font.init()
myfont = pygame.font.SysFont('comicsansms', 26)
IMAGE = r'/home/pi/Desktop/ori101.jpg'
IMAGE2= r'/home/pi/Desktop/23.jpg'
img = pygame.image.load(IMAGE)
img3 = pygame.image.load(IMAGE2)
finish = False
mac_to_details = {
            '2c:d0:66:4c:0c:93': dict(name='ori', position=(100, 295), counter=0, last_sin='ERROR'),
            '60:ab:67:b9:9a:2f': dict(name='Alona', position=(100, 135), counter=0,last_sin='ERROR'),
            'a8:db:03:89:a3:10': dict(name='Oded', position=(100, 89), counter=0,last_sin='ERROR'),
            '1c:cc:d6:4c:d6:0c': dict(name='Adir', position=(100, 256), counter=0,last_sin='ERROR'),
            '60:ab:67:c2:46:c0': dict(name='Daniel', position=(100, 170), counter=0, last_sin='ERROR')
                 }
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    screen.blit(img, (0, 0))
    screen.blit(img3, (0, 0))
    for client in clients:
        if client['mac'] in mac_to_details.keys():
            mac_to_details[client['mac']]['counter'] = 8
            now = datetime.now()
            date = now.strftime("%H:%M:%S")
            mac_to_details[client['mac']]['last_sin']=date
            textsurface = myfont.render(mac_to_details[client['mac']]['last_sin'], False, (0, 0, 0))
            screen.blit(textsurface, mac_to_details[client['mac']]['position'])
    for key in mac_to_details:
        textsurface = myfont.render(mac_to_details[key]['last_sin'], False, (0, 0, 0))
        screen.blit(textsurface, mac_to_details[key]['position'])
            
    pygame.display.flip()
    time.sleep(13)
