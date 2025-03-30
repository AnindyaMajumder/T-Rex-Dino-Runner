from OpenGL.GL import *
from shapes.circle import Circle
from shapes.line import Line
from shapes.dinosaur import Dinosaur

def drawRotatingRectangle(x, y, width, height, angle):
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)

    glTranslatef(x, y, 0)
    glRotatef(angle, 0, 0, 1)

    half_width = width / 2
    half_height = height / 2

    glBegin(GL_QUADS)
    glVertex2f(-half_width, -half_height)
    glVertex2f(half_width, -half_height)
    glVertex2f(half_width, half_height)
    glVertex2f(-half_width, half_height)
    glEnd()

    glPopMatrix()

def outdoorScene(is_day, stars):
    if is_day:
        glColor3f(0.529, 0.808, 0.922)  # Light blue for daytime
    else:
        glColor3f(0.0, 0.0, 0.2)  # Dark blue for nighttime
        
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 500)
    glVertex2f(0, 500)
    glEnd()

    # Ground
    glColor3f(0.133, 0.545, 0.133)  # Green for grass
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 100)
    glVertex2f(0, 100)
    glEnd()

    # Sun or Moon
    if is_day:
        glColor3f(1.0, 0.843, 0.0)  # Yellow for the sun
    else:
        glColor3f(1.0, 1.0, 1.0)  # White for the moon
    for i in range(1,40):
        Circle.circles(i,100,450)
        
    # Clouds (daytime only)
    if is_day:
        glColor3f(1.0, 1.0, 1.0)  # White for clouds
        Circle.circles(20, 200, 400)
        Circle.circles(30, 230, 420)
        Circle.circles(20, 260, 400)

        Circle.circles(20, 500, 450)
        Circle.circles(30, 530, 470)
        Circle.circles(20, 560, 450)

    # Stars (nighttime only)
    if not is_day:
        glColor3f(1.0, 1.0, 1.0)  # White for stars
        for x, y in stars:
            Line.WritePixel(x, y)

def keyboard(key, x, y, dinosaur, is_day, pause):
    if key == b' ':
        dinosaur.jump_press()
    if key == b"d":
        is_day = not is_day
    if key == b"\x1b":
        pause = not pause
    return is_day, pause

def keyboardUp(key, x, y, dinosaur):
    if key == b' ':
        dinosaur.jump_release()

def iterate(is_day):
    glViewport(0, 0, 800, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if is_day:
        glClearColor(.8, 0.8, .8, 2)
    else:
        glClearColor(0, 0, 0, 1)
    glOrtho(0.0, 800, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()