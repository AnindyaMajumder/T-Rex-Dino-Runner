from OpenGL.GL import *
from .circle import Circle
from .line import Line
from logics.jump import JumpPhysics
import math
import time

class Dinosaur:
    def __init__(self):
        self.x = 150  # Base x position
        self.y = 130  # Base y position
        self.size = 0.7  # Scaling factor to make dino smaller
        self.visual_offset_x = 0  # Horizontal offset for animation
        self.jump_physics = JumpPhysics()  # Jump physics handler
        self.last_update_time = time.time()
        self.run_animation_time = 0
        self.run_animation_period = 0.3  # Period of running animation in seconds
        
    def jump_press(self):
        """Handle jump button press"""
        return self.jump_physics.jump_press()
    
    def jump_release(self):
        """Handle jump button release"""
        self.jump_physics.jump_release()
    
    def update(self, game_speed):
        """Update dinosaur state based on current game conditions"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update jump physics
        new_y, jump_progress, is_jumping = self.jump_physics.update(delta_time)
        self.y = new_y
        self.is_jumping = is_jumping
        
        # Update running animation (bobbing motion when not jumping)
        if not is_jumping:
            self.run_animation_time += delta_time
            if self.run_animation_time > self.run_animation_period:
                self.run_animation_time -= self.run_animation_period
            
            # Create a slight up/down motion when running
            bob_amount = 3.0  # Pixels to bob up/down
            run_progress = self.run_animation_time / self.run_animation_period
            bob_offset = bob_amount * math.sin(run_progress * 2 * math.pi)
            self.visual_offset_x = math.sin(run_progress * 4 * math.pi) * 2.0
        else:
            # Use jump progress for animation
            self.jump_progress = jump_progress
    
    def set_position(self, x, y):
        """Set the dinosaur position"""
        self.x = x
        self.y = y
    
    def draw(self):
        """Draw the dinosaur at the current position with proper animation state"""
        # Apply scaling by adjusting coordinates relative to center
        s = self.size  # scaling factor
        cx, cy = self.x + self.visual_offset_x, self.y  # center point
        
        # T-Rex body shape
        glColor3f(0.2, 0.7, 0.3)  # Green dinosaur color
        
        # Head
        for i in range(1, int(18 * s)):
            Circle.circles(i, cx, cy + int(10 * s))
        
        # Body
        glBegin(GL_POLYGON)
        glVertex2f(cx - int(15 * s), cy + int(15 * s))  # Top neck
        glVertex2f(cx - int(40 * s), cy)                # Mid back
        glVertex2f(cx - int(30 * s), cy - int(15 * s))  # Lower back
        glVertex2f(cx + int(10 * s), cy - int(15 * s))  # Bottom front
        glVertex2f(cx + int(15 * s), cy)                # Mid front
        glEnd()
        
        # Legs and feet based on jumping state
        glLineWidth(2.0)
        if self.jump_physics.is_currently_jumping():
            self._draw_jumping_legs(cx, cy, s)
        else:
            self._draw_running_legs(cx, cy, s)
        
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
    
    def _draw_jumping_legs(self, cx, cy, s):
        """Draw legs for jumping animation state"""
        jump_progress = self.jump_physics.jump_progress
        
        # Dynamic leg animation based on jump phase
        if jump_progress < 0.2:
            # Takeoff phase - legs extending backward
            leg_angle = 60 * jump_progress / 0.2  # 0 to 60 degrees
        elif jump_progress > 0.8:
            # Landing phase - legs extending forward
            landing_progress = (jump_progress - 0.8) / 0.2  # 0 to 1 in landing phase
            leg_angle = 60 - 120 * landing_progress  # 60 to -60 degrees
        else:
            # Mid-flight - maintain tucked position
            mid_flight_progress = (jump_progress - 0.2) / 0.6  # 0 to 1 in mid-flight
            # Add subtle oscillation during flight
            leg_angle = 60 - 10 * math.sin(mid_flight_progress * math.pi * 2)
        
        # Front leg with dynamic angle
        leg_x = cx + int(5 * s)
        leg_y = cy - int(15 * s)
        leg_length = int(15 * s)
        
        # Calculate leg positions with the angle
        end_x = leg_x + leg_length * math.cos(math.radians(leg_angle))
        end_y = leg_y - leg_length * math.sin(math.radians(leg_angle))
        
        Line.plot(leg_x, leg_y, int(end_x), int(end_y))
        Line.plot(int(end_x), int(end_y), int(end_x + 10 * s), int(end_y))
        
        # Back leg with opposite angle for balance
        back_leg_x = cx - int(20 * s)
        back_leg_y = cy - int(15 * s)
        back_leg_angle = -leg_angle  # Mirror the front leg
        
        back_end_x = back_leg_x + leg_length * math.cos(math.radians(back_leg_angle))
        back_end_y = back_leg_y - leg_length * math.sin(math.radians(back_leg_angle))
        
        Line.plot(back_leg_x, back_leg_y, int(back_end_x), int(back_end_y))
        Line.plot(int(back_end_x), int(back_end_y), int(back_end_x + 10 * s), int(back_end_y))
    
    def _draw_running_legs(self, cx, cy, s):
        """Draw legs for running animation"""
        # Use run_animation_time to create alternating leg movements
        run_progress = self.run_animation_time / self.run_animation_period
        leg_angle_front = 30 * math.sin(run_progress * 2 * math.pi)  # -30 to 30 degrees
        leg_angle_back = -leg_angle_front  # Opposite movement
        
        # Front leg with dynamic angle
        leg_x = cx + int(5 * s)
        leg_y = cy - int(15 * s)
        leg_length = int(15 * s)
        
        # Calculate leg positions with the angle
        end_x = leg_x + leg_length * math.cos(math.radians(leg_angle_front))
        end_y = leg_y - leg_length * math.sin(math.radians(leg_angle_front))
        
        Line.plot(leg_x, leg_y, int(end_x), int(end_y))
        Line.plot(int(end_x), int(end_y), int(end_x + 10 * s), int(end_y))
        
        # Back leg with opposite angle for balance
        back_leg_x = cx - int(20 * s)
        back_leg_y = cy - int(15 * s)
        
        back_end_x = back_leg_x + leg_length * math.cos(math.radians(leg_angle_back))
        back_end_y = back_leg_y - leg_length * math.sin(math.radians(leg_angle_back))
        
        Line.plot(back_leg_x, back_leg_y, int(back_end_x), int(back_end_y))
        Line.plot(int(back_end_x), int(back_end_y), int(back_end_x + 10 * s), int(back_end_y))