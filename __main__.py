try:
    from tkinter import *
except:
    from Tkinter import *

import math
import time

root = Tk()

canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.configure(background='black')
canvas.pack()

class Game:
    def __init__(self):
        self.game = True

        self.time = time.time()
        self.delta_time = 0
        self.last_time = time.time()

        self.player = Player()

        self.keys = []

        self.mouse_x = 0
        self.mouse_y = 0

        self.enemy = Enemy(300,300)



    def key_press(self,event):
        self.keys.append(event.keysym)

    def key_release(self,event):
        while event.keysym in self.keys:
            self.keys.remove(event.keysym)

    def motion(self,event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def update(self):
        self.delta_time = time.time()-self.last_time
        self.last_time = time.time()

        canvas.delete(ALL)

        self.player.vel_x = 0
        self.player.vel_y = 0

        if 'w' in self.keys:
            self.player.vel_y = -150
        if 's' in self.keys:
            self.player.vel_y = 150
        if 'a' in self.keys:
            self.player.vel_x = -150
        if 'd' in self.keys:
            self.player.vel_x = 150

        #canvas.create_text(100,100,text='FPS: '+str(int(1/self.delta_time)),fill='white')


        self.player.update()

        self.enemy.update()

        root.update()

class Player:
    def __init__(self):
        self.x = root.winfo_screenwidth()/2
        self.y = root.winfo_screenheight()/2

        self.vel_x = 0
        self.vel_y = 0

        self.width = root.winfo_screenwidth()/43
        self.height = root.winfo_screenwidth()/17

        self.photo = PhotoImage(file='Astronaut.gif')

        if 45/self.width > 1:
            self.photo = self.photo.zoom(int(45/self.width),1)
        else:
            self.photo = self.photo.subsample(int(self.width/45),1)
        if 64/self.width > 1:
            self.photo = self.photo.zoom(1,int(64/self.width))
        else:
            self.photo = self.photo.subsample(1,int(self.width/64))

    def update(self):
        self.x += self.vel_x*game.delta_time
        self.y += self.vel_y*game.delta_time

        self.render()

    def render(self):
        canvas.create_image(self.x,self.y,anchor=CENTER,image=self.photo)
        #canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='white',outline='white')

        x = game.mouse_x
        y = game.mouse_y

        canvas.create_line(self.x,self.y,x,y,width=5,fill='white')

class Enemy:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.width = root.winfo_screenwidth()/20
        self.height = root.winfo_screenheight()/10

    def update(self):
        dist_x = game.player.x - self.x
        dist_y = game.player.y - self.y

        x = math.atan2(dist_x,dist_y)
        x = math.tan(x)*100

        dist_x = 100
        dist_y = x

        self.x += dist_x*game.delta_time
        self.y += dist_y*game.delta_time

        self.render()

    def render(self):
        canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='red',outline='red')

game = Game()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

root.bind('<Motion>',game.motion)

while game.game == True:
    try:
        game.update()
    except TclError:
        break
