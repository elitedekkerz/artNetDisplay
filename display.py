#!/usr/bin/python3
import pygame
import socket
import time

#setup artnet client
artnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
artnet.bind(('0.0.0.0',6454))               
artnet.settimeout(1)
firstChannel=18 #first channel byte in artnet protocol
offset = firstChannel + 0

#setup pygame
pygame.init()
pygame.mouse.set_visible(False)

#create a fullscreen display
displayResolution = pygame.display.list_modes()[0]
screen = pygame.display.set_mode(
    displayResolution,
    pygame.RESIZABLE,
    )

#create surface to draw on
background = pygame.Surface(displayResolution)

#create logo
logo = pygame.transform.scale(
    pygame.image.load('./logo.png'),
    displayResolution)

color = [0,0,0] #default background color
run = True
while run:

    #get data from artnet
    try:
        data, addr = artnet.recvfrom(1024)
        prevcolor = color
        color = [int(data[offset]),int(data[offset+1]),int(data[offset+2])]
    except:
        continue

    #update background color if changed
    if color != prevcolor:
        print(color)
        background.fill(color)
        screen.blit(background,[0,0])
        screen.blit(logo,[0,0])

        #update display
        pygame.display.flip()

    #detect quit status
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quit state')
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                print('escape pressed')
                run = False
                break

#clanup
pygame.quit()
artnet.close()
