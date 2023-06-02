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

gravity=3
jumpPower=-45

X=0
Y=1
W=2
H=3

def drawScene(p,plats):
    screen.fill(BLACK)
    draw.rect(screen,RED,p)
    for plat in plats:
        draw.rect(screen,GREEN,plat)
    display.flip()

def move(p):
    keys=key.get_pressed()

    if keys[K_SPACE] and p[Y]+p[H]==v[2] and v[Y]==0:
        v[Y]=jumpPower

    v[X]=0
    if keys[K_LEFT]:
        v[X]=-5
    elif keys[K_RIGHT]:
        v[X]=5
  
    p[X]+=v[X] #horizontal movement
    v[Y]+=gravity

def check(p,plats):
    '''
    check(p) - checks if the player is touching the ground
    or lands on a platform
    '''

    #we will first check if the player lands on
    #one of the platforms
    for plat in plats:
                                                        #   current position         next frame position
        if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
            v[Y]=0#stop falling down
            v[2]=plat[Y]
            p[Y]=plat[Y]-p[H]

    p[Y]+=v[Y]#vertical movement

    if p[Y]+p[H]>=600:
        v[Y]=0
        p[Y]=600-p[H]
        v[2]=600

 
        
    

#hor ver height
v=[0,0, 600]

myClock=time.Clock()
running=True
    #   X  Y  W  H
p=Rect(300,60,40,70)
    #   0  1  2  3

plats=[Rect(500,480,70,20),Rect(600,460,70,20),Rect(200,470,50,10)]

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False

    drawScene(p,plats)
    move(p)
    check(p,plats)
    print(v)
    myClock.tick(60)
quit()