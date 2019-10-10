try:
    from tkinter import *
except:
    from Tkinter import *

import math
import time
import random

root = Tk()
root.config(cursor='none')

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

        self.wave = Wave(40,2)


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
            x = (root.winfo_screenwidth()/4)+(root.winfo_screenwidth()/2*(len(self.wave.enemies)/float(self.wave.size)))
            self.progress_bar(root.winfo_screenwidth()/4,root.winfo_screenheight()/30*2,x,root.winfo_screenwidth()/4*3,root.winfo_screenheight()/60)
            canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/30,anchor=CENTER,text='Wave',fill='white',font=('TkTextFont',25))

        self.player.update()

        dist_x = self.mouse_x-game.player.x
        dist_y = self.mouse_y-game.player.y

        if math.sqrt(abs(dist_x)**2+abs(dist_y)**2) > root.winfo_screenwidth()/4:
            a = math.atan2(dist_y,dist_x)

            x = math.cos(a)
            y = math.sin(a)

            x_pos = self.player.x
            y_pos = self.player.y
            while math.sqrt(abs(self.player.x-x_pos)**2+abs(self.player.y-y_pos)**2) < root.winfo_screenwidth()/4:
                x_pos += x
                y_pos += y

        else:
            x_pos = self.mouse_x
            y_pos = self.mouse_y

        self.crosshair(x_pos,y_pos)

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

    def crosshair(self,x,y):
        canvas.create_line(x-5,y-5,x-20,y-5,fill='white',width=5)
        canvas.create_line(x-5,y-5,x-5,y-20,fill='white',width=5)
        canvas.create_line(x-5,y+5,x-20,y+5,fill='white',width=5)
        canvas.create_line(x-5,y+5,x-5,y+20,fill='white',width=5)
        canvas.create_line(x+5,y-5,x+20,y-5,fill='white',width=5)
        canvas.create_line(x+5,y-5,x+5,y-20,fill='white',width=5)
        canvas.create_line(x+5,y+5,x+20,y+5,fill='white',width=5)
        canvas.create_line(x+5,y+5,x+5,y+20,fill='white',width=5)

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

        self.lasers = []

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

        if game.mouse_press:
            if len(self.lasers) < 10:
                x = game.mouse_x-self.x
                y = game.mouse_y-self.y

                a = math.atan2(y,x)

                x = math.cos(a)
                y = math.sin(a)

                self.lasers.append(Player_Laser(self.x,self.y,x,y,3))

                game.mouse_press = False

        for i in self.lasers:
            i.update()

        self.render()

    def render(self):
        canvas.create_image(self.x,self.y,anchor=CENTER,image=self.photo)

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
            self.laser_time = time.time()-random.randint(0,300)/float(100)
            self.laser = None

    def update(self):
        dist_x = game.player.x - self.x
        dist_y = game.player.y - self.y

        if abs(dist_x) > game.player.width/2+self.width/2 or abs(dist_y) > game.player.height/2+self.height/2:

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
                    self.laser = Enemy_Laser(self.x,self.y,x,y,3,self)
                    self.laser_available = False

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

class Enemy_Laser:
    def __init__(self,x,y,x_move,y_move,speed,enemy):
        self.x = x
        self.y = y

        self.speed_x = x_move*speed
        self.speed_y = y_move*speed

        self.enemy = enemy

        self.x += self.speed_x*15
        self.y += self.speed_y*15

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x > game.player.x-game.player.width/2 and self.x < game.player.x+game.player.width/2 and self.y > game.player.y-game.player.height/2 and self.y < game.player.y+game.player.height/2:
            game.player.dead = True
            self.enemy.laser = None
            self.enemy.laser_time = time.time()

        if abs(self.enemy.x - self.x) > root.winfo_screenwidth() or abs(self.enemy.y - self.y) > root.winfo_screenheight():
            self.enemy.laser = None
            self.enemy.laser_time = time.time()

        self.render()

    def render(self):
        canvas.create_line(self.x,self.y,self.x-self.speed_x*15,self.y-self.speed_y*15,fill = 'green',width=4)

class Player_Laser:
    def __init__(self,x,y,x_move,y_move,speed):
        self.x = x
        self.y = y

        self.speed_x = x_move*speed
        self.speed_y = y_move*speed

        self.x += self.speed_x*15
        self.y += self.speed_y*15


    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        for i in game.wave.enemies:
            if self.x > i.x-i.width/2 and self.x < i.x+i.width/2 and self.y > i.y-i.height/2 and self.y < i.y+i.height/2:
                game.wave.enemies.remove(i)
                game.player.lasers.remove(self)
                break

        if abs(game.player.x - self.x) > root.winfo_screenwidth() or abs(game.player.y - self.y) > root.winfo_screenheight():
            game.player.lasers.remove(self)

        self.render()

    def render(self):
        canvas.create_line(self.x,self.y,self.x-self.speed_x*15,self.y-self.speed_y*15,fill = 'green',width=4)

class Wave:
    def __init__(self,size,level):
        self.size = size

        self.level = level

        self.enemies = []
        for i in range(size):
            type = random.randint(1,self.level*5)
            if type > 1:
                type = 1
            else:
                type = 2

            side = random.randint(1,4)
            if side == 1:
                x = random.randint(0,root.winfo_screenwidth())
                y = 100*(type-1)
            elif side == 2:
                x = root.winfo_screenwidth()-100*(type-1)
                y = random.randint(0,root.winfo_screenheight())
            elif side == 3:
                x = random.randint(0,root.winfo_screenwidth())
                y = root.winfo_screenheight()-100*(type-1)
            else:
                x = 100*(type-1)
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
