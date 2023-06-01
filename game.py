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
counter=0
block=image.load("block1.png")
rect_list=[]
omx,omy=0,0
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert_alpha() for i in range(6)]
playerImgs=[image.load(f"player/player ({i+1}).png") for i in range(21)]
for img in lavaImgs:
    img.set_colorkey(BLACK)

player=image.load("player/player (1).png")
player=transform.scale(player,(300,300))
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

def animate(lst,counter,x,y):
    screen.blit(lst[int(counter)],(x,y))
    counter=(counter+0.1)%len(lst)
    return counter

while running:
    screen.fill(WHITE)
    screen.blit(player,(0,0))

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
    
    draw.rect(screen,(220,70,40),(0,667,1150,30))
    counter=animate(lavaImgs,counter,0,580)
    print(len(rect_list))
    myClock.tick(60)
    display.flip()
    omx,omy=mx,my
quit()
