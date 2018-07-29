#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 18:49:06 2018

@author: AMS, FMC
"""
import math

class ship :
    def __init__(self, type, xo, yo, pygame):
        self.shipImage = pygame.image.load('assets/images/ships/ship'+ str(type)+'.png')
        self.x = xo
        self.y = yo
        self.vx = 0
        self.vy = 0
        self.a = 1
        self.limvel = 30
        
    def getPos(self):
        return (self.x, self.y)        
        
    def draw(self, surface):
        rect = self.shipImage.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(self.shipImage,rect)
        
    def vel(self,direction):
        if direction=='up' and self.vy > -self.limvel:
            self.vy -= self.a  
        elif direction == 'down' and self.vy < self.limvel:
            self.vy += self.a
        elif direction == 'left'and self.vx > -self.limvel:
            self.vx -= self.a
        elif direction == 'right'and self.vx < self.limvel:
            self.vx += self.a
    
    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        #if (self.x - 25) >= 0 and (self.x + 25) <= WINDOW_WIDTH and (self.y + 25) <= WINDOW_HEIGHT and (self.y - 25) <= 0:
        self.x += self.vx
        self.y += self.vy
            
        if self.x - 25 <= 0:
            self.x = 0 + 25
            self.vx = 0
        if self.x + 25 >= WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - 25
            self.vx = 0
        if self.y + 25 >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - 25
            self.vy = 0
        if self.y - 25 <= 0:
            self.y = 0 + 25
            self.vy = 0
        
        if self.vx > 0:
            self.vx -= self.a/2
        elif self.vx <0:
            self.vx += self.a/2
        if self.vy > 0 :
            self.vy -= self.a/2
        elif self.vy > 0:
            self.vy += self.a/2
        
        
    def getPos(self):
        return (self.x, self.y)
        
class doubleShip :
    def __init__(self, type1, xo1, yo1, type2, xo2, yo2, pygame):
        self.ship1=ship(type1, xo1, yo1, pygame)
        self.ship2=ship(type2, xo2, yo2, pygame)
        self.colorLine = (255, 255, 255)
        self.frec = 1/5
        self.amp = 5
    
    def draw(self, surface):
        x1 = int(self.ship1.getPos()[0])
        y1 = int(self.ship1.getPos()[1])
        x2 = int(self.ship2.getPos()[0])
        y2 = int(self.ship2.getPos()[1])
        
        if abs(x1-x2) > abs(y1-y2) :
            if x1 > x2:
                up = x1
                down = x2
            else:
                up = x2
                down = x1
            for i in range(down,up):
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.sin(i*self.frec))),self.colorLine)
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1) + self.amp*math.cos(i*self.frec))),(255,0,0))
                surface.set_at((i,int(y1+((y2-y1)/(x2-x1))*(i-x1))),(255,255,0))
        else :
            if y1 > y2:
                up = y1
                down = y2
            else:
                up = y2
                down = y1            
            for i in range(down,up):
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.sin(i*self.frec)),i),self.colorLine)
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1) + self.amp*math.cos(i*self.frec)),i),(255,0,0))
                surface.set_at((int(x1+((x2-x1)/(y2-y1))*(i-y1)),i),(255,255,0))
        self.ship1.draw(surface)
        self.ship2.draw(surface)
    
    def vel (self, direction1, direction2):
        self.ship1.vel(direction1)
        self.ship2.vel(direction2)
        
    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.ship1.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ship2.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        
    def getPos(self):
        return (self.ship1.getPos(),self.ship2.getPos())
                
    