#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:04:47 2018

@author: AMS, FMC
"""
import math 

class enemy:
    
    def __init__(self, type, xo, yo, vx, vy, angularSpeed, pygame):
        self.type = type
        self.x = xo
        self.y = yo
        self.vx = vx
        self.vy = vy
        self.angularSpeed = angularSpeed
        self.radius = 25
        
        if self.type=='alien':
            self.withRotation = pygame.image.load("assets/images/enemies/alien.png")
            self.cockpit = pygame.image.load("assets/images/enemies/cockpit.png")
        else:
            self.withRotation = pygame.image.load("assets/images/enemies/bomb.png")
        self.angle = 0
        self.pygame = pygame

    def hablar(self):
        print('hola soy un '+ self.type + ' que está en las coordenadas ' + str(self.x) + ' y ' + str(self.y))

    def draw(self, surface):
        imageToDraw = self.pygame.transform.rotate(self.withRotation,self.angle)
        rect = imageToDraw.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(imageToDraw,rect)    
        if self.type == 'alien':
            rect = self.cockpit.get_rect()
            rect.center = (self.x,self.y)
            surface.blit(self.cockpit,rect)
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.angularSpeed
        self.angle = self.angle % 360
    
    def out(self,WINDOW_WIDTH,WINDOW_HEIGHT): # If you create an enemy more than 100 px out of the screen it will desapear
        if self.x < -100 or self.x > WINDOW_WIDTH+100 or self.y < -100 or self.y > WINDOW_HEIGHT + 100:
            toReturn = True
        else:
            toReturn = False
        return toReturn

    def dead (self, pos1, pos2):
        if pos2[0]-pos1[0]:
            dist = abs(self.x-pos1[0])
        else:
            a = (pos2[1]-pos1[1])/(pos2[0]-pos1[0])
            b = pos1[1]-a*pos1[0]
            dist = abs(a*self.x-self.y+b)/math.sqrt(a**2+1)
#        if pos2[0]>pos1[0]:
#            upx = pos2[0]
#            downx = pos1[0]
#        else:
#            upx = pos1[0]
#            downx = pos2[0]
        
        print("Mi distancia a la línea: "+ str(dist))
        
