from OpenGL.GL import *
from .circle import Circle
from .line import Line
import time
import math

class Dinosaur:
    def __init__(self):
        self.base_x = 150  # Base x position
        self.x = self.base_x  # Current x position
        self.y = 130  # Lower starting position to match ground
        self.base_y = 130  # Store the ground level
        self.jump_height = 210  # Significantly increased jump height
        self.max_jump_height = 280  # Even higher maximum jump height
        self.jump_time = 0
        self.jumping = False
        self.max_jump_time = 100  # Longer jump duration for higher arc
        self.size = 0.7  # Scaling factor to make dino smaller
        
        # For variable jump height
        self.jump_start_time = 0
        self.jump_key_held = False
        self.key_hold_duration = 0
        self.target_height = self.jump_height
        
        # Horizontal jump parameters
        self.forward_distance = 90  # Significantly increased forward movement
        self.max_forward_distance = 150  # Much larger horizontal movement for projectile

    def jump_press(self):
        """Called when jump key is initially pressed"""
        if not self.jumping:
            self.jumping = True
            self.jump_time = 0
            self.jump_key_held = True
            self.jump_start_time = time.time()
            # Reset position to base
            self.x = self.base_x
            # Start with standard height, will be adjusted if key is held
            self.target_height = self.jump_height
            self.target_distance = self.forward_distance

    def jump_release(self):
        """Called when jump key is released"""
        if self.jump_key_held:
            self.jump_key_held = False
            # Calculate how long the key was held
            hold_duration = time.time() - self.jump_start_time
            
            # Adjust jump height based on hold duration (0.1-0.5 seconds)
            if hold_duration < 0.1:
                # Short press = lower jump
                self.target_height = self.jump_height * 0.7
                self.target_distance = self.forward_distance * 0.6
            elif hold_duration > 0.5:
                # Long press = higher jump
                self.target_height = min(self.max_jump_height, self.jump_height * 1.3)
                self.target_distance = min(self.max_forward_distance, self.forward_distance * 1.5)
            else:
                # Medium press = standard jump
                self.target_height = self.jump_height
                self.target_distance = self.forward_distance

    def update(self):
        if self.jumping:
            self.jump_time += 1
            
            # If key is still held after 0.5s, use maximum height
            if self.jump_key_held and (time.time() - self.jump_start_time) > 0.5:
                self.target_height = self.max_jump_height
                self.target_distance = self.max_forward_distance
            
            # Calculate jump progress as a fraction (0 to 1)
            progress = self.jump_time / self.max_jump_time
            
            # Parabolic jump trajectory with variable height
            if self.jump_time <= self.max_jump_time / 2:
                # Upward acceleration phase with slower rise
                fraction = self.jump_time / (self.max_jump_time / 2)
                self.y = self.base_y + self.target_height * (fraction * (2 - fraction))
            else:
                # Downward acceleration phase with slower fall
                fraction = (self.jump_time - self.max_jump_time / 2) / (self.max_jump_time / 2)
                self.y = self.base_y + self.target_height * ((1 - fraction) * (2 - (1 - fraction)))
            
            # More hang time at the peak of the jump
            if self.jump_time > (self.max_jump_time / 2 - 8) and self.jump_time < (self.max_jump_time / 2 + 8):
                self.y = self.base_y + self.target_height  # Hold at max height
            
            # Horizontal movement - move forward during the first half, then back
            # This creates an arc-like path for more horizontal coverage
            if progress <= 0.5:
                # Moving forward during rise
                self.x = self.base_x + self.target_distance * (progress * 2)
            else:
                # Moving back during fall
                self.x = self.base_x + self.target_distance * (2 - progress * 2)
            
            # End jump cycle
            if self.jump_time >= self.max_jump_time:
                self.y = self.base_y
                self.x = self.base_x  # Reset to original x position
                self.jumping = False
                
    def draw(self):
        # Apply scaling by adjusting coordinates relative to center
        s = self.size  # scaling factor
        cx, cy = self.x, self.y  # center point
        
        # T-Rex body shape (improved)
        glColor3f(0.2, 0.7, 0.3)  # Green dinosaur color
        
        # Head
        for i in range(1, int(18 * s)):
            Circle.circles(i, cx, cy + int(10 * s))
        
        # Body (more compact)
        glBegin(GL_POLYGON)
        glVertex2f(cx - int(15 * s), cy + int(15 * s))  # Top neck
        glVertex2f(cx - int(40 * s), cy)                # Mid back
        glVertex2f(cx - int(30 * s), cy - int(15 * s))  # Lower back
        glVertex2f(cx + int(10 * s), cy - int(15 * s))  # Bottom front
        glVertex2f(cx + int(15 * s), cy)                # Mid front
        glEnd()
        
        # Front leg animation based on jump state
        glLineWidth(2.0)
        if self.jumping:
            # Legs tucked up during jump
            leg_angle = 45 * math.sin(self.jump_time * 0.2)
            
            # Front leg tucked
            leg_x = cx + int(5 * s)
            leg_y = cy - int(15 * s)
            leg_length = int(15 * s)
            
            # Calculate the leg end position with angle
            end_x = leg_x + leg_length * math.cos(math.radians(leg_angle))
            end_y = leg_y - leg_length * math.sin(math.radians(leg_angle))
            
            Line.plot(leg_x, leg_y, int(end_x), int(end_y))
            Line.plot(int(end_x), int(end_y), int(end_x + 10 * s), int(end_y))
            
            # Back leg tucked
            back_leg_x = cx - int(20 * s)
            back_leg_y = cy - int(15 * s)
            back_leg_angle = -leg_angle
            
            back_end_x = back_leg_x + leg_length * math.cos(math.radians(back_leg_angle))
            back_end_y = back_leg_y - leg_length * math.sin(math.radians(back_leg_angle))
            
            Line.plot(back_leg_x, back_leg_y, int(back_end_x), int(back_end_y))
            Line.plot(int(back_end_x), int(back_end_y), int(back_end_x + 10 * s), int(back_end_y))
        else:
            # Normal standing legs
            Line.plot(cx + int(5 * s), cy - int(15 * s), cx + int(5 * s), cy - int(30 * s))  # Upper leg
            Line.plot(cx + int(5 * s), cy - int(30 * s), cx + int(15 * s), cy - int(30 * s))  # Foot
            
            # Back leg
            Line.plot(cx - int(20 * s), cy - int(15 * s), cx - int(20 * s), cy - int(30 * s))  # Upper leg
            Line.plot(cx - int(20 * s), cy - int(30 * s), cx - int(10 * s), cy - int(30 * s))  # Foot
        
        # Arm (small T-Rex arm)
        Line.plot(cx, cy, cx + int(10 * s), cy + int(5 * s))
        
        # Eye
        glColor3f(0.9, 0.9, 0.9)  # White eye
        Circle.circles(int(3 * s), cx + int(12 * s), cy + int(12 * s))
        glColor3f(0.0, 0.0, 0.0)  # Black pupil
        Circle.circles(int(1 * s), cx + int(13 * s), cy + int(12 * s))
        
        # Mouth
        glColor3f(0.0, 0.0, 0.0)
        Line.plot(cx + int(18 * s), cy + int(5 * s), cx + int(8 * s), cy + int(5 * s))
        
        glLineWidth(1.0)