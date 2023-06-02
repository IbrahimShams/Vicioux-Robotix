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
rect_list=[Rect(0,450,50,50)]
omx,omy=0,0
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
lava_background=Rect(0,667,1150,30)
# gravity=3
# jumpPower=-45

# X,Y,W,H=0,1,2,3

# def drawScene():
#     screen.fill(WHITE)
#     draw.rect(screen,RED,p)
#     for plat in rect_list:
#         screen.blit(block,plat)
#     display.flip()

# def movePlayer(p):
#     keys=key.get_pressed()
#     if keys[K_SPACE] and p[Y]+p[H]==v[2] and v[Y]==0:
#         v[Y]=jumpPower

#     v[X]=0
#     if keys[K_LEFT]:
#         v[X]=-10
#     elif keys[K_RIGHT]:
#         v[X]=10
  
#     p[X]+=v[X] #horizontal movement
#     v[Y]+=gravity

# def check(p):
#     #we will first check if the player lands on
#     #one of the platforms
#     for plat in rect_list:
#                                                         #   current position         next frame position
#         if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
#             v[Y]=0#stop falling down
#             v[2]=plat[Y]
#             p[Y]=plat[Y]-p[H]

#     p[Y]+=v[Y]#vertical movement

#     # if p[Y]+p[H]>=600:
#     #     v[Y]=0
#     #     p[Y]=600-p[H]
#     #     v[2]=600

# #hor ver height
# v=[0,0, 600]

# p=Rect(0,250,50,50)

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
        if eraseRect in map:
            map.remove(eraseRect)

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
    
    # drawScene()
    draw.rect(screen,(220,70,40),lava_background)
    lava_counter=animate(lavaImgs,lava_counter,0.1,0,580)
    for rect in rect_list:
         screen.blit(block,rect)
    # movePlayer(p)
    # check(p)
    #print(len(rect_list))
    myClock.tick(60)
    display.flip()
    omx,omy=mx,my
quit()
