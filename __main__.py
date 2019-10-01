try:
    from tkinter import *
except:
    from Tkinter import *

root = Tk()

canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.configure(background='black')
canvas.pack()

class Game:
    def __init__(self):
        self.game = True

        self.player = Player()

        self.keys = []

        self.enemy = Enemy(300,300)

    def key_press(self,event):
        self.keys.append(event.keysym)

    def key_release(self,event):
        while event.keysym in self.keys:
            self.keys.remove(event.keysym)

    def update(self):
        canvas.delete(ALL)

        if 'w' in self.keys:
            self.player.vel_y = -1
        if 's' in self.keys:
            self.player.vel_y = 1
        if 'a' in self.keys:
            self.player.vel_x = -1
        if 'd' in self.keys:
            self.player.vel_x = 1


        self.player.update()

        self.enemy.update()

        root.update()

class Player:
    def __init__(self):
        self.x = root.winfo_screenwidth()/2
        self.y = root.winfo_screenheight()/2

        self.vel_x = 0
        self.vel_y = 0

        self.width = root.winfo_screenwidth()/20
        self.height = root.winfo_screenheight()/10

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.render()

    def render(self):
        canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='white',outline='white')

class Enemy:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.width = root.winfo_screenwidth()/20
        self.height = root.winfo_screenheight()/10

    def update(self):
        dist_x = 0#self.x - game.player.x
        dist_x /= 10
        dist_y = 0#self.y - game.player.y
        dist_y /= 10

        self.x += dist_x
        self.y += dist_y

        self.render()

    def render(self):
        canvas.create_rectangle(self.x+self.width/2,self.y+self.height/2,self.x-self.width/2,self.y-self.height/2,fill='red',outline='red')

game = Game()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.game == True:
    game.update()
