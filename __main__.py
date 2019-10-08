try:
    from tkinter import *
except:
    from Tkinter import *

import math
import time
import random

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
        self.mouse_press = False

        self.list = []
        self.wave = Enemy(300,300,5,self.list,2)
        self.list.append(self.wave)

    def key_press(self,event):
        self.keys.append(event.keysym)

    def key_release(self,event):
        while event.keysym in self.keys:
            self.keys.remove(event.keysym)

    def motion(self,event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def click(self,event):
        self.mouse_press = True

    def un_click(self,event):
        self.mouse_press = False

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
        if self.wave:
            self.wave.update()
            #x = (root.winfo_screenwidth()/4)+(root.winfo_screenwidth()/2*(len(self.wave.enemies)/float(self.wave.size)))
            #self.progress_bar(root.winfo_screenwidth()/4,root.winfo_screenheight()/30*2,x,root.winfo_screenwidth()/4*3,root.winfo_screenheight()/60)
            #canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/30,anchor=CENTER,text='Wave',fill='white',font=('TkTextFont',25))

        self.player.update()

        root.update()

    def progress_bar(self,x,y,x2,x3,height):
        height = int(height)
        if not height%2 == 0:
            height += 1
        canvas.create_oval(x-height-1,y-height-1,x+height-1,y+height-1,fill='white')
        canvas.create_oval(x3-height-1,y-height-1,x3+height-1,y+height-1,fill='white')
        canvas.create_line(x,y,x3,y,fill='white',width=height*2)
        if not x == x2:
            canvas.create_oval(x-(height/2-1)-1,y-(height/2-1)-1,x+(height/2-1)-1,y+(height/2-1)-1,fill='red',outline='red')
            canvas.create_oval(x2-(height/2-1)-1,y-(height/2-1)-1,x2+(height/2-1)-1,y+(height/2-1)-1,fill='red',outline='red')
        canvas.create_line(x,y,x2,y,fill='red',width=height)

class Player:
    def __init__(self):
        self.x = root.winfo_screenwidth()/2
        self.y = root.winfo_screenheight()/2

        self.vel_x = 0
        self.vel_y = 0

        self.dead = False

        self.width = root.winfo_screenwidth()/43
        self.height = root.winfo_screenwidth()/60

        self.photo = PhotoImage(file='Astronaut.gif')

        self.laser = False
        self.laser_time = 0

        if self.width/45 > 1:
            self.photo = self.photo.zoom(int(self.width/45),1)
        else:
            self.photo = self.photo.subsample(int(45/self.width),1)
        if self.width/64 > 1:
            self.photo = self.photo.zoom(1,int(self.width/64))
        else:
            self.photo = self.photo.subsample(1,int(64/self.width))

    def update(self):
        if self.dead == False:
            self.x += self.vel_x*game.delta_time
            self.y += self.vel_y*game.delta_time

        if game.mouse_press and not self.laser:
            self.laser = True
            self.laser_time = time.time()

        if self.laser:
            if time.time()-self.laser_time > .5:
                self.laser = False

        self.render()

    def render(self):
        canvas.create_image(self.x,self.y,anchor=CENTER,image=self.photo)
        #canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='white',outline='white')

        x = game.mouse_x
        y = game.mouse_y

        if self.laser:
            fill = 'green'
        else:
            fill = 'white'

        canvas.create_line(self.x,self.y,x,y,width=5,fill=fill)

class Enemy:
    def __init__(self,x,y,speed,wave,type):
        self.x = x
        self.y = y

        self.type = type

        self.speed = speed

        self.width = root.winfo_screenwidth()/100
        self.height = root.winfo_screenwidth()/60

        self.photo = PhotoImage(file='Alien.gif')

        if self.width/19 > 1:
            self.photo = self.photo.zoom(int(self.width/19),1)
        else:
            self.photo = self.photo.subsample(int(19/self.width),1)
        if self.width/33 > 1:
            self.photo = self.photo.zoom(1,int(self.width/33))
        else:
            self.photo = self.photo.subsample(1,int(33/self.width))

        self.wave = wave

        if self.type == 2:
            self.laser_available = False
            self.laser_time = time.time()
            self.laser = None

    def update(self):
        dist_x = game.player.x - self.x
        dist_y = game.player.y - self.y

        if abs(dist_x) > game.player.width/2+self.width/2 or abs(dist_y) > game.player.height/2+self.height/2:
            if game.player.laser:
                if game.mouse_x > self.x - self.width/2 and game.mouse_x < self.x + self.width/2 and game.mouse_y > self.y - self.height/2 and game.mouse_y < self.y + self.height/2:
                    game.player.laser = False
                    game.mouse_press = False
                    self.wave.enemies.remove(self)

            a = math.atan2((dist_y),(dist_x))

            x = math.cos(a)
            y = math.sin(a)

            dist_x = x*self.speed
            dist_y = y*self.speed

            if self.type == 1:
                self.x += dist_x*game.delta_time
                self.y += dist_y*game.delta_time

            if self.type == 2:
                if self.laser_available == True:
                    self.laser = Laser(self.x,self.y,x,y,8,self)
                    self.laser_available = False

                print(time.time()-self.laser_time)

                if self.laser_available == False and self.laser == None and time.time() - self.laser_time > 5:
                    self.laser_available = True

                if self.laser:
                    self.laser.update()

        else:
            game.player.dead = True


        self.render()

    def render(self):
        canvas.create_image(self.x,self.y,anchor=CENTER,image=self.photo)
        #canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='red',outline='red')

class Laser:
    def __init__(self,x,y,x_move,y_move,speed,enemy):
        self.x = x
        self.y = y

        self.last_x = x
        self.last_y = y

        self.even_laster_x = x
        self.even_laster_y = y

        self.speed_x = x_move*speed
        self.speed_y = y_move*speed

        self.enemy = enemy


    def update(self):
        self.even_laster_x = self.last_x
        self.even_laster_y = self.last_y

        self.last_x = self.x
        self.last_y = self.y

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x > game.player.x-game.player.width/2 and self.x < game.player.x+game.player.width/2 and self.y > game.player.y-game.player.height/2 and self.y > game.player.y-game.player.height/2:
            game.player.dead = True
            self.enemy.laser = None
            self.enemy.laser_time = time.time()

        if abs(self.enemy.x - self.x) > root.winfo_screenwidth() or abs(self.enemy.y - self.y) > root.winfo_screenheight():
            game.player.dead = True
            self.enemy.laser = None
            self.enemy.laser_time = time.time()

        self.render()

    def render(self):
        canvas.create_line(self.x,self.y,self.even_laster_x,self.even_laster_y,fill = 'green',width=4)

class Wave:
    def __init__(self,size,level):
        self.size = size

        self.level

        self.enemies = []
        for i in range(size):
            type = random.randint(1,self.level)
            side = random.randint(1,4)
            if side == 1:
                x = random.randint(0,root.winfo_screenwidth())
                y = 0
            elif side == 2:
                x = root.winfo_screenwidth()
                y = random.randint(0,root.winfo_screenheight())
            elif side == 3:
                x = random.randint(0,root.winfo_screenwidth())
                y = root.winfo_screenheight()
            else:
                x = 0
                y = random.randint(0,root.winfo_screenheight())
            self.enemies.append(Enemy(x,y,50,self,type))

    def update(self):
        for i in self.enemies:
            i.update()

game = Game()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

root.bind('<Motion>',game.motion)
root.bind('<Button-1>',game.click)
root.bind('<ButtonRelease-1>',game.un_click)

while game.game == True:
    try:
        game.update()
    except TclError:
        break
