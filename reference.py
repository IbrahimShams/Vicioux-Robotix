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

def addPics(name,start,end):
    mypics=[]
    for i in range(start,end+1):
        mypics.append(image.load(f"images/{name}{i:03}.png"))

    return mypics
    

def drawScene(player,picList):
    '''
    this function draws 1 of the 24 pictures from the 2D list
    '''
    screen.fill(GREEN)
    row=player[2]
    col=int(player[3])
    pic=picList[row][col]
    screen.blit(pic,(player[0],player[1]))
    display.flip()


def movePlayer(player):
    '''
    this function changes the x and y location of the player
    It also adjusts the ROW and the COLUMN values in the list
    so that we can show the correct picture
    '''
    if keys[K_RIGHT]:
        player[0]+=2
        player[2]=0#0 right
    elif keys[K_LEFT]:
        player[0]-=2
        player[2]=3#3 left
    elif keys[K_UP]:
        player[1]-=2
        player[2]=2#2 up
    elif keys[K_DOWN]:
        player[1]+=2
        player[2]=1#1 down
    else:
        player[3]=0

    player[3]=player[3]+0.2
    if player[3]>=6:
        player[3]=1

        

     #x    y  row col
mario=[250,150,0 ,0]
       #0  1   2  3

pics=[]
pics.append(addPics("Mario",1,6))#right facing pics
pics.append(addPics("Mario",7,12))#down facing pics
pics.append(addPics("Mario",13,18))#up facing pics
pics.append(addPics("Mario",19,24))#leftdown facing pics


print(pics)


running=True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()

    drawScene(mario,pics)#pics is the 2D list with all 24 pictures
    movePlayer(mario)
    
    myClock.tick(60)
    
            
quit()
