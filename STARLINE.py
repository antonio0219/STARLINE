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

state = 'welcomeScreen'
startTime = 0

configFile = open('assets/config/config.csv')
configReader = csv.reader(configFile, delimiter=';')
configList = list(configReader)

spacePressed = False
hPressed = False
upPressed = False
downPressed = False
leftPressed = False
rightPressed = False

upButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
downButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()

level = -1
nextLevel = False
tipo1 = 1
tipo2 = 1

enemiesList = []
actualMessage = None

Xo1 = None
Yo1 = None
Xo2 = None
Yo2 = None

#levelFile = open(configList[0][0])
#levelReader = csv.reader(levelFile, delimiter=';')
#levelList = list(configReader)
            
# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
XLABEL = 500
YLABEL = 500
XLOGO = 500
YLOGO = 200
XARROWUP = 500
YARROWUP = 375
XARROWDOWN = 500
YARROWDOWN = 625
timeButtonPressed = 500

# PYGAME OBJECTS

pygame.display.init()
pygame.mixer.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('STARLINE')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("Becker", 40)
levelTitleFont = pygame.font.SysFont("Becker", 30)
type1 = 1 # TODO: from config file.
type2 = 2 # TODO: from config file.
player = ship.doubleShip(type1, Xo1, Yo1, type2, Xo2, Yo2, pygame)

# LOAD IMAGES

titleImage = pygame.image.load("assets/images/background/STARLINE.png")
starImage = pygame.image.load("assets/images/background/star.png")
angleStar = 0
skyImage = pygame.image.load("assets/images/background/sky.png")
chooseShipImage = pygame.image.load("assets/images/background/shipSelector.png")
gameOverImage = pygame.image.load("assets/images/background/gameOver.png")
redLevel = pygame.image.load("assets/images/background/redLevel.png")
grayLevel = pygame.image.load("assets/images/background/grayLevel.png")
greenLevel = pygame.image.load("assets/images/background/greenLevel.png")
arrowUpSmallImage = pygame.image.load("assets/images/buttons/buttonUpSmall.png")
arrowUpBigImage = pygame.image.load("assets/images/buttons/buttonUpBig.png")
arrowDownSmallImage = pygame.image.load("assets/images/buttons/buttonDownSmall.png")
arrowDownBigImage = pygame.image.load("assets/images/buttons/buttonDownBig.png")

#FUNCTIONS

# GENERAL FUNCTIONS

def resetPressed():
    global spacePressed, hPressed, upPressed, downPressed, leftPressed, rightPressed, nextLevel, aPressed, dPressed, sPressed, wPressed, rPressed, pPressed
    spacePressed = False
    hPressed = False
    pPressed = False
    rPressed = False
    
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
    if state == 'chooseShip':
        surface.blit(chooseShipImage, (0,0))
    else:
        surface.blit(skyImage, (0,0))

def drawLogo():
    global surface, angleStar
    angleStar += 2
    angleStar = angleStar % 360
    imageToDraw = pygame.transform.rotate(starImage,angleStar)
    rect = imageToDraw.get_rect()
    rect.center = (XLOGO+150,YLOGO-70)
    surface.blit(imageToDraw,rect) 
    rect = titleImage.get_rect()
    rect.center = (XLOGO,YLOGO)
    surface.blit(titleImage, rect)
    
def welcomeScreen():
    global surface
    drawLogo()  
    renderedText = textFont.render('Pantalla de inicio. Pulsa espacio para empezar o \"h\" para ayuda', 1, (255,255,255))
    surface.blit(renderedText, (100, 500))

def helpScreen():
    global surface
    renderedText = textFont.render('Te estoy ayudando', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))

def drawArrows():
    global surface
    if not upButtonPressedToDraw :
        imageToDrawUp = arrowUpBigImage
    else:
        imageToDrawUp = arrowUpSmallImage
    if not downButtonPressedToDraw :
        imageToDrawDown = arrowDownBigImage
    else:
        imageToDrawDown = arrowDownSmallImage
    rect = imageToDrawUp.get_rect()
    rect.center = (XARROWUP,YARROWUP)
    surface.blit(imageToDrawUp,rect)
    rect = imageToDrawDown.get_rect()
    rect.center = (XARROWDOWN,YARROWDOWN)
    surface.blit(imageToDrawDown,rect)
    

    
def levelSelector():
    global surface, configList, level
    drawLogo() # To draw the logo of the game.
    drawArrows()
    
    if downPressed and level < len(configList) - 1 : # -1 represents the ship selector, not really a level
        level += 1
        resetPressed()
    elif upPressed and level > -1 :
        level -= 1
        resetPressed()
	
    if level == -1 :
        imageToDraw = grayLevel
        renderedText = levelTitleFont.render('Ship selection', 1, (255,255,255))
    elif configList[level][3] == "True" :
        imageToDraw = greenLevel
        renderedText = levelTitleFont.render(configList[level][1], 1, (255,255,255))
    else :
        imageToDraw = redLevel
        renderedText = levelTitleFont.render(configList[level][1], 1, (255,255,255))
    rect = imageToDraw.get_rect()
    rect.center = (XLABEL,YLABEL)
    surface.blit(imageToDraw,rect)
    rect = renderedText.get_rect()
    rect.center = (XLABEL,YLABEL)
    surface.blit(renderedText,rect)    
 
def startAnimation():
    global surface
    renderedText = textFont.render('Animacion de inicio de nivel. Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
        
def inGame():
    global surface, levelList, enemiesList, actualMessage, nextLevel, state, rPressed, player, startTime, levelList, levelFile, levelReader, level
    if len(levelList)>0 : # Si quedan mensajes o enemigos por procesar
        if (GAME_TIME.get_ticks() - startTime > int(levelList[0][0])):
            if not player.isDead() and not player.isBlowUp() : # No añadimos nuevos enemigos si ya nos han matado
                if levelList[0][1] == 'message' : # Si hay que crear el nuevo mensaje
                    actualMessage = enemies.message(levelList[0][2], GAME_TIME.get_ticks(), levelList[0][3], levelList[0][4], levelList[0][5], levelList[0][6], pygame) # Creamos el mensaje
                    print('añadido mensaje')
                    print('tamaño de lista = ' + str(len(levelList)))
                else : # Hay que añadir un enemigo
                    enemiesList.append(enemies.enemy(levelList[0][1],int(levelList[0][2]),int(levelList[0][3]),int(levelList[0][4]),int(levelList[0][5]),random.randint(-10,10),pygame))
                    print('añadido enemigo')
                    print('tamaño de lista = ' + str(len(levelList)))
                levelList.pop(0)
    else :
        if len(enemiesList) == 0 and not player.isDead() and not player.isBlowUp():
            configList[level+1][3] = 'True'
            nextLevel = True

    for i,enemy in enumerate(enemiesList):
        enemy.move()
        enemy.draw(surface, GAME_TIME)
        #enemy.hablar()
        if enemy.out(WINDOW_WIDTH, WINDOW_HEIGHT) or enemy.isdead()[0]:
            enemiesList.pop(i)
        if not player.isDead() and not player.isBlowUp():
            enemy.dead(player.getPos()[0],player.getPos()[1], player.getPoints(), GAME_TIME)
            if enemy.isdead()[1] or (enemy.out(WINDOW_WIDTH, WINDOW_HEIGHT) and enemy.isAlien()):
                player.toDie(GAME_TIME) # Enters here when ship is killed
                resetPressed()
             
    if not player.isDead():
        player.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        player.draw(surface, GAME_TIME)

    if actualMessage is not None and not player.isDead():
        actualMessage.draw(surface, GAME_TIME, textFont, pygame)
        if actualMessage.isDead(GAME_TIME) :
            actualMessage = None
        
    if player.isDead():
        surface.blit(gameOverImage, (83, 69))
        if rPressed: 
            state = 'inGame'
            startTime = GAME_TIME.get_ticks()
            enemiesList = []
            levelFile = open('assets/levels/'+configList[level][0])
            levelReader = csv.reader(levelFile, delimiter=';')
            levelList = list(levelReader)
            Xo1 = int(levelList[0][1])
            Yo1 = int(levelList[0][2])
            levelList.pop(0)
            Xo2 = int(levelList[0][1]) 
            Yo2 = int(levelList[0][2])
            levelList.pop(0)
            player.goTo(Xo1, Yo1, Xo2, Yo2)
            player.revive()
            resetPressed()


def chooseShip():
    global type1, type2, surface
    renderedText = textFont.render('Selección de nave. Presiona el ratón', 1, (255,255,255))
    surface.blit(renderedText, (100, 100))
    type1 = 3
    type2 = 4
   
    
# MUSIC
    
def music(i):
    if i == 'menu':
        pygame.mixer.music.load('assets/music/Chronometry.ogg')
        pygame.mixer.music.play(-1)
    
     
    

# MAIN LOOP

while True:
    drawStage()
    # Handle user and system events 
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                if state == 'welcomeScreen':
                    quitGame()
                elif state == 'levelSelector':
                    state = 'welcomeScreen'
                else :
                    state = 'levelSelector'
            if event.key == pygame.K_SPACE :
                spacePressed = True
            if event.key == pygame.K_h :
                hPressed = True
            if event.key == pygame.K_UP:
                upPressed = True
                upButtonPressedToDraw = True # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
            if event.key == pygame.K_DOWN:
                downPressed = True
                downButtonPressedToDraw = True # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
            if event.key == pygame.K_RIGHT:
                rightPressed = True
            if event.key == pygame.K_LEFT:
                leftPressed = True
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_w:
                wPressed = True
            if event.key == pygame.K_s:
                sPressed = True
            if event.key == pygame.K_p:
                pPressed = True
            if event.key == pygame.K_r:
                rPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upPressed = False
                upButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
            if event.key == pygame.K_DOWN:
                downPressed = False
                downButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
            if event.key == pygame.K_RIGHT:
                rightPressed = False
            if event.key == pygame.K_LEFT:
                leftPressed = False
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_d:
                dPressed = False
            if event.key == pygame.K_w:
                wPressed = False
            if event.key == pygame.K_s:
                sPressed = False
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()
 
    if state == 'welcomeScreen' :
        welcomeScreen()
        if spacePressed:
            state = 'levelSelector'
            resetPressed()
        if hPressed :
            state = 'helpScreen'
            resetPressed()
            
    if state == 'levelSelector': # LevelSelector
        levelSelector()
        if spacePressed:
            if (level == -1):
                state = 'chooseShip'
                resetPressed()
            elif (configList[level][3]) == 'True' :
                state = 'startAnimation'
                resetPressed()
                levelFile = open('assets/levels/'+configList[level][0])
                levelReader = csv.reader(levelFile, delimiter=';')
                levelList = list(levelReader)
                enemiesList = []
                Xo1 = int(levelList[0][1]) 
                Yo1 = int(levelList[0][2])
                levelList.pop(0)
                Xo2 = int(levelList[0][1]) 
                Yo2 = int(levelList[0][2]) 
                levelList.pop(0)
                player.goTo(Xo1, Yo1, Xo2, Yo2)
                player.revive()
                        
    if state == 'chooseShip':
        chooseShip()
        if spacePressed:
            state = 'levelSelector'
            resetPressed()
            player = ship.doubleShip(type1, Xo1, Yo1, type2, Xo2, Yo2, pygame)
            
    if state == 'startAnimation': 
        startAnimation()
        if spacePressed:
            state = 'inGame'
            resetPressed()
            startTime = GAME_TIME.get_ticks()
 
    if state == 'inGame':
        inGame()
        if upPressed:
            player.vel('up', 'none')
        if rightPressed:
            player.vel('right', 'none')
        if leftPressed:
            player.vel('left', 'none')
        if downPressed:
            player.vel('down', 'none')
            
        if aPressed:
            player.vel('none', 'left')
        if dPressed:
            player.vel('none', 'right')
        if sPressed:
            player.vel('none', 'down')
        if wPressed:
            player.vel('none', 'up')
            
        if nextLevel:
            state = 'levelSelector'
            resetPressed()
        
    
    if state == 'helpScreen':
        helpScreen()
        if spacePressed:
            state = 'welcomeScreen'
            resetPressed()
    
    
    clock.tick(FPS)
    pygame.display.update()
    

        
