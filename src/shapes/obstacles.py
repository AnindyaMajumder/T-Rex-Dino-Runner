from OpenGL.GL import *
from .line import Line
from logics.speed import GameSpeed
import random
import time

class MovingObstacles:
    def __init__(self):
        self.obstacles = []
        self.ground_level = 100  # Height of the ground
        self.speed_controller = GameSpeed()
        self.generate_obstacles()
        self.last_update_time = time.time()
        self.num_triangles_touched = 0
        self.translation = [0, 0]  # [x, y] translation offset
        
    def generate_obstacles(self, start_x=800, count=4, min_spacing=400, max_spacing=900):
        """Generate a sequence of random obstacles with appropriate spacing"""
        self.obstacles = []
        current_x = start_x
        
        for _ in range(count):
            obstacle_type = random.choice(["small_cactus", "tall_cactus", "cactus_group", "bird_cactus"])
            
            width = self.get_obstacle_width(obstacle_type)
            height = self.get_obstacle_height(obstacle_type)
            
            self.obstacles.append({
                "type": obstacle_type,
                "x": current_x,
                "y": self.ground_level,  # All obstacles start from ground level
                "width": width,
                "height": height,
                "passed": False  # Track if the obstacle has been passed
            })
            
            # Add spacing for next obstacle
            spacing = random.randint(min_spacing, max_spacing)
            current_x += width + spacing
    
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
        """Return the height for each obstacle type"""
        if obstacle_type == "small_cactus":
            return random.randint(40, 60)
        elif obstacle_type == "tall_cactus":
            return random.randint(70, 90)
        elif obstacle_type == "bird_cactus":
            return random.randint(120, 160)
        else:  # cactus_group
            return random.randint(50, 70)
            
    def update(self):
        """Update obstacle positions based on game speed"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Get current game speed
        speed = self.speed_controller.update(delta_time)
        
        # Move obstacles to the left based on speed
        for obstacle in self.obstacles:
            obstacle["x"] -= speed
            
            # Check if an obstacle has just passed the dinosaur
            if not obstacle["passed"] and obstacle["x"] < 100:  # Dinosaur x position is 150
                obstacle["passed"] = True
                self.num_triangles_touched += 1
        
        # Remove obstacles that are off-screen to the left
        self.obstacles = [obs for obs in self.obstacles if obs["x"] > -100]
        
        # Add new obstacles if needed
        if len(self.obstacles) < 4:
            last_x = self.obstacles[-1]["x"] if self.obstacles else 800
            self.add_obstacle(last_x + random.randint(200, 400))
            
        # Update translation value for animation synchronization
        self.translation[0] = speed
        
        return speed
        
    def add_obstacle(self, x_position):
        """Add a new obstacle at the specified position"""
        obstacle_type = random.choice(["small_cactus", "tall_cactus", "cactus_group", "bird_cactus"])
        width = self.get_obstacle_width(obstacle_type)
        height = self.get_obstacle_height(obstacle_type)
        
        self.obstacles.append({
            "type": obstacle_type,
            "x": x_position,
            "y": self.ground_level,
            "width": width,
            "height": height,
            "passed": False
        })
    
    def set_ground_level(self, level):
        """Set the ground level for all obstacles"""
        self.ground_level = level
        for obstacle in self.obstacles:
            obstacle["y"] = level

    def get_score(self):
        """Get the current score"""
        return self.speed_controller.get_score()

    def reset(self):
        """Reset the game"""
        self.speed_controller.reset()
        self.obstacles = []
        self.num_triangles_touched = 0
        self.generate_obstacles()

    def draw(self):
        """Draw all obstacles at their current positions"""
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
                self.draw_flying_cactus(x, y + 90, width, height-90)
            else:  # cactus_group
                glColor3f(0.0, 0.42, 0.05)  # Another shade for variety
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

    def detect_collision(self, dino_x, dino_y, dino_width=40, dino_height=60):
        """Check for collision between dinosaur and obstacles"""
        # Simplified collision detection with smaller hitboxes for better gameplay
        dino_hitbox_x = dino_x + 10  # Offset from left edge
        dino_hitbox_width = dino_width - 20  # Narrower than visual size
        dino_hitbox_height = dino_height - 10  # Shorter than visual size
        
        for obstacle in self.obstacles:
            # Skip obstacles that are too far away
            if obstacle["x"] > dino_x + dino_width + 10:
                continue
                
            # Skip obstacles that have already passed
            if obstacle["x"] + obstacle["width"] < dino_x - 10:
                continue
                
            # Adjust obstacle hitbox based on type
            obs_hitbox_width = obstacle["width"] * 0.8
            obs_hitbox_x = obstacle["x"] + (obstacle["width"] - obs_hitbox_width) / 2
                
            # Special case for flying cactus - check at dinosaur head height
            if obstacle["type"] == "bird_cactus":
                # Flying cactus is in the air, so check if dinosaur is jumping
                if dino_y > self.ground_level + 60:  # If dinosaur is high in jump
                    if (dino_hitbox_x < obs_hitbox_x + obs_hitbox_width and
                        dino_hitbox_x + dino_hitbox_width > obs_hitbox_x and
                        dino_y + dino_hitbox_height > obstacle["y"] + 90 and
                        dino_y < obstacle["y"] + 90 + obstacle["height"] - 90):
                        return True
            else:
                # Standard ground obstacle collision check
                if (dino_hitbox_x < obs_hitbox_x + obs_hitbox_width and
                    dino_hitbox_x + dino_hitbox_width > obs_hitbox_x and
                    dino_y < obstacle["y"] + obstacle["height"] and
                    dino_y + dino_hitbox_height > obstacle["y"]):
                    return True
                    
        return False