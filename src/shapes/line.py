from OpenGL.GL import *
import random

class Line:
    @staticmethod
    def WritePixel(x, y):
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    @staticmethod
    def plot(x1, y1, x2, y2):
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    @staticmethod
    def stars():
        glPointSize(3)
        glBegin(GL_POINTS)
        for _ in range(50):
            glVertex2f(random.randint(0, 800), random.randint(300, 400))
        glEnd()