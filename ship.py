#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 18:49:06 2018

@author: AMS, FMC
"""
import math, random

class ship :
    def __init__(self, type, xo, yo, vel, pygame):
        self.shipImage = pygame.image.load('assets/images/ships/ship'+ str(type)+'.png')
        self.x = xo
        self.y = yo
        self.vel = vel
        
        
    def draw(self, surface):
        rect = self.shipImage.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(self.shipImage,rect)
        
    def move(self,direction):
        if direction=='up' :
            self.y -= self.vel
        elif direction == 'down' :
            self.y += self.vel
        elif direction == 'left':
            self.x -= self.vel
        elif direction == 'right':
            self.x += self.vel
    
    def getPos(self):
        return (self.x, self.y)
        
class doubleShip :
    def __init__(self, type1, xo1, yo1, type2, xo2, yo2, vel, pygame):
        self.ship1=ship(type1, xo1, yo1, vel, pygame)
        self.ship2=ship(type2, xo2, yo2, vel, pygame)
        self.colorLine = (255, 255, 255)
        self.frec = 1/5
        self.amp = 5
    
    def draw(self, surface):
        x1 = int(self.ship1.getPos()[0])
        y1 = int(self.ship1.getPos()[1])
        x2 = int(self.ship2.getPos()[0])
        y2 = int(self.ship2.getPos()[1])
        
        if abs(x1-x2) > abs(y1-y2) :
            for i in range(x1,x2):
                #surface.set_at((int(i+self.amp*math.sin(i*self.frec)),int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.sin(i*self.frec))),self.colorLine)
                #surface.set_at((int(i+self.amp*math.cos(i*self.frec)),int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.cos(i*self.frec))),(255,0,0))
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.sin(i*self.frec))),self.colorLine)
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.cos(i*self.frec))),(255,0,0))
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1))),(255,255,0))
        else :
            for i in range(y1,y2):
                #surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.sin(i*self.frec)),int(i+self.amp*math.sin(i*self.frec))),self.colorLine)
                #surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.cos(i*self.frec)),int(i+self.amp*math.cos(i*self.frec))),(255,0,0))
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.sin(i*self.frec)),i),self.colorLine)
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.cos(i*self.frec)),i),(255,0,0))
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1)),i),(255,255,0))
        self.ship1.draw(surface)
        self.ship2.draw(surface)
        
    def move(self, direction1, direction2):
        self.ship1.move(direction1)
        self.ship2.move(direction2)
        
    
                
    