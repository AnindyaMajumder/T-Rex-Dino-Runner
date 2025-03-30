from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shapes.dinosaur import Dinosaur
from shapes.moving_triangles import MovingTriangles
from utils.utils import drawRotatingRectangle, outdoorScene, keyboard, iterate

import random

moving_triangles = MovingTriangles()
dinosaur = Dinosaur()
is_day = False
stars = [(random.uniform(0, 800), random.uniform(800, 300)) for _ in range(200)]
pause = False

def showScreen():
    global pause, is_day
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate(is_day)

    outdoorScene(is_day, stars)
    if not pause:
        moving_triangles.update()
        dinosaur.update()
    dinosaur.draw()
    displayPoint()
    moving_triangles.draw()

    glutSwapBuffers()

def displayPoint():
    """Display the score on the screen."""
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(600, 450)  # Position for the score display
    score_text = f"Score: {moving_triangles.num_triangles_touched}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def keyboardHandler(key, x, y):
    global is_day, pause
    is_day, pause = keyboard(key, x, y, dinosaur, is_day, pause)

# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500)  # window size
glutInitWindowPosition(250, 150)
wind = glutCreateWindow(b"Dinosaur Jump Game")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardHandler)
glutIdleFunc(showScreen)
glutMainLoop()