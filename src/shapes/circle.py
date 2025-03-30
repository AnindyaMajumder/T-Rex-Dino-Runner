from OpenGL.GL import *

class Circle:
    @staticmethod
    def eight_way_draw(x0, y0, x, y):
        glPointSize(2)
        glBegin(GL_POINTS)

        glVertex2f(x + x0, y + y0)
        glVertex2f(y + x0, x + y0)
        glVertex2f(-y + x0, x + y0)
        glVertex2f(-x + x0, y + y0)
        glVertex2f(-x + x0, -y + y0)
        glVertex2f(-y + x0, -x + y0)
        glVertex2f(y + x0, -x + y0)
        glVertex2f(x + x0, -y + y0)

        glEnd()

    @staticmethod
    def midPointCircle(x0, y0, rad):
        x = 0
        y = rad
        d = 1 - rad

        Circle.eight_way_draw(x0, y0, x, y)
        while x < y:
            if d >= 0:
                d = d + 2 * x - 2 * y + 5
                x += 1
                y -= 1
            else:
                d = d + 2 * x + 3
                x += 1

            Circle.eight_way_draw(x0, y0, x, y)

    @staticmethod
    def circles(rad, x0, y0):
        Circle.midPointCircle(x0, y0, rad)