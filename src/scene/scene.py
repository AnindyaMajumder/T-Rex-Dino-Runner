from OpenGL.GL import *
from shapes.circle import Circle
from shapes.line import Line
import random

class Scene:
    def __init__(self):
        self.is_day = False
        self.stars = [(random.uniform(0, 800), random.uniform(800, 300)) for _ in range(200)]
    
    def toggle_day_night(self):
        """Toggle between day and night mode"""
        self.is_day = not self.is_day
        return self.is_day
    
    def draw(self):
        """Draw the outdoor scene based on day/night status"""
        # Sky background
        if self.is_day:
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
        if self.is_day:
            glColor3f(1.0, 0.843, 0.0)  # Yellow for the sun
        else:
            glColor3f(1.0, 1.0, 1.0)  # White for the moon
        for i in range(1, 40):
            Circle.circles(i, 100, 450)
            
        # Clouds (daytime only)
        if self.is_day:
            glColor3f(1.0, 1.0, 1.0)  # White for clouds
            Circle.circles(20, 200, 400)
            Circle.circles(30, 230, 420)
            Circle.circles(20, 260, 400)

            Circle.circles(20, 500, 450)
            Circle.circles(30, 530, 470)
            Circle.circles(20, 560, 450)

        # Stars (nighttime only)
        if not self.is_day:
            glColor3f(1.0, 1.0, 1.0)  # White for stars
            for x, y in self.stars:
                Line.WritePixel(x, y)
    
    def set_clear_color(self):
        """Set the background clear color based on day/night mode"""
        if self.is_day:
            glClearColor(0.8, 0.8, 0.8, 2)
        else:
            glClearColor(0, 0, 0, 1)