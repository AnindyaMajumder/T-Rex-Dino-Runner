from OpenGL.GL import *
from .line import Line
import random
import time
import numpy as np

class MovingTriangles:
    def __init__(self):
        num_triangles = random.randint(2, 3)
        self.triangles = []
        x = 800
        for _ in range(num_triangles):
            size = random.randint(30, 60)
            x -= 400
            y = 120
            self.triangles.append((x, y, x + size, y + size, False))
            x -= size
        self.translation = np.array([-0.1, 0.0], dtype=np.float32)
        self.start_time = time.time()
        self.total_time = 180
        self.num_triangles_disappeared = 0
        self.num_triangles_touched = 0

    def draw(self):
        glColor3f(0.0, 1.0, 0.0)
        for triangle in self.triangles:
            x1, y1, x2, y2, _ = triangle
            Line.plot(x1, y1, x2, y1)
            Line.plot(x1, y1, (x1 + x2) / 2, y2)
            Line.plot((x1 + x2) / 2, y2, x2, y1)

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.total_time:
            speed_factor = -0.9 - (elapsed_time / self.total_time) * 4.9
            self.translation[0] = speed_factor

        for i in range(len(self.triangles)):
            self.triangles[i] = (
                self.triangles[i][0] + self.translation[0],
                self.triangles[i][1] + self.translation[1],
                self.triangles[i][2] + self.translation[0],
                self.triangles[i][3] + self.translation[1],
                self.triangles[i][4]
            )
            if self.triangles[i][2] < 0:
                self.num_triangles_disappeared += 1
                self.triangles[i] = (
                    self.triangles[i][0] + 800,
                    self.triangles[i][1],
                    self.triangles[i][2] + 800,
                    self.triangles[i][3],
                    self.triangles[i][4]
                )
            if self.triangles[i][0] < 0 and not self.triangles[i][4]:
                self.triangles[i] = (
                    self.triangles[i][0],
                    self.triangles[i][1],
                    self.triangles[i][2],
                    self.triangles[i][3],
                    True
                )
                self.num_triangles_touched += 1
            elif self.triangles[i][0] >= 0:
                self.triangles[i] = (
                    self.triangles[i][0],
                    self.triangles[i][1],
                    self.triangles[i][2],
                    self.triangles[i][3],
                    False
                )