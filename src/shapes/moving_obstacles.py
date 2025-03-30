from OpenGL.GL import *
from .line import Line
import random
import time
import numpy as np

class MovingObstacles:
    def __init__(self):
        self.obstacles = []
        # Start with a slower speed
        self.translation = np.array([-0.5, 0.0], dtype=np.float32)
        self.start_time = time.time()
        self.total_time = 300  # 3 minutes of gameplay for full difficulty
        self.obstacles_disappeared = 0
        self.obstacles_touched = 0
        self.last_spawn_time = time.time()
        # Longer initial spawn interval for easier start
        self.spawn_interval = random.uniform(2.5, 4.0)
        
        # Ensure obstacles are generated immediately
        self.create_initial_obstacles()

    def get_obstacle_width(self, obstacle_type):
        """Return the width for each obstacle type"""
        if obstacle_type == "small_cactus":
            return 20
        elif obstacle_type == "tall_cactus":
            return 25
        elif obstacle_type == "bird_cactus":
            return 30
        else:  # cactus_group
            return 60

    def get_obstacle_height(self, obstacle_type):
        if obstacle_type == "small_cactus":
            return random.randint(40, 60)  # Lower height for small cacti
        elif obstacle_type == "tall_cactus":
            return random.randint(70, 90)  # Shorter tall cacti
        elif obstacle_type == "bird_cactus":
            return random.randint(120, 160)  # Lower flying obstacles 
        else:  # cactus_group
            return random.randint(50, 70)  # Shorter group cacti


    def create_initial_obstacles(self):
        # Create first obstacle further away to give player time to react
        self.obstacles.append({
            "type": "small_cactus",
            "x": 800,  # Moved further to allow for longer jump duration
            "y": 100,  # Base at ground level
            "width": 20,
            "height": 50,
            "touched": False
        })
        
        # Add a few more off-screen with greater spacing
        x_positions = [1200, 1800, 2400]  # Increased spacing for initial obstacles
        for x_pos in x_positions:
            obstacle_type = random.choice(["small_cactus", "tall_cactus", "cactus_group", "bird_cactus"])
            self.obstacles.append({
                "type": obstacle_type,
                "x": x_pos,
                "y": 100,
                "width": self.get_obstacle_width(obstacle_type),
                "height": self.get_obstacle_height(obstacle_type),
                "touched": False
            })

    def draw(self):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            x = obstacle["x"]
            y = obstacle["y"]
            width = obstacle["width"]
            height = obstacle["height"]
            
            if obstacle["type"] == "small_cactus":
                glColor3f(0.0, 0.5, 0.0)  # Slightly brighter green
                self.draw_cactus(x, y, width, height, True, "small")
            elif obstacle["type"] == "tall_cactus":
                glColor3f(0.0, 0.4, 0.0)  # Dark green
                self.draw_cactus(x, y, width, height, True, "tall")
            elif obstacle["type"] == "bird_cactus":
                glColor3f(0.0, 0.45, 0.1)  # Different shade of green
                # Adjust flying cactus to a better height - not too high
                self.draw_flying_cactus(x, y + 90, width, height-90)
            else:  # cactus_group
                glColor3f(0.0, 0.42, 0.05)  # Another shade for variety
                # Draw a group of cacti with better spacing
                small_width = width // 4
                self.draw_cactus(x, y, small_width, height * 0.85, True, "small")
                self.draw_cactus(x + small_width * 1.5, y, small_width, height, True, "tall")
                if random.choice([True, False]):
                    self.draw_cactus(x + small_width * 3, y, small_width, height * 0.9, True, "small")
    
    def draw_cactus(self, x, y, width, height, with_arms, cactus_type):
        """Draw a single cactus with optional arms"""
        # Main stem with thicker lines for better visibility
        glLineWidth(2.0)
        Line.plot(x, y, x, y + height)
        Line.plot(x + width, y, x + width, y + height)
        Line.plot(x, y + height, x + width, y + height)
        
        # Add some texture to the cactus
        num_lines = int(height / 10)
        for i in range(1, num_lines):
            # Horizontal texture lines
            y_pos = y + i * 10
            Line.plot(x, y_pos, x + width, y_pos)
        
        # Arms with better proportion and randomization
        if with_arms:
            # First set of arms
            arm_height = y + height * (0.65 + random.random() * 0.15)
            arm_length = width * (1.2 + random.random() * 0.3)
            arm_width = width * 0.7
            
            # Left arm (with depth)
            if cactus_type == "tall" or random.random() > 0.3:
                Line.plot(x, arm_height, x - arm_length, arm_height)
                Line.plot(x - arm_length, arm_height, x - arm_length, arm_height + arm_width)
                Line.plot(x - arm_length, arm_height + arm_width, x, arm_height + arm_width)
                # Texture on arm
                for i in range(1, int(arm_width / 5)):
                    Line.plot(x - arm_length, arm_height + i * 5, x, arm_height + i * 5)
            
            # Right arm (with depth)
            if cactus_type == "tall" or random.random() > 0.3:
                Line.plot(x + width, arm_height, x + width + arm_length, arm_height)
                Line.plot(x + width + arm_length, arm_height, x + width + arm_length, arm_height + arm_width)
                Line.plot(x + width + arm_length, arm_height + arm_width, x + width, arm_height + arm_width)
                # Texture on arm
                for i in range(1, int(arm_width / 5)):
                    Line.plot(x + width, arm_height + i * 5, x + width + arm_length, arm_height + i * 5)
            
            # Maybe add a second set of arms for tall cacti
            if cactus_type == "tall" and random.random() > 0.5:
                arm_height2 = y + height * (0.3 + random.random() * 0.15)
                arm_length2 = width * (0.8 + random.random() * 0.3)
                arm_width2 = width * 0.6
                
                # Second left arm
                if random.random() > 0.4:
                    Line.plot(x, arm_height2, x - arm_length2, arm_height2)
                    Line.plot(x - arm_length2, arm_height2, x - arm_length2, arm_height2 + arm_width2)
                    Line.plot(x - arm_length2, arm_height2 + arm_width2, x, arm_height2 + arm_width2)
                
                # Second right arm
                if random.random() > 0.4:
                    Line.plot(x + width, arm_height2, x + width + arm_length2, arm_height2)
                    Line.plot(x + width + arm_length2, arm_height2, x + width + arm_length2, arm_height2 + arm_width2)
                    Line.plot(x + width + arm_length2, arm_height2 + arm_width2, x + width, arm_height2 + arm_width2)
        
        # Reset line width
        glLineWidth(1.0)

    def draw_flying_cactus(self, x, y, width, height):
        """Draw a flying cactus with wings"""
        # Flying cactus (a smaller cactus with "wings")
        # Draw the small cactus body
        self.draw_cactus(x, y, width, height, False, "small")
        
        # Add wings
        wing_width = width * 2
        wing_height = height * 0.6
        
        # Left wing
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y + height * 0.3)
        glVertex2f(x - wing_width, y + height * 0.5)
        glVertex2f(x, y + height * 0.7)
        glEnd()
        
        # Right wing
        glBegin(GL_LINE_LOOP)
        glVertex2f(x + width, y + height * 0.3)
        glVertex2f(x + width + wing_width, y + height * 0.5)
        glVertex2f(x + width, y + height * 0.7)
        glEnd()

    def update(self):
        elapsed_time = time.time() - self.start_time
        
        # More gradual speed increase over time
        if elapsed_time < self.total_time:
            # Start slower and increase gradually
            speed_factor = min(-1.5, -0.5 - (elapsed_time / self.total_time) * 3.0)
            self.translation[0] = speed_factor
        
        # Variables to track if a flying cactus was just processed
        had_flying_cactus = False
        
        # Update obstacle positions
        obstacles_to_remove = []
        for i, obstacle in enumerate(self.obstacles):
            # Apply movement to each obstacle
            obstacle["x"] += self.translation[0]
            
            # Check if obstacle has gone off screen
            if obstacle["x"] + obstacle["width"] < 0:
                self.obstacles_disappeared += 1
                obstacles_to_remove.append(i)
            
            # Check if obstacle has crossed the dinosaur position
            dino_zone = 150  # X-coordinate where dino is
            if obstacle["x"] < dino_zone and (obstacle["x"] + obstacle["width"]) > (dino_zone - 40) and not obstacle["touched"]:
                obstacle["touched"] = True
                self.obstacles_touched += 1
                
                # Check if this was a flying cactus (for spacing the next obstacle)
                if obstacle["type"] == "bird_cactus":
                    had_flying_cactus = True
        
        # Remove obstacles that are offscreen
        for index in sorted(obstacles_to_remove, reverse=True):
            if index < len(self.obstacles):  # Safeguard against index errors
                self.obstacles.pop(index)
        
        # Spawn new obstacles as needed
        current_time = time.time()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.last_spawn_time = current_time
            # Gradually decrease spawn interval as game progresses
            max_interval = 4.0 - (elapsed_time / self.total_time) * 2.5
            min_interval = 2.5 - (elapsed_time / self.total_time) * 1.5
            self.spawn_interval = random.uniform(min_interval, max_interval)
            
            # Add a new obstacle at the right edge with better spacing
            obstacle_type = random.choice(["small_cactus", "tall_cactus", "cactus_group", "bird_cactus"])
            
            # ENHANCED SPACING CALCULATIONS
            # Base spacing values - increase minimum to ensure enough space between obstacles
            min_spacing = 400  # Increased from 350 to give more reaction time
            max_spacing = 650  # Increased from 600
            
            # Check if the last obstacle was a flying cactus (we check all obstacles)
            last_was_flying = False
            if self.obstacles:
                # Check the most recent obstacle that passed the dino
                for obs in reversed(self.obstacles):
                    if obs["touched"] and obs["type"] == "bird_cactus":
                        last_was_flying = True
                        break
            
            # If the previous obstacle was flying, add extra spacing
            if last_was_flying or had_flying_cactus:
                min_spacing += 150
                max_spacing += 150
            
            # Adjust spacing based on speed - faster = more space
            speed_adjustment = abs(self.translation[0]) * 60
            min_spacing += speed_adjustment
            max_spacing += speed_adjustment
            
            # Force positive values and reasonable limits
            min_spacing = max(400, min(min_spacing, 900))
            max_spacing = max(650, min(max_spacing, 1200))
            
            # Ensure new obstacles are properly spaced
            if self.obstacles:
                last_x = max([o["x"] for o in self.obstacles])
                new_x = last_x + random.randint(int(min_spacing), int(max_spacing))
            else:
                new_x = 850  # Just off-screen
                
            self.obstacles.append({
                "type": obstacle_type,
                "x": new_x,
                "y": 100,  # Base at ground level
                "width": self.get_obstacle_width(obstacle_type),
                "height": self.get_obstacle_height(obstacle_type),
                "touched": False
            })
            
    @property
    def num_triangles_touched(self):
        """Legacy property for compatibility with main.py"""
        return self.obstacles_touched