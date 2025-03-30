from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random
import time

class Line:
    @staticmethod
    def FindZone(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        zone = -1

        if abs(dx) > abs(dy):
            if dx > 0 and dy > 0:
                zone = 0
            elif dx < 0 and dy > 0:
                zone = 3
            elif dx < 0 and dy < 0:
                zone = 4
            else:
                zone = 7
        else:
            if dx > 0 and dy > 0:
                zone = 1
            elif dx < 0 and dy > 0:
                zone = 2
            elif dx < 0 and dy < 0:
                zone = 5
            else:
                zone = 6

        return zone

    @staticmethod
    def zone0_conversion(zone, x, y):
        if zone == 0:
            return x, y
        elif zone == 1:
            return y, x
        elif zone == 2:
            return -y, x
        elif zone == 3:
            return -x, y
        elif zone == 4:
            return -x, -y
        elif zone == 5:
            return -y, -x
        elif zone == 6:
            return -y, x
        elif zone == 7:
            return x, -y

    @staticmethod
    def zone_original_conversion(zone, x, y):
        if zone == 0:
            return x, y
        if zone == 1:
            return y, x
        if zone == 2:
            return -y, -x
        if zone == 3:
            return -x, y
        if zone == 4:
            return -x, -y
        if zone == 5:
            return -y, -x
        if zone == 6:
            return y, -x
        if zone == 7:
            return x, -y

    @staticmethod
    def DrawLine(zone, x1, y1, x2, y2):  # MidPoint Line drawing algorithm
        dx = x2 - x1
        dy = y2 - y1
        d = 2 * dy - dx
        incE = 2 * dy
        incNE = 2 * (dy - dx)

        x = x1
        y = y1

        while x <= x2:
            a, b = Line.zone_original_conversion(zone, x, y)
            Line.WritePixel(a, b)

            if d > 0:
                d = d + incNE
                x += 1
                y += 1
            else:
                d = d + incE
                x += 1

    @staticmethod
    def plot(x1, y1, x2, y2):
        zone = Line.FindZone(x1, y1, x2, y2)
        a, b = Line.zone0_conversion(zone, x1, y1)
        c, d = Line.zone0_conversion(zone, x2, y2)
        Line.DrawLine(zone, a, b, c, d)

    @staticmethod
    def WritePixel(x, y):
        glPointSize(3)  # pixel size. by default 1 thake
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    @staticmethod
    def stars():
        glPointSize(3)  # pixel size. by default 1 thake
        glBegin(GL_POINTS)

        for i in range(50):
            glVertex2f(random.randint(0, 800), random.randint(300, 400))  # (x,y)

        glEnd()

class Circle:
    @staticmethod
    def eight_way_draw(x0, y0, x, y):
        glPointSize(2)  # pixel size
        glBegin(GL_POINTS)

        glVertex2f(x + x0, y + y0)  # zone 0
        glVertex2f(y + x0, x + y0)  # zone 1
        glVertex2f(-y + x0, x + y0)  # zone 2
        glVertex2f(-x + x0, y + y0)  # zone 3
        glVertex2f(-x + x0, -y + y0)  # zone 4
        glVertex2f(-y + x0, -x + y0)  # zone 5
        glVertex2f(y + x0, -x + y0)  # zone 6
        glVertex2f(x + x0, -y + y0)  # zone 7

        glEnd()

    @staticmethod
    def midPointCircle(x0, y0, rad):
        x = 0
        y = rad
        d = 1 - rad

        Circle.eight_way_draw(x0, y0, x, y)
        while x < y:
            if d >= 0:
                # SE
                d = d + 2 * x - 2 * y + 5
                x += 1
                y -= 1
            else:
                # E
                d = d + 2 * x + 3
                x += 1

            Circle.eight_way_draw(x0, y0, x, y)

    @staticmethod
    def circles(rad, x0, y0):
        Circle.midPointCircle(x0, y0, rad)  # Outer Circle

class Dinosaur:
    def __init__(self):
        self.x = 150
        self.y = 200
        self.jump_height = 130  # Adjust this value to control jump height
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
        for i in range(1,26):
            Circle.circles(i, self.x, self.y)
        Line.plot(self.x - 20, self.y + 10, self.x - 40, self.y - 40)
        Line.plot(self.x - 90, self.y - 40, self.x - 40, self.y - 40)
        Line.plot(self.x + 20, self.y - 20, self.x, self.y - 70)
        Line.plot(self.x - 70, self.y - 70, self.x, self.y - 70)
        Line.plot(self.x - 110, self.y - 30, self.x - 70, self.y - 70)
        Line.plot(self.x - 50, self.y - 70, self.x - 50, self.y - 100)
        Line.plot(self.x - 60, self.y - 100, self.x - 20, self.y - 100)
        Line.plot(self.x - 30, self.y - 70, self.x - 30, self.y - 100)

        glColor3f(.2, .5, .2)
        Line.plot(0, 100, 800, 100)


class MovingTriangles:
    def __init__(self):
        num_triangles = random.randint(2, 3)
        self.triangles = []
        x = 800  # Start from the rightmost boundary
        for _ in range(num_triangles):
            size = random.randint(30, 60)
            x -= 400  # Keep a fixed space of 400 units between triangles
            y = 120  # Place on the horizontal line
            self.triangles.append((x, y, x + size, y + size, False))  # Add False flag for tracking
            x -= size
        self.translation = np.array([-0.1, 0.0], dtype=np.float32)  # Initial translation speed to move left
        self.start_time = time.time()
        self.total_time = 180  # 3 minutes in seconds
        self.num_triangles_disappeared = 0
        self.num_triangles_touched = 0

    def draw(self):
        glColor3f(0.0, 1.0, 0.0)
        for triangle in self.triangles:
            x1, y1, x2, y2, _ = triangle
            Line.plot(x1, y1, x2, y1)
            Line.plot(x1, y1, (x1 + x2) / 2, y2)
            Line.plot((x1 + x2) / 2, y2, x2, y1)
            Line.plot((x1 + x2) / 2, y1, (x1 + x2) / 2, 100)

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.total_time:
            # Adjust translation speed linearly from -0.1 to -5.0 within 1 minute
            speed_factor = -0.9 - (elapsed_time / self.total_time) * 4.9
            self.translation[0] = speed_factor

        for i in range(len(self.triangles)):
            self.triangles[i] = (
                self.triangles[i][0] + self.translation[0],
                self.triangles[i][1] + self.translation[1],
                self.triangles[i][2] + self.translation[0],
                self.triangles[i][3] + self.translation[1],
                self.triangles[i][4]  # Retain the flag
            )
            if self.triangles[i][2] < 0:
                self.num_triangles_disappeared += 1
                self.triangles[i] = (
                    self.triangles[i][0] + 800,
                    self.triangles[i][1],
                    self.triangles[i][2] + 800,
                    self.triangles[i][3],
                    self.triangles[i][4]  # Retain the flag
                )
            if self.triangles[i][0] < 0 and not self.triangles[i][4]:
                self.triangles[i] = (
                    self.triangles[i][0],
                    self.triangles[i][1],
                    self.triangles[i][2],
                    self.triangles[i][3],
                    True  # Set the flag to True
                )
                self.num_triangles_touched += 1
            elif self.triangles[i][0] >= 0:
                self.triangles[i] = (
                    self.triangles[i][0],
                    self.triangles[i][1],
                    self.triangles[i][2],
                    self.triangles[i][3],
                    False  # Set the flag to False
                )


def drawRotatingRectangle(x, y, width, height, angle):
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # Blue color for the rectangle

    glTranslatef(x, y, 0)  # Translate to the specified position
    glRotatef(angle, 0, 0, 1)  # Rotate around the Z-axis

    half_width = width / 2
    half_height = height / 2

    glBegin(GL_QUADS)
    glVertex2f(-half_width, -half_height)
    glVertex2f(half_width, -half_height)
    glVertex2f(half_width, half_height)
    glVertex2f(-half_width, half_height)
    glEnd()

    glPopMatrix()

moving_triangles = MovingTriangles()
dinosaur = Dinosaur()
is_day = False
stars = [(random.uniform(0, 800), random.uniform(800, 300)) for _ in range(200)]
pause = False

def outdoorScene():
    if(is_day):
        glColor3f(1.0, 0.843, 0.0)
    else:
        glColor3f(1,1,1)
        for x, y in stars:
            Line.WritePixel(x, y)

    for i in range(1,40):
        Circle.circles(i,100,450)

def keyboard(key, x, y):
    global is_day,pause
    if key == b' ':
        dinosaur.jump()
    if key == b"d":
        is_day = not is_day
    if key == b"\x1b":
        pause = not pause

def iterate():
    global is_day
    glViewport(0, 0, 800, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if(is_day):
        glClearColor(.8, 0.8, .8, 2)
    else:
        glClearColor(0, 0, 0, 1)
    glOrtho(0.0, 800, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    outdoorScene()
    if(not pause):
        moving_triangles.update()
        dinosaur.update()
    dinosaur.draw()
    displayPoint()
    moving_triangles.draw()

    glutSwapBuffers()

def displayPoint(num_passed=0):
    global moving_triangles
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(600, 50)
    for char in "Score: " + str(moving_triangles.num_triangles_touched):
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glutTimerFunc(num_passed, displayPoint, 1000)

# def print_passed_triangles(num_passed):
#     global moving_triangles
#     print("Score: ", moving_triangles.num_triangles_touched)
#     glutTimerFunc(num_passed, print_passed_triangles, 1000)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 500)  # window size
glutInitWindowPosition(250, 150)
wind = glutCreateWindow(b"Dinosaur Jump Game")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutIdleFunc(showScreen)
glutTimerFunc(0, displayPoint, 1000)
# glutTimerFunc(0, print_passed_triangles, 1000)
glutMainLoop()