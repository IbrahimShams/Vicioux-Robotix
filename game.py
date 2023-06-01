from pygame import *
from math import *

width,height=1150,697
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True
lava_counter=0
block=image.load("block1.png")
rect_list=[]
omx,omy=0,0
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
player=image.load("player/tile000.png")
player=transform.scale(player, (100,100))
"""Idle (2 frames)
Blink (variation to idle, 2 frames)
Walk (4 frames)
Run (8 frames)
Kneel/Duck (6 frames)
Jump (8 frames)
Teleport/disappear (4 frames)
Die (8 frames)
Attack (8 frames)
To Do:
- idle + blink
- jump
- run
- attack
"""
# def addPics(name,start,end):
#     mypics=[]
#     for i in range(start,end+1):
#         mypics.append(image.load(f"images/{name}{i:03}.png"))
#     return mypics

# def drawScene(player,picList):
#     screen.fill(WHITE)
#     row=player[2]
#     col=int(player[3])
#     pic=picList[row][col]
#     screen.blit(pic,(player[0],player[1]))
#     display.flip()

# def movePlayer(player):
#     '''
#     this function changes the x and y location of the player
#     It also adjusts the ROW and the COLUMN values in the list
#     so that we can show the correct picture
#     '''
#     if keys[K_RIGHT]:
#         player[0]+=2
#         player[2]=0#0 right
#     elif keys[K_LEFT]:
#         player[0]-=2
#         player[2]=3#3 left
#     elif keys[K_UP]:
#         player[1]-=2
#         player[2]=2#2 up
#     elif keys[K_DOWN]:
#         player[1]+=2
#         player[2]=1#1 down
#     else:
#         player[3]=0

#     player[3]=player[3]+0.2
#     if player[3]>=6:
#         player[3]=1

     #x    y  row col
# mc=[250,150,0 ,0]

# pics=[]
# pics.append(addPics("Mario",1,6))#right facing pics
# pics.append(addPics("Mario",7,12))#down facing pics
# pics.append(addPics("Mario",13,18))#up facing pics
# pics.append(addPics("Mario",19,24))#leftdown facing pics
# mario=[250,150,0 ,0]

# print(pics)

for img in lavaImgs:
    img.set_colorkey(BLACK)

def roundIt(num,round_num):
    n=0
    for i in range(0,num+1,round_num):
        if i+round_num>num:
            n=i
    return n

def gaps(x1,y1,x2,y2,lst,action):
    dst=sqrt((x2-x1)**2+(y2-y1)**2)
    dx,dy=x2-x1,y2-y1
    if abs(dx)>=abs(dy):
        side=dy/dx*50
    elif abs(dx)<abs(dy):
        side=dx/dy*50
    hypot=sqrt(50**2+side**2)
    num_squares=int(dst/hypot)
    dx_increase,dy_increase=dx/num_squares,dy/num_squares
    dotX,dotY=omx,omy
    if action=="fill":
        for i in range(num_squares):
            dotX+=dx_increase
            dotY+=dy_increase
            gapfillRect=Rect(roundIt(int(dotX),50),roundIt(int(dotY),50),50,50)
            if gapfillRect not in lst:
                lst.append(gapfillRect)
    elif action=="erase":
        for i in range(num_squares):
            dotX=omx+dx_increase*i
            dotY=omy+dy_increase*i
            gaperaseRect=Rect(roundIt(int(dotX),50),roundIt(int(dotY),50),50,50)
            if gaperaseRect in rect_list:
                rect_list.remove(gaperaseRect)
    return lst

def drawMap(x1,y1,x2,y2,map):
    if y2<600 and y1<600:
        if abs(x1-x2)>50 or abs(y1-y2)>50:
            map=gaps(x1,y1,x2,y2,map,"fill")
        else:
            drawRect=Rect(x2,y2,50,50)
            if drawRect not in map:
                map.append(drawRect)

def eraseMap(x1,y1,x2,y2,map):
    if abs(x1-x2)>50 or abs(y1-y2)>50:
        map=gaps(x1,y1,x2,y2,map,"erase")
    else:
        eraseRect=Rect(x2,y2,50,50)
        if eraseRect in rect_list:
            rect_list.remove(eraseRect)

def animate(lst,counter,speed,x,y):
    screen.blit(lst[int(counter)],(x,y))
    counter=(counter+speed)%len(lst)
    return counter

while running:
    screen.fill(WHITE)
    for evt in event.get():
        if evt.type==QUIT:
            running=False

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    if mb[0]:
        drawMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list)
    elif mb[2]:
        eraseMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list)

    for rect in rect_list:
        screen.blit(block,rect)
    
    # drawScene(mc,pics)#pics is the 2D list with all 24 pictures
    # movePlayer(mc)

    screen.blit(player,(0,0))

    draw.rect(screen,(220,70,40),(0,667,1150,30))
    lava_counter=animate(lavaImgs,lava_counter,0.1,0,580)
    print(len(rect_list))
    myClock.tick(60)
    display.flip()
    omx,omy=mx,my
quit()
