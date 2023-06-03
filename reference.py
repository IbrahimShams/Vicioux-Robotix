from pygame import *

width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()

player=Rect(250,250,25,25)

walls=[Rect(50,100,200,80),Rect(300,250,100,50),Rect(390,470,50,100),Rect(460,70,50,40)]


def drawScene(player,walls):
    screen.fill(BLACK)
    draw.rect(screen,GREEN,player)
    for w in walls:
        draw.rect(screen,RED,w)
    display.flip()

def movePlayer(player):
    keys=key.get_pressed()
    if keys[K_DOWN] and hitWalls(player[0],player[1]+5,walls)==-1:
        player[1]+=5
    elif keys[K_UP] and hitWalls(player[0],player[1]-5,walls)==-1:
        player[1]-=5
    if keys[K_RIGHT] and hitWalls(player[0]+5,player[1],walls)==-1:
        player[0]+=5
    elif keys[K_LEFT] and hitWalls(player[0]-5,player[1],walls)==-1:
        player[0]-=5

def hitWalls(x,y,walls):
    playerRect=Rect(x,y,25,25)
    return playerRect.collidelist(walls)
    #-1 if not colliding (0 or more if colliding)


running=True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    drawScene(player,walls)
    movePlayer(player)
    myClock.tick(60)
   
            
quit()
