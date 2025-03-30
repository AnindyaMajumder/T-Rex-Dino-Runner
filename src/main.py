from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shapes.dinosaur import Dinosaur
from shapes.moving_obstacles import MovingObstacles  # Updated import
from utils.utils import drawRotatingRectangle, outdoorScene, keyboard, keyboardUp, iterate

import random

moving_obstacles = MovingObstacles()  # Updated class name
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
        moving_obstacles.update()  # Updated variable name
        dinosaur.update()
    dinosaur.draw()
    displayPoint()
    moving_obstacles.draw()  # Updated variable name

    glutSwapBuffers()

def displayPoint():
    """Display the score on the screen."""
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(600, 450)  # Position for the score display
    score_text = f"Score: {moving_obstacles.num_triangles_touched}"  # Updated variable name
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def keyboardHandler(key, x, y):
    global is_day, pause
    is_day, pause = keyboard(key, x, y, dinosaur, is_day, pause)

def keyboardUpHandler(key, x, y):
    keyboardUp(key, x, y, dinosaur)

# OpenGL initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500)  # window size
glutInitWindowPosition(250, 150)
wind = glutCreateWindow(b"Dinosaur Jump Game")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardHandler)
glutKeyboardUpFunc(keyboardUpHandler)  # Add key release handler
glutIdleFunc(showScreen)
glutMainLoop()