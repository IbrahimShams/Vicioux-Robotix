from pygame import *
from math import *
from random import *

width,height=1150,697
screen=display.set_mode((width,height))
display.set_caption("Vicioux Robotix")
RED=(255,0,0)
GREY=(200,200,200)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True
lava_counter=0
block=image.load("block2.png").convert()
rect_list=[]
omx,omy=0,0
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
lava_background=Rect(0,597,1150,100)
nospawnregion=Rect(0,275,250,150)
robot_platforms=[Rect(randint(0,975),randint(0,405),175,20)]
jumpPower=-7
move_list=["no jump","right",0.07]
dJump,facing,img_speed=0,1,2
gravity=0.3
X,Y,W,H=0,1,2,3
timer,moved=0,False

v=[0,0,697]
p=Rect(0,400,75,75)
p_list=[0,0]
objects=[lava_background,p]

def flipPics(lst):
    flip_lst=[]
    for image in lst:
        flip_lst.append(transform.flip(image,True,False))
    return flip_lst

def addPics(name,start,end):
    mypics=[]
    for i in range(start,end):
        img=image.load(f"player/{name}{i:03}.png").convert_alpha()
        img=transform.scale(img,(75,75))
        mypics.append(img)
    return mypics

pics=[]
pics.append(addPics("tile",0,5)) #idle right
pics.append(flipPics(pics[0])) #idle left
pics.append(addPics("tile",24,31)) #walking right
pics.append(flipPics(pics[2])) #walking left
pics.append(addPics("tile",40,47)) #jumping right
pics.append(flipPics(pics[4])) #jumping left
pics.append(addPics("tile",64,71)) #attack right
pics.append(flipPics(pics[6])) #attack left

def drawScene():
    screen.fill(GREY)
    draw.rect(screen,RED,nospawnregion,1)
    draw.rect(screen,RED,p,1)
    for plat in robot_platforms:
        draw.rect(screen,RED,plat,1)
    for plat in rect_list:
        screen.blit(block,plat)
    row=p_list[0]
    col=int(p_list[1])
    pic=pics[row][col]
    screen.blit(pic,p)

def hitWalls(x,y,walls):
    playerRect=Rect(x,y,75,75)
    return playerRect.collidelist(walls)

def movePlayer(p,move_list):
    keys=key.get_pressed()
    v[X]=0
    move_list[img_speed]=0.07
    if move_list[facing]=="right":
        p_list[0]=0
    else:
        p_list[0]=1
    if keys[K_a] and hitWalls(p[X]-5,p[Y],rect_list)==-1:
        v[X]=-5
        move_list[facing]="left"
        if v[Y]==0:
            p_list[0]=3
            move_list[img_speed]=0.15
    if keys[K_d] and hitWalls(p[X]+5,p[Y],rect_list)==-1:
        v[X]=5
        move_list[facing]="right"
        if v[Y]==0:
            p_list[0]=2
            move_list[img_speed]=0.15
    if keys[K_w] and p[Y]+p[H]==v[2] and v[Y]==0:
        v[Y]=jumpPower
        move_list[dJump]="first jump"
    if not keys[K_w] and move_list[dJump]=="first jump":
        move_list[dJump]="double jump available"
    if move_list[dJump]=="double jump available" and keys[K_w]:
        v[Y]=jumpPower
        move_list[dJump]="no jump"
    if v[Y]<0:
        move_list[img_speed]=0.33
        if hitWalls(p[X],p[Y]+v[Y],rect_list)!=-1:
            v[Y]=-gravity
        if move_list[facing]=="right":
            p_list[0]=4
        else:
            p_list[0]=5
    if keys[K_LSHIFT]:
        move_list[img_speed]=0.2
        if move_list[facing]=="right":
            p_list[0]=6
        else:
            p_list[0]=7

    p_list[1]=(p_list[1]+move_list[img_speed])%len(pics[p_list[0]])

    p[X]+=v[X]
    if v[Y]<=100:
        v[Y]+=gravity

def check(p):
    global timer
    for plat in rect_list:
        if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
            v[Y]=0
            v[2]=plat[Y]
            p[Y]=plat[Y]-p[H]
    if not moved:
        if timer<180:
            timer+=1
            v[Y]=0
    else:
        p[Y]+=int(v[Y])

for img in lavaImgs:
    img.set_colorkey(BLACK)

def roundIt(num,round_num):
    n=0
    for i in range(0,num+1,round_num):
        if i+round_num>num:
            n=i
    return n

def gaps(x1,y1,x2,y2,map,action):
    gap=[]
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
            if gapfillRect not in map:
                gap.append(gapfillRect)
        return gap
    elif action=="erase":
        for i in range(num_squares):
            dotX=omx+dx_increase*i
            dotY=omy+dy_increase*i
            gaperaseRect=Rect(roundIt(int(dotX),50),roundIt(int(dotY),50),50,50)
            if gaperaseRect in rect_list:
                rect_list.remove(gaperaseRect)
        return map

def cleanMap(map):
    for block in map:
        if block.collidelist(objects)!=-1:
            map.remove(block)

def drawMap(x1,y1,x2,y2,map):
    if abs(x1-x2)>50 or abs(y1-y2)>50:
        for block in gaps(x1,y1,x2,y2,map,"fill"):
            map.append(block)
    else:
        drawRect=Rect(x2,y2,50,50)
        if drawRect not in map:
            map.append(drawRect)
    cleanMap(map)

def eraseMap(x1,y1,x2,y2,map):
    if abs(x1-x2)>50 or abs(y1-y2)>50:
        map=gaps(x1,y1,x2,y2,map,"erase")
    else:
        eraseRect=Rect(x2,y2,50,50)
        if eraseRect in map:
            map.remove(eraseRect)

def animate(lst,counter,speed,x,y):
    screen.blit(lst[int(counter)],(x,y))
    return (counter+speed)%len(lst)

while running:
    if nospawnregion.colliderect(robot_platforms[0]):
        robot_platforms[0]=Rect(randint(0,975),randint(0,405),175,20)
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key==K_w or evt.key==K_LSHIFT:
                p_list[1]=0
            if evt.key==K_w or evt.key==K_a or evt.key==K_d:
                moved=True
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    
    if mb[0]:
        drawMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list)
    
    elif mb[2]:
        eraseMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list)
    
    drawScene()
    draw.rect(screen,(220,70,40),lava_background)
    lava_counter=animate(lavaImgs,lava_counter,0.1,0,580)
    movePlayer(p,move_list)
    check(p)
    print(len(rect_list))
    myClock.tick(60)
    display.update()
    omx,omy=mx,my
quit()
