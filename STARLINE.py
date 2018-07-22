#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:21:31 2018

@author: Antonio Muñoz Santiago, FMC

This is the main file
"""

import pygame, sys
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME
import csv

import enemies

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

enemiesList = []
#levelFile = open(configList[0][0])
#levelReader = csv.reader(levelFile, delimiter=';')
#levelList = list(configReader)
            
# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# PYGAME OBJECTS

pygame.display.init()
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
            enemiesList.append(enemies.enemy(levelList[0][1],int(levelList[0][2]),int(levelList[0][3]),int(levelList[0][4]),int(levelList[0][5]),pygame))
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
            state = 4
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
            startTime = GAME_TIME.get_ticks()
    
    if state == 3:
        inGame()
        if nextLevel:
            state = 1
            resetPressed()
    
    if state == 4:
        helpScreen()
        if spacePressed or mousePressed:
            state = 0
            resetPressed()
    
    
    clock.tick(FPS)
    pygame.display.update()
    

        
