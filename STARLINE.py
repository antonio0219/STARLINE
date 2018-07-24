#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:21:31 2018

@author: Antonio Muñoz Santiago, FMC

This is the main file
"""

import pygame, sys, random
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME
import csv

import enemies, ship

# VARIABLES

state = 0
startTime = 0

configFile = open('assets/config/config.csv')
configReader = csv.reader(configFile, delimiter=';')
configList = list(configReader)

spacePressed = False
mousePressed = False
hPressed = False
upPressed = False
downPressed = False
leftPressed = False
rightPressed = False

level = 0
nextLevel = False
tipo1 = 1
tipo2 = 1

enemiesList = []

#levelFile = open(configList[0][0])
#levelReader = csv.reader(levelFile, delimiter=';')
#levelList = list(configReader)
            
# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
Xo1 = 300 
Yo1 = 100
Xo2 = 300
Yo2 = 700
VELSHIP = 10

# PYGAME OBJECTS

pygame.display.init()
pygame.mixer.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('STARLINE')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("Becker", 40)
levelTitleFont = pygame.font.SysFont("Becker", 30)

# LOAD IMAGES

titleImage = pygame.image.load("assets/images/background/STARLINE.png")
starImage = pygame.image.load("assets/images/background/star.png")
angleStar = 0
skyImage = pygame.image.load("assets/images/background/sky.png")

#FUNCTIONS

# GENERAL FUNCTIONhhS

def resetPressed():
    global spacePressed, mousePressed, hPressed, upPressed, downPressed, leftPressed, rightPressed, nextLevel
    spacePressed = False
    mousePressed = False
    hPressed = False
    
    upPressed = False
    downPressed = False
    leftPressed = False
    rightPressed = False
    
    aPressed = False
    dPressed = False
    sPressed = False
    wPressed = False
    
    nextLevel = False

# STATE FUNCTIONS

def quitGame():
    configFile.close()
    pygame.quit()
    sys.exit()
    
def drawStage():
    global surface
    surface.blit(skyImage, (0,0))

def welcomeScreen():
    global surface, angleStar
    renderedText = textFont.render('Pantalla de inicio. Pulsa espacio para empezar o \"h\" para ayuda', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    angleStar += 2
    angleStar = angleStar % 360
    imageToDraw = pygame.transform.rotate(starImage,angleStar)
    rect = imageToDraw.get_rect()
    rect.center = (625,220)
    surface.blit(imageToDraw,rect)    
    surface.blit(titleImage, (130,235))

def helpScreen():
    global surface
    renderedText = textFont.render('Te estoy ayudando', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))

    
def levelSelector():
	global surface, configList, level
	if downPressed and level < len(configList) - 1 :
		level += 1
		resetPressed()
	elif upPressed and level > 0 :
		level -= 1
		resetPressed()
	if configList[level][3] == "True" :
		renderedText = levelTitleFont.render(configList[level][1], 1, (0,255,0))
	else :
		renderedText = levelTitleFont.render(configList[level][1], 1, (255,0,0))
	surface.blit(renderedText, (100, 100))

def startAnimation():
    global surface
    renderedText = textFont.render('Animacion de inicio de nivel. Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
        
def inGame():
    global surface, levelList, enemiesList, nextLevel
    print('entrado ingame')
    print(len(levelList))
    if len(levelList)>0 :
        if (GAME_TIME.get_ticks() - startTime > int(levelList[0][0])):
            enemiesList.append(enemies.enemy(levelList[0][1],int(levelList[0][2]),int(levelList[0][3]),int(levelList[0][4]),int(levelList[0][5]),random.randint(-10,10),pygame))
            levelList.pop(0)
    else :
        if len(enemiesList) == 0 :
            configList[level+1][3] = 'True'
            nextLevel = True
            print('Parece que hemos terminando')

    for i,enemy in enumerate(enemiesList):
        enemy.move()
        enemy.draw(surface)
        enemy.hablar()
        if enemy.out(WINDOW_WIDTH, WINDOW_HEIGHT) :
            enemiesList.pop(i)
    
    player.draw(surface)

def chooseShip():
    global type1, type2, surface
    renderedText = textFont.render('Selección de nave. Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    type1 = 1
    type2 = 2
   
# MUSIC
    
def music(i):
    if i == 'menu':
        pygame.mixer.music.load('assets/music/Chronometry.mp3')
        pygame.mixer.music.play(-1)
    
     
    

# MAIN LOOP

while True:
    drawStage()
    # Handle user and system events 
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                quitGame()
            if event.key == pygame.K_SPACE :
                spacePressed = True
            if event.key == pygame.K_h :
                hPressed = True
            if event.key == pygame.K_UP:
                upPressed = True
            if event.key == pygame.K_DOWN:
                downPressed = True
            if event.key == pygame.K_RIGHT:
                rightPressed = True
            if event.key == pygame.K_LEFT:
                leftPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upPressed = False
            if event.key == pygame.K_DOWN:
                downPressed = False
            if event.key == pygame.K_RIGHT:
                rightPressed = False
            if event.key == pygame.K_LEFT:
                leftPressed = False
          
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()
 
    if state == 0 :
        welcomeScreen()
        if spacePressed or mousePressed:
            state = 1
            resetPressed()
        if hPressed :
            state = 5
            resetPressed()
            
    if state == 1: # LeveSelector
        levelSelector()
        if (spacePressed or mousePressed) and configList[level][3]=='True':
            state += 1
            resetPressed()
            levelFile = open('assets/levels/'+configList[level][0])
            levelReader = csv.reader(levelFile, delimiter=';')
            levelList = list(levelReader)
    
            
    if state == 2: 
        startAnimation()
        if spacePressed or mousePressed:
            state += 1
            resetPressed()

    if state == 3:
        chooseShip()
        if spacePressed or mousePressed:
            state += 1
            resetPressed()
            player = ship.doubleShip(type1, Xo1, Yo1, type2, Xo2, Yo2, VELSHIP, pygame)
            startTime = GAME_TIME.get_ticks()
    
    if state == 4:
        inGame()
        if upPressed:
            player.move('up', 'none')
        if rightPressed:
            player.move('right', 'none')
        if leftPressed:
            player.move('left', 'none')
        if downPressed:
            player.move('down', 'none')
        if nextLevel:
            state = 1
            resetPressed()
        
    
    if state == 5:
        helpScreen()
        if spacePressed or mousePressed:
            state = 0
            resetPressed()
    
    
    clock.tick(FPS)
    pygame.display.update()
    

        
