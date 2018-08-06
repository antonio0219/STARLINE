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
        self.deadTime = 0
        self.numberImage = 0
        self.state = 'living'

        self.explosionImage = [
            pygame.image.load("assets/images/explosion/expl1.png"),
            pygame.image.load("assets/images/explosion/expl2.png"),
            pygame.image.load("assets/images/explosion/expl3.png"),
            pygame.image.load("assets/images/explosion/expl4.png"),
            pygame.image.load("assets/images/explosion/expl5.png"),
            pygame.image.load("assets/images/explosion/expl6.png"),
            pygame.image.load("assets/images/explosion/expl7.png"),
            pygame.image.load("assets/images/explosion/expl8.png"),
            pygame.image.load("assets/images/explosion/expl9.png")                
            ]
        
    def getPos(self):
        return (self.x, self.y)        
        
    def draw(self, surface, GAME_TIME):
        if self.state == 'living':
            imageToDraw = self.shipImage
        else:
            imageToDraw = self.explosionImage[self.numberImage]
            if GAME_TIME.get_ticks()-self.deadTime >= 40:
                if self.numberImage == 8:
                    self.state = 'dead'
                if self.numberImage < 8 :
                    self.numberImage += 1
                self.deadTime = GAME_TIME.get_ticks()
        rect = imageToDraw.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(imageToDraw,rect)
        
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

    def isDead(self):
        return self.state == 'dead'
    
    def isBlowUp(self):
        return self.state == 'blowup'
    
    def kill(self, time):
        self.deadTime = time
        self.state = 'blowup'
    
    def goTo(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.numberImage = 0
    
    def revive(self):
        self.state = 'living'
        
class doubleShip :
    def __init__(self, type1, xo1, yo1, type2, xo2, yo2, pygame):
        self.ship1=ship(type1, xo1, yo1, pygame)
        self.ship2=ship(type2, xo2, yo2, pygame)
        self.colorLine = (255, 255, 255)
        self.frec = 1/5
        self.amp = 5
        self.displacements = ((0,-25),(0,25), (25,25), (-25,25), (-12,0), (12,0))

    def draw(self, surface, GAME_TIME):
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
        self.ship1.draw(surface, GAME_TIME)
        self.ship2.draw(surface, GAME_TIME)
    
    def vel (self, direction1, direction2):
        self.ship1.vel(direction1)
        self.ship2.vel(direction2)
        
    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.ship1.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ship2.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        
    def getPos(self):
        return (self.ship1.getPos(),self.ship2.getPos())
    
    def getPoints(self):
        toReturn = []
        for desp in self.displacements:
            toReturn.append((self.ship1.getPos()[0]+desp[0], self.ship1.getPos()[1]+desp[1]))
            toReturn.append((self.ship2.getPos()[0]+desp[0], self.ship2.getPos()[1]+desp[1]))
        return toReturn
    
    def toDie(self, GAME_TIME):
        self.ship1.kill(GAME_TIME.get_ticks())
        self.ship2.kill(GAME_TIME.get_ticks())
        
    def isDead(self):
        return self.ship1.isDead() or self.ship2.isDead()
    
    def goTo(self, Xo1, Yo1, Xo2, Yo2):
        self.ship1.goTo(Xo1, Yo1)
        self.ship2.goTo(Xo2, Yo2)
    
    def isBlowUp(self):
        return self.ship1.isBlowUp() or self.ship2.isBlowUp()

    def revive(self):
        self.ship1.revive()
        self.ship2.revive()