from OpenGL.GL import *
from .circle import Circle
from .line import Line

class Dinosaur:
    def __init__(self):
        self.x = 150
        self.y = 200
        self.jump_height = 130
        self.jump_time = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_time = 0

    def update(self):
        if self.jumping:
            self.jump_time += 1
            if self.jump_time <= self.jump_height:
                self.y += 1
            else:
                self.y -= 1
                if self.y <= 200:
                    self.y = 200
                    self.jumping = False

    def draw(self):
        glColor3f(.2, .5, .9)
        for i in range(1, 26):
            Circle.circles(i, self.x, self.y)
        Line.plot(self.x - 20, self.y + 10, self.x - 40, self.y - 40)
        Line.plot(self.x - 90, self.y - 40, self.x - 40, self.y - 40)
        Line.plot(self.x + 20, self.y - 20, self.x, self.y - 70)
        Line.plot(self.x - 70, self.y - 70, self.x, self.y - 70)
        Line.plot(self.x - 110, self.y - 30, self.x - 70, self.y - 70)
        Line.plot(self.x - 50, self.y - 70, self.x - 50, self.y - 100)
        Line.plot(self.x - 60, self.y - 100, self.x - 20, self.y - 100)
        Line.plot(self.x - 30, self.y - 70, self.x - 30, self.y - 100)