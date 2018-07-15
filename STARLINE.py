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

# VARIABLES

state = 0
actualTime = 0

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

# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# PYGAME OBJECTS

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('STARLINE')
clock = pygame.time.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("Becker", 40)
levelTitleFont = pygame.font.SysFont("Becker", 30)

# LOAD IMAGES

titleImage = pygame.image.load("assets/images/background/STARLINE.png")
starImage = pygame.image.load("assets/images/background/star.png")
angleStar = 0

#FUNCTIONS

# GENERAL FUNCTIONhhS

def resetPressed():
    global spacePressed, mousePressed, hPressed, upPressed, downPressed, leftPressed, rightPressed
    spacePressed = False
    mousePressed = False
    hPressed = False
    upPressed = False
    downPressed = False
    leftPressed = False
    rightPressed = False

# STATE FUNCTIONS

def quitGame():
    configFile.close()
    pygame.quit()
    sys.exit()
    
def drawStage():
    global surface
    surface.fill((30,30,30))

def welcomeScreen():
    global surface, angleStar
    renderedText = textFont.render('Pantalla de inicio. Pulsa espacio para empezar o \"h\" para ayuda', 1, (255,255,255))
    angleStar += 2
    angleStar = angleStar % 360
    imageToDraw = pygame.transform.rotate(starImage,angleStar)
    rect = imageToDraw.get_rect()
    rect.center = (625,220)
    surface.blit(imageToDraw,rect)
    surface.blit(renderedText, (100, 100))
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
    
def story():
    global surface
    renderedText = textFont.render('Diálogos. Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    
def inGame():
    global surface
    renderedText = textFont.render('Jugando... Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    

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
            state = 5
            resetPressed()
            
    if state == 1: # LeveSelector
        levelSelector()
        if (spacePressed or mousePressed) and configList[level][3]=='True':
            state += 1
            resetPressed()
            
    if state == 2:
        startAnimation()
        if spacePressed or mousePressed:
            state += 1
            resetPressed()
    
    if state == 3:
        story()
        if spacePressed or mousePressed:
            state += 1
            resetPressed()
    
    if state == 4:
        inGame()
        if spacePressed or mousePressed:
            state = 1
            resetPressed()
    
    if state == 5:
        helpScreen()
        if spacePressed or mousePressed:
            state = 0
            resetPressed()
    
    
    clock.tick(FPS)
    pygame.display.update()
    

        
