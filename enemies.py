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
        self.kill = False
        
        if self.type=='alien':
            self.withRotation = pygame.image.load("assets/images/enemies/alien.png")
            self.cockpit = pygame.image.load("assets/images/enemies/cockpit.png")
        else:
            self.withRotation = pygame.image.load("assets/images/enemies/bomb.png")
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
        self.angle = 0
        self.pygame = pygame
        self.state = 'living'
        self.deadTime = 0
        self.numberImage = 0

    def hablar(self):
        print('hola soy un '+ self.type + ' que está en las coordenadas ' + str(self.x) + ' y ' + str(self.y))

    def draw(self, surface, GAME_TIME):
        if self.state == 'living':
            imageToDraw = self.pygame.transform.rotate(self.withRotation,self.angle)
        else:
            imageToDraw = self.explosionImage[self.numberImage]
            if GAME_TIME.get_ticks()-self.deadTime >= 10:
                if self.numberImage == 8:
                    self.state = 'dead'
                if self.numberImage < 8 :
                    self.numberImage += 1
                self.deadTime = GAME_TIME.get_ticks()
        rect = imageToDraw.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(imageToDraw,rect)    
        if self.type == 'alien' and self.state == 'living':
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

    def dead (self, pos1, pos2, pointsShips, GAME_TIME):
        for point in pointsShips:
            if math.sqrt( (self.x-point[0])**2 + (self.y-point[1])**2 ) < self.radius:
                if self.state == 'living' :
                   self.state = 'blowup'
                   self.deadTime = GAME_TIME.get_ticks()
                   print ('tengo que morir, noooooo') 
                   self.kill = True
        if pos2[0]==pos1[0]:
            dist = abs(self.x-pos1[0])
        else:
            a = (pos2[1]-pos1[1])/(pos2[0]-pos1[0])
            b = pos1[1]-a*pos1[0]
            dist = abs(a*self.x-self.y+b)/math.sqrt(a**2+1)
        if pos2[0]>pos1[0]:
            upx = pos2[0]
            downx = pos1[0]
        else:
            upx = pos1[0]
            downx = pos2[0]
        if pos2[1]>pos1[1]:
            upy = pos2[1]
            downy = pos1[1]
        else:
            upy = pos1[1]
            downy = pos2[1]
        if self.x-self.radius<upx and self.x+self.radius>downx:
            #print ('estoy dentro en x')
            if self.y-self.radius<upy and self.y+self.radius>downy:
                #print ('estoy dentro en y')
                if dist <= self.radius and self.state == 'living':
                    self.state = 'blowup'
                    self.deadTime = GAME_TIME.get_ticks()
                    #print ('tengo que morir, noooooo')
                    if self.type == 'bomb' :
                        self.kill = True
        #print ('distancia :' + str(dist))

    def isdead(self):
        return (self.state == 'dead', self.kill)
    
    def isAlien(self):
        return self.type == 'alien'
                    
class message:
    
    def __init__(self, text, to, duration, x, y, timeCharacter, pygame):
        self.x = int(x)
        self.y = int(y)
        self.messageImage = pygame.image.load("assets/images/background/messageImage.png")
        self.text = text
        self.to = to
        self.duration = int(duration)
        self.timeCharacter = int(timeCharacter)
        self.toDraw = ''
        self.lastCharacterTime = 0
        
    def draw(self, surface, GAME_TIME, textFont, pygame):
        if len(self.text) > 0 :
            if GAME_TIME.get_ticks()-self.lastCharacterTime > self.timeCharacter :
                self.toDraw += self.text[0] # Añado la primera letra a la palabra a dibujar
                self.text = self.text[1:] # Quito la primera letra
                self.lastCharacterTime = GAME_TIME.get_ticks()
        rect = self.messageImage.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(self.messageImage,rect)
        renderedText = textFont.render(self.toDraw, 1, (255,255,255))
        rect = renderedText.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(renderedText,rect)

    def isDead(self, GAME_TIME):
        return GAME_TIME.get_ticks()- self.to > self.duration
            
