
import pygame
import sys
from pygame.locals import *
import os
import cv2
import numpy
from classes import *

pygame.init() 

WIDTH = 800
HEIGHT= 600

WHITE = (255,255,255)
BLACK = (0,0,0)

screen=pygame.display.set_mode((WIDTH,HEIGHT))

startb=pygame.image.load("backg.png")
startb=pygame.transform.scale(startb,(WIDTH,HEIGHT))
startb=startb.convert_alpha()

# Get the directory path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

#Create the game class
game=Game()

#take picture button
button = pygame.image.load("button.png")
button=pygame.transform.scale(button,(300,50))
bW = button.get_width()  # measure the image  
bH = button.get_height()  
bX = WIDTH//2 - bW//2  #the center of the screen
bY = HEIGHT//2 - bH//2  #the center of the screen

#business

b1 = pygame.image.load("buiss.png")
b1=pygame.transform.scale(b1,(250,200))
b2 = pygame.image.load("buiss1.png")
b2=pygame.transform.scale(b2,(150,150))
b3 = pygame.image.load("buiss2.png")
b3=pygame.transform.scale(b3,(200,200))
b4 = pygame.image.load("buiss3.png")
b4=pygame.transform.scale(b4,(200,200))
b=[b1,b2,b3,b4]

#casual 
c1=pygame.image.load("cas.png")
c1=pygame.transform.scale(c1,(200,200))
c2 = pygame.image.load("cas1.png")
c2=pygame.transform.scale(c2,(250,300))
c3 = pygame.image.load("cas2.png")
c3=pygame.transform.scale(c3,(200,200))
c=[c1,c2,c3]

#fancy 
f1 = pygame.image.load("fanc.png")
f1=pygame.transform.scale(f1,(200,200))
f2 = pygame.image.load("fanc1.png")
f2=pygame.transform.scale(f2,(200,300))
f3 = pygame.image.load("fanc2.png")
f3=pygame.transform.scale(f3,(200,200))
f4 = pygame.image.load("fanc3.png")
f4=pygame.transform.scale(f4,(250,250))
f=[f1,f2,f3,f4]


matched=pygame.image.load("matched.png")
matched = pygame.transform.scale(matched,(400,70))

i1=pygame.image.load("intro.png")
i2=pygame.image.load("intro1.png")

font=pygame.font.SysFont('Ariel Black',50)

TOP = 0
BOTTOM = HEIGHT
LEFT = 0
RIGHT = WIDTH

# set camera scale
color = False  # True or False
camera_index = 0
camera = cv2.VideoCapture(camera_index)
camera.set(3, 640)
camera.set(4, 480)

# This shows an image the way it should be
cv2.namedWindow("w1", cv2.WINDOW_AUTOSIZE)
retval, frame = camera.read()
cv2.flip(frame, 1, frame)  # mirror the image
cv2.imshow("w1", frame)

#--------------------------------------------#
# set camera scale                           #
#--------------------------------------------#


def getCamFrame(color,camera):
    retval,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame=numpy.rot90(frame)
    frame=pygame.surfarray.make_surface(frame)
    return frame


#--------------------------------------------#
# Game screens                               #
#--------------------------------------------#

def takePic(screen):
  screen.fill(0) #set pygame screen to black
  frame=getCamFrame(color,camera)
  screen.blit(frame,(WIDTH//2-320,HEIGHT//2-210))
  pygame.display.flip()
        
  #Save the image file in the same directory as the script
  image_path = os.path.join(script_dir, "image.jpg")
  pygame.image.save(screen, image_path)

  #PICTURE OF USER
  picture = pygame.image.load("image.jpg")
  picture = pygame.transform.scale(picture,(WIDTH,HEIGHT))

  return picture
#---------------------------------------#
# Intro and Introduction                #
#---------------------------------------#
introScreen = True
while introScreen:
  for event in pygame.event.get():       
    if event.type == pygame.MOUSEBUTTONDOWN:
      posX, posY=pygame.mouse.get_pos()
      if posX>bX and posX<(bX+bW) and posY>bY and posY<(bY+bH): 
        picture=takePic(screen)
        introScreen = False
    elif event.type == QUIT:
      introScreen = False

  screen.blit(i1,(50,50))
  screen.blit(i1,(400,50))
  screen.blit(startb,(0,25))
  screen.blit (button, (bX,bY))
  
  pygame.display.update()
  
#--------------------------------------------#
# the main program begins here               #
#--------------------------------------------#
countClick=0   #Counter that checks once a feature has been pressed

picScreen=True
while picScreen:
  screen.blit(picture,(0,0))
  items=['hair','skin','eye']
  instrucMain=font.render("Click on your "+items[countClick],True,WHITE, (0, 0, 0))
  textRect = instrucMain.get_rect(center=(WIDTH//2,HEIGHT//12))
  screen.blit(instrucMain,textRect)
  
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      posX, posY=pygame.mouse.get_pos()
      game.rgbs.append(list(screen.get_at((posX,posY)))[:3])
      countClick+=1
    if event.type == QUIT or countClick>2:
      picScreen = False
  
  
  fashionmusic=pygame.mixer.Sound("fashion.mp3") 
  pygame.display.update()
  
game.makeColours()
choiceScreen=True
while choiceScreen:
  
  screen.fill(0)
  coordx=int(WIDTH/13)

  for i in range(4):
    rect=pygame.Rect(coordx,HEIGHT//3,int(WIDTH/6.5),HEIGHT//3)
    pygame.draw.rect(screen,game.compColours[i],rect)
    coordx+=int(WIDTH/6.5)+int(WIDTH/13)

  instrucColChoice=font.render("Click on the colour you want to choose:",True,WHITE,(0, 0, 0))
  text_rect = instrucColChoice.get_rect(center=(WIDTH//2,HEIGHT//12))
  screen.blit(instrucColChoice,text_rect)

  pygame.display.update()
    

  for event in pygame.event.get():    
    if event.type == pygame.QUIT:       
      choiceScreen = False                # To exit choice screen
    if event.type == pygame.MOUSEBUTTONDOWN:
      posX, posY=pygame.mouse.get_pos()
      for i in range(4):
        if posX>int((WIDTH/13)+(i*((WIDTH/6.5)+(WIDTH/13)))) and posX<int((WIDTH/13)+(i*((WIDTH/6.5)+(WIDTH/13))+(WIDTH/6.5))) and posY>HEIGHT//3 and posY<(HEIGHT//3)*2:
          game.rgbs=screen.get_at((posX,posY))[:3]
          choiceScreen = False
  
  pygame.display.update()

typescreen=True

while typescreen:
  screen.fill(0)
  occasion=[b,c,f]
  x=25
  occChoice=font.render("Click on your chosen occasion:",True,WHITE,(0, 0, 0))
  text__rect = occChoice.get_rect(center=(WIDTH//2,HEIGHT//12))
  screen.blit(occChoice,text__rect)
  
  for i in range(3):
    rect1=pygame.Rect(x,100,250,600)
    pygame.draw.rect(screen,(0,0,0),rect1)
    if i == 0:
      occrect=font.render("business",25,WHITE)
      screen.blit(occrect,(x,200))
    elif i==1:
      occrect=font.render("casual",25,WHITE)
      screen.blit(occrect,(x,200))
    elif i==2:
      occrect=font.render("fancy",25,WHITE)
      screen.blit(occrect,(x,200))
    x+=250

  for event in pygame.event.get():    
    if event.type == pygame.QUIT:       
      typescreen = False                # To exit choice screen
    if event.type == pygame.MOUSEBUTTONDOWN:
      posX, posY=pygame.mouse.get_pos()
      for i in range(3):
        if posX>(25+(250*i)) and posX<(25+(250*(i+1))) and posY>50 and posY<600:
          occ=occasion[i]
          typescreen = False
  
  pygame.display.update()
  
#---------------------------------------#
# Game Over Section                     #
#---------------------------------------#
gameOver=True
while gameOver:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:       
            gameOver = False # To exit gameOver screen
   
    screen.fill(0)
    screen.blit(matched,(WIDTH//2-(matched.get_width()//2),0))
    occX=0
    for i in occ:
      occX+=i.get_width()
    occX=(WIDTH-occX)//(len(occ)+1)
    occx=occX
    occy=100
    for j in range(len(occ)):
      screen.blit(occ[j],(occx,occy))
      occx=occx+occ[j].get_width()+occX
      colour=pygame.Rect(0,535,800,65)
      pygame.draw.rect(screen,(game.rgbs),colour)
    shirtColText=font.render("This is your shirt colour",True,BLACK,game.rgbs)
    text___rect = shirtColText.get_rect(center=(WIDTH//2,HEIGHT-30))
    screen.blit(shirtColText,text___rect)
    pygame.time.delay(60)
    pygame.display.update()
    
pygame.quit()  
cv2.destroyAllWindows()
sys.exit()