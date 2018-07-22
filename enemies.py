#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:04:47 2018

@author: AMS, FMC
"""

class enemy:
    
    def __init__(self, type, xo, yo, vx, vy, pygame):
        self.type = type
        self.x = xo
        self.y = yo
        self.vx = vx
        self.vy = vy
        if self.type=='alien':
            self.withRotation = pygame.image.load("assets/images/enemies/alien.png")
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
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += 2
        self.angle = self.angle % 360
    
    def out(self,WINDOW_WIDTH,WINDOW_HEIGHT):
        if self.x < -100 or self.x > WINDOW_WIDTH+100 or self.y < -100 or self.y > WINDOW_HEIGHT + 100:
            toReturn = True
        else:
            toReturn = False
        return toReturn

        
