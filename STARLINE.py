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
spaceReleased = False

upButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
downButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
startButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()

nextLevel = False

enemiesList = []
actualMessage = None

Xo1 = None
Yo1 = None
Xo2 = None
Yo2 = None

startAnimationChoose = [False, False] # It will be used in state chooseShip while the animation of the ship is running
up = [True, True] # it will be used by chooseShip animation. If True the ship will exit the screen rising
shipIsOut = [False, False]


deltaTime = 0
lastTime = 0
multiplier = 1
   
         
# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 30
XLABEL = 500
YLABEL = 500
XLOGO = 500
YLOGO = 200
XARROWUP = 500
YARROWUP = 375
XARROWDOWN = 500
YARROWDOWN = 625
timeButtonPressed = 500
XSTARTBUTTON = 450
YSTARTBUTTON = 300
MAXTYPES = 11
XSELECTION = [745, 245]
YSELECTION = [350, 350]
XANIMATION = [random.randint(550,800), random.randint(200,450)]
YANIMATION = [random.randint(800,1000), random.randint(800,1000)]
XPLANET = 500
YPLANET = 575


# PYGAME OBJECTS

pygame.display.init()
pygame.mixer.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('STARLINE')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.Font("assets/fonts/nasalization-rg.ttf", 30)
levelTitleFont = pygame.font.Font("assets/fonts/nasalization-rg.ttf", 30)
type = [int(configList[0][0]), int(configList[0][1])]
configList.pop(0)
level = -1
player = ship.doubleShip(type[0], Xo1, Yo1, type[1], Xo2, Yo2, pygame)
playerChoose = [ship.ship(type[0], XSELECTION[0], YSELECTION[0], pygame, 'big'), ship.ship(type[1], XSELECTION[1], YSELECTION[1], pygame, 'big')]
menuMessage = enemies.message('Presiona espacio', 0, 'infinity', 500, 500, 100, pygame)


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
startButtonUp = pygame.image.load("assets/images/buttons/startButtonUp.png")
startButtonDown = pygame.image.load("assets/images/buttons/startButtonDown.png")
backgroundPlanet = pygame.image.load("assets/images/background/backgroundPlanet.png")
youWinImage = pygame.image.load("assets/images/background/wellDoneImage.png")

# LOAD SOUNDS

clickSound = pygame.mixer.Sound('assets/sounds/click.ogg')
completedSound = pygame.mixer.Sound('assets/sounds/completed.ogg')
gameOverSound = pygame.mixer.Sound('assets/sounds/shipExplosion.ogg')
        

#FUNCTIONS

# GENERAL FUNCTIONS

def resetPressed():
    global spaceReleased, hPressed, upPressed, downPressed, leftPressed, rightPressed, aPressed, dPressed, sPressed, wPressed, rPressed, pPressed
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
    
    spaceReleased = False

# STATE FUNCTIONS

def quitGame():
    configFile.close()
    configFileWrite = open('assets/config/config.csv', 'w',  newline='')
    configWriter = csv.writer(configFileWrite, delimiter=';')
    configWriter.writerow(type)
    for item in configList:
        configWriter.writerow(item)
    configFileWrite.close()
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
    menuMessage.draw(surface, GAME_TIME, textFont, pygame)

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
        playSound('click')
        resetPressed()
    elif upPressed and level > -1 :
        level -= 1
        playSound('click')
        resetPressed()
	
    if level == -1 :
        imageToDraw = grayLevel
        renderedText = levelTitleFont.render('Plataforma de lanzamiento', 1, (255,255,255))
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
    global surface, kAnim, playerChoose, state, XANIMATION, YANIMATION, startTime
    rect = backgroundPlanet.get_rect()
    rect.center = (XPLANET,YPLANET)
    surface.blit(backgroundPlanet,rect) 

    res1 = playerChoose[0].moveSlow(XANIMATION[0], -400, multiplier, 0.4)
    res2 = playerChoose[1].moveSlow(XANIMATION[1], -400, multiplier, 0.4)
    playerChoose[0].draw(surface, GAME_TIME)
    playerChoose[1].draw(surface, GAME_TIME)
    
    if res1 and res2:
        state = 'inGame'
        music('inGame')
        resetPressed()
        startTime = GAME_TIME.get_ticks()
        XANIMATION = [random.randint(550,800), random.randint(200,450)]
        YANIMATION = [random.randint(800,1000), random.randint(800,1000)]
    
        
def inGame():
    global surface, levelList, enemiesList, actualMessage, nextLevel, state, rPressed, player, startTime, levelList, levelFile, levelReader, level
    if len(levelList)>0 : # Si quedan mensajes o enemigos por procesar
        while len(levelList)>0 and (GAME_TIME.get_ticks() - startTime > int(levelList[0][0])) and not player.isDead() and not player.isBlowUp(): # No añadimos nuevos enemigos si ya nos han matado
            #if not player.isDead() and not player.isBlowUp() : # No añadimos nuevos enemigos si ya nos han matado
            if levelList[0][1] == 'message' : # Si hay que crear el nuevo mensaje
                actualMessage = enemies.message(levelList[0][2], GAME_TIME.get_ticks(), levelList[0][3], levelList[0][4], levelList[0][5], levelList[0][6], pygame) # Creamos el mensaje
                print('añadido mensaje en '+ str(GAME_TIME.get_ticks()))
                print('tamaño de lista = ' + str(len(levelList)))
            else : # Hay que añadir un enemigo
                enemiesList.append(enemies.enemy(levelList[0][1],int(levelList[0][2]),int(levelList[0][3]),int(levelList[0][4]),int(levelList[0][5]),random.randint(-10,10),pygame))
                print('añadido enemigo')
                print('tamaño de lista = ' + str(len(levelList)))
            levelList.pop(0)
    else :
        if len(enemiesList) == 0 and not player.isDead() and not player.isBlowUp() and actualMessage is None:
            if len(configList) > level+1:
                configList[level+1][3] = 'True'
            if nextLevel == False :
                music('spaceAmbient')
                playSound('completed')
                nextLevel = True
                resetPressed()

    for i,enemy in enumerate(enemiesList):
        enemy.move(multiplier)
        enemy.draw(surface, GAME_TIME)
        #enemy.hablar()
        if enemy.out(WINDOW_WIDTH, WINDOW_HEIGHT) or enemy.isdead()[0]:
            enemiesList.pop(i)
        if not player.isDead() and not player.isBlowUp():
            enemy.dead(player.getPos()[0],player.getPos()[1], player.getPoints(), GAME_TIME)
            if enemy.isdead()[1] or (enemy.out(WINDOW_WIDTH, WINDOW_HEIGHT) and enemy.isAlien()):
                player.toDie(GAME_TIME) # Enters here when ship is killed
                music('spaceAmbient')
                playSound('gameOver')
                resetPressed()

    if not player.isDead():
        player.move(WINDOW_WIDTH, WINDOW_HEIGHT, multiplier)
        player.draw(surface, GAME_TIME)

    if actualMessage is not None and not player.isDead():
        actualMessage.draw(surface, GAME_TIME, textFont, pygame)
        if actualMessage.isDead(GAME_TIME) :
            actualMessage = None
            print('Elminado Mensaje en: ' + str(GAME_TIME.get_ticks()))

    if player.isDead() or nextLevel:
        if nextLevel:
            surface.blit(youWinImage, (100, 69))
        else:
            surface.blit(gameOverImage, (83, 69))
        actualMessage = None
        if rPressed: 
            state = 'inGame'
            music('inGame')
            playSound('click')
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
            nextLevel = False
            resetPressed()


def chooseShip():
    global type, surface, startAnimationChoose, playerChoose, up, shipIsOut

    upPres = [upPressed, wPressed]
    downPres = [downPressed, sPressed]
    
    for num in range(0,2):
        if startAnimationChoose[num] :
            if not shipIsOut[num]: # Si todavía no ha salido la nave vieja
                if up[num] :
                    shipIsOut[num] = playerChoose[num].moveSlow(XSELECTION[num], -300, 0.5, multiplier) # Movemos la nave vieja fuera de la pantalla y activamos shipIsOut cuando sale
                else:
                    shipIsOut[num] = playerChoose[num].moveSlow(XSELECTION[num], WINDOW_HEIGHT+300, 0.5, multiplier)
                if shipIsOut[num] : # Sólo una vez, cuando la nave ha salido, creo la nueva nave con al nuevo tipo
                    if up[num]:
                        playerChoose[num] = ship.ship(type[num], XSELECTION[num], WINDOW_HEIGHT + 100, pygame, 'big')
                    else:
                        playerChoose[num] = ship.ship(type[num], XSELECTION[num], -100 , pygame, 'big')
            elif playerChoose[num].moveSlow(XSELECTION[num], YSELECTION[num], 0.5, multiplier) : # Movemos la nave al centro y comprobamos simultáneamente si ha llegado
                playerChoose[num].goTo(XSELECTION[num],YSELECTION[num])
                startAnimationChoose[num] = False
                resetPressed()
                shipIsOut = [False, False]

        if upPres[num] and not startAnimationChoose[num]:
            type[num] -= 1
            type[num] = type[num] % MAXTYPES
            resetPressed()
            startAnimationChoose[num] = True
            up[num] = True
        elif downPres[num] and not startAnimationChoose[num]:
            type[num] += 1
            type[num] = type[num] % MAXTYPES
            resetPressed()
            startAnimationChoose[num] = True
            up[num] = False        

        playerChoose[num].draw(surface, GAME_TIME)
    
    if startButtonPressedToDraw: # Draw the button when it is pressed
        surface.blit(startButtonDown, (XSTARTBUTTON + 10, YSTARTBUTTON + 10))            
    else:
        surface.blit(startButtonUp, (XSTARTBUTTON, YSTARTBUTTON))  
    
# MUSIC AND SOUNDS CONTROL
    
def music(i):
    pygame.mixer.stop()
    if i == 'menu':
        pygame.mixer.music.load('assets/music/A New Dimension.ogg')
        pygame.mixer.music.play(-1)
    elif i == 'animation':
        pygame.mixer.music.load('assets/sounds/animationSound.ogg')
        pygame.mixer.music.play(-1)
    elif i == 'inGame':
        pygame.mixer.music.load('assets/music/' + configList[level][2])
        pygame.mixer.music.play(-1)
    elif i == 'spaceAmbient':
        pygame.mixer.music.load('assets/sounds/spaceAmbient.ogg')
        pygame.mixer.music.play(-1)
    
def playSound(i):
    if i == 'click':
        clickSound.play()
    elif i == 'completed':
        completedSound.play()
    elif i == 'gameOver':
        gameOverSound.play()
    

# MAIN LOOP

music('menu')
while True:
    drawStage()
    # Handle user and system events 
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                playSound('click')
                if state == 'welcomeScreen':
                    quitGame()
                elif state == 'levelSelector':
                    state = 'welcomeScreen'
                    menuMessage.reset()
                elif state == 'chooseShip':
                    state = 'levelSelector'    
                elif state == 'inGame':
                    state = 'levelSelector'
                    music('menu')
                    nextLevel = False
                resetPressed()
            if event.key == pygame.K_SPACE :
                spacePressed = True
                startButtonPressedToDraw = True # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
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
            if event.key == pygame.K_SPACE :
                spaceReleased = True
                spacePressed = False
                startButtonPressedToDraw = False # Only to show the button pressed in the level selector screen. Not reset by resetPressed()
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
        if spaceReleased:
            state = 'levelSelector'
            playSound('click')
            resetPressed()
            
    if state == 'levelSelector': # LevelSelector
        levelSelector()
        if spaceReleased:
            if (level == -1):
                state = 'chooseShip'
                for num in range(0,2):
                    playerChoose[num].goTo(XSELECTION[num],YSELECTION[num])
                    shipIsOut = [False, False]
                    startAnimationChoose[num] = False
                resetPressed()
            elif (configList[level][3]) == 'True':
                state = 'startAnimation'
                music('animation')
                playSound('click')
                XANIMATION = [random.randint(550,800), random.randint(200,450)]
                YANIMATION = [random.randint(800,1200), random.randint(800,1200)]
                playerChoose[0].goTo(XANIMATION[0],YANIMATION[0])
                playerChoose[1].goTo(XANIMATION[1],YANIMATION[1])
                resetPressed()
                levelFile = open('assets/levels/'+configList[level][0])
                levelReader = csv.reader(levelFile, delimiter=';')
                levelList = list(levelReader)
                enemiesList = []
                actualMessage = None
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

        if spaceReleased:
            state = 'levelSelector'
            resetPressed()
            player = ship.doubleShip(type[0], Xo1, Yo1, type[1], Xo2, Yo2, pygame)
            for num in range(0,2):
                playerChoose[num].goTo(XSELECTION[num],YSELECTION[num])
                startAnimationChoose[num] = False
            
    if state == 'startAnimation': 
        startAnimation()
        if spacePressed:
            state = 'inGame'
            music('inGame')
            resetPressed()
            kAnim = 0
            XANIMATION = [random.randint(550,800), random.randint(200,450)]
            YANIMATION = [random.randint(800,1200), random.randint(800,1200)]
            playerChoose[0].goTo(XANIMATION[0],YANIMATION[0])
            playerChoose[1].goTo(XANIMATION[1],YANIMATION[1])
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
    
    
    clock.tick(FPS)
    deltaTime = GAME_TIME.get_ticks() - lastTime
    lastTime = GAME_TIME.get_ticks()
    multiplier = deltaTime * FPS * 1E-3
    pygame.display.update()