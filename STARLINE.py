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


# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# PYGAME OBJECTS

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('STARLINE')
clock = pygame.time.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("Becker", 40)

# LOAD IMAGES


# FUNCTIONS

def quitGame():
    cofigFile.close()
    pygame.quit()
    sys.exit()
    
def drawStage():
    global surface
    surface.fill((0,0,0))

def welcomeScreen():
    global surface
    renderedText = textFont.render('Pantalla de inicio. Pulsa espacio o presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    
def levelSelector():
    global surface
    renderedText = textFont.render('Selector de nivel. Presiona el ratón', 1, (255,255,255))
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    if state == 0 :
        welcomeScreen()
        if spacePressed or mousePressed:
            state += 1
            spacePressed = False
            mousePressed = False
            
    if state == 1:
        levelSelector()
        if spacePressed or mousePressed:
            state += 1
            spacePressed = False
            mousePressed = False
            
    if state == 2:
        startAnimation()
        if spacePressed or mousePressed:
            state += 1
            spacePressed = False
            mousePressed = False
    
    if state == 3:
        story()
        if spacePressed or mousePressed:
            state += 1
            spacePressed = False
            mousePressed = False
    
    if state == 4:
        inGame()
        if spacePressed or mousePressed:
            state = 1
            spacePressed = False
            mousePressed = False
    
    
    clock.tick(FPS)
    pygame.display.update()
    

        