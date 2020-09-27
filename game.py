import pygame as pg
import math

WIDTH = 600
HEIGHT = 600
running = True
currentScreen = "home"


# Test colors:
class Color:
    white = (255,255,255)
    grey = (127,127,127)
    red = (255,40,0)
    orange = (200,210,0)
    yellow = (205,125,0)
    green = (0,127,50)
    blue = (0,50,255)
    purple = (150,30,255)
    black = (0,0,0)

# The game
pg.init()
pg.font.init()
frame = pg.display.set_mode([WIDTH,HEIGHT])

mouseX = pg.mouse.get_pos()[0]
mouseY = pg.mouse.get_pos()[1]
mouseIsDown = pg.mouse.get_pressed()[0] == 1

pg.display.set_caption("PHCGolf")

def renderText(content,posX,posY,fontSize=20):
    font = pg.font.Font("./assets/fonts/Montserrat-Regular.ttf",fontSize)
    text = font.render(content,True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (posX,posY)
    frame.blit(text,textRect)


# Classes
class Ball:
    def __init__(self,x,y,r,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.color = color
    def show(self):
        pg.draw.circle(frame,self.color,(int(self.x),int(self.y)),int(self.r))
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        if self.x-self.r<=0 or self.x+self.r>=WIDTH:
            self.vx = -self.vx
        if self.y-self.r<=0 or self.y+self.r>=HEIGHT:
            self.vy = -self.vy
        self.vx/=1.05
        self.vy/=1.05
    def contactBlock(self,block):
        if (self.x+self.r+self.vx>block.x
        and self.x-self.r+self.vx<block.x+block.w
        and self.y+self.r>block.y
        and self.y<block.y+block.h):
            self.vx *= -1
        if (self.x+self.r>block.x
        and self.x<block.x+block.w
        and self.y+self.r+self.vy>block.y
        and self.y-self.r+self.vy<block.y+block.h):
            self.vy *= -1
            print("Contact!")
    def detectHole(self,hole):
        distance = math.sqrt((self.x-hole.x)**2+(self.y-hole.y)**2)
        if (distance<hole.r):
            return True
            # print("IN HOLE!")

class Hole:
    def __init__(self,x,y,r,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.color = color
    def show(self):
        pg.draw.circle(frame,self.color,(self.x,self.y),self.r)
    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Block:
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = w
        self.h = h
        self.color = color
    def show(self):
        pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h))
    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Button:
    def __init__(self,x,y,w,h,color,hoverColor,clickedColor,textColor,content,screen):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.hoverColor = hoverColor
        self.clickedColor = clickedColor
        self.textColor = Color.white
        self.currentColor = self.color
        self.content = content
        self.screen = screen
        self.visible = False
    def onDefault(self):
        self.currentColor = self.color
    def onHover(self):
        self.currentColor = self.hoverColor
    def onClick(self):
        global currentScreen
        self.currentColor = self.clickedColor
        currentScreen = self.screen
        for i in range(1,11):
            if (self.screen=="level"+str(i)):
                gameScreen.setLevel(i)
    def setVisibility(self,visible):
        self.visible = visible
    def show(self):
        self.setVisibility(True)
        if self.visible==True:
            pg.draw.rect(frame,self.currentColor,(self.x-self.w,self.y-self.h,self.w*2,self.h*2))
            renderText(self.content,self.x,self.y)
            if (mouseX>=self.x-self.w and mouseX<=self.x+self.w
            and mouseY>=self.y-self.h and mouseY<=self.y+self.h):
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONUP:
                        self.onClick()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        self.currentColor = self.clickedColor
                    else:
                        self.onHover()
                # if (mouseIsDown):
                #     self.onClick()
                # else:
                #     self.onHover()
            else:
                self.onDefault()

class GameScreen:
    def __init__(self):
        self.playBtn = Button(WIDTH/2,HEIGHT/2,100,25,Color.blue,Color.yellow,Color.white,Color.grey,"Start Game!","levels")
        self.backBtn = Button(100,HEIGHT/4,50,25,Color.blue,Color.yellow,Color.white,Color.grey,"Back","home")
        self.lvlNumBtns = []
        self.blocks = []
        for i in range(1,6):
            self.lvlNumBtns.append(Button(i*100,(HEIGHT/2),30,30,Color.blue,Color.yellow,Color.white,Color.grey,str(i),"level"+str(i)))
        for i in range(6,11):
            self.lvlNumBtns.append(Button((i-5)*100,(HEIGHT/2)+100,30,30,Color.blue,Color.yellow,Color.white,Color.grey,str(i),"level"+str(i)))
        self.player = Ball(50,HEIGHT/2,10,Color.white)
        self.hole = Hole(550,250,15,Color.black)
        self.strokes = 0
        self.par = 0
        self.currentLevel = 0
    def showHome(self):
        pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
        renderText("PHCGolf",WIDTH/2,HEIGHT/4,fontSize=40)
        renderText("By PixelHyperCube!",WIDTH/2,HEIGHT/3,fontSize=30)
        self.playBtn.show()
    def showLevelScreen(self):
        pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
        renderText("Choose a level!",WIDTH/2,HEIGHT/4)
        self.backBtn.show()
        for btn in self.lvlNumBtns:
            btn.show()
    def setLevel(self,num):
        self.strokes = 0
        if num==1:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(100,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==2:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==3:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==4:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==5:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==6:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==7:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==8:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==9:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        elif num==10:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,10,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.par = 3
        self.currentLevel = num
    def showLevel(self):
        global running
        global currentScreen
        pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
        self.hole.show()
        self.hole.update()
        for block in self.blocks:
            block.show()
            block.update()
            if (self.player.contactBlock(block)):
                print(True)
        self.player.show()
        self.player.update()
        if (self.player.detectHole(self.hole)):
            print("Scored!")
            currentScreen = "scored"
        if mouseIsDown:
            pg.draw.line(frame,Color.red,(self.player.x,self.player.y),(mouseX,mouseY))
        renderText("Par "+str(self.par),WIDTH-70,30,fontSize=30)
        renderText("Strokes: "+str(self.strokes),WIDTH-100,80,fontSize=30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONUP:
                self.strokes+=1
                distance = 0.05*math.sqrt((mouseX-self.player.x)**2+(mouseY-self.player.y)**2)
                angle = math.atan2(self.player.y-mouseY,self.player.x-mouseX)
                self.player.vx = distance*math.cos(angle)
                self.player.vy = distance*math.sin(angle)
    def showScored(self):
        pg.draw.rect(frame,Color.blue,(0,0,WIDTH,HEIGHT))
        renderText("SCORED!!!",WIDTH/2,HEIGHT/2,fontSize=40)
        Button(WIDTH/2,HEIGHT/1.6,100,30,Color.orange,Color.yellow,Color.green,Color.white,"Next Level!","level"+str(self.currentLevel+1)).show()
        Button(WIDTH/2,HEIGHT/1.3,100,30,Color.orange,Color.yellow,Color.green,Color.white,"Go back!","levels").show()

gameScreen = GameScreen()

clock = pg.time.Clock()

while running:
    clock.tick(60)
    mouseX = pg.mouse.get_pos()[0]
    mouseY = pg.mouse.get_pos()[1]
    mouseIsDown = pg.mouse.get_pressed()[0] == 1
    if (currentScreen=="home"):
        gameScreen.showHome()
    if (currentScreen=="levels"):
        gameScreen.showLevelScreen()
    if (currentScreen=="scored"):
        gameScreen.showScored()
    for i in range(1,11):
        if (currentScreen=="level"+str(i)):
            gameScreen.showLevel()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            print("mouse is down")
        elif event.type == pg.MOUSEBUTTONUP:
            print("mouse is up")
    pg.display.update()