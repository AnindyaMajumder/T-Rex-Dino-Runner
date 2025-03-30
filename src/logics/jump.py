import math
import time

class JumpPhysics:
    def __init__(self):
        self.jump_height = 150  # Maximum jump height in pixels
        self.jump_duration = 0.7  # Total jump duration in seconds
        self.is_jumping = False
        self.jump_start_time = 0
        self.jump_pressed = False
        self.base_y = 130  # Base y position of dinosaur (ground level)
        self.current_y = self.base_y
        self.jump_progress = 0.0
        
    def jump_press(self):
        """Handle jump button press"""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_start_time = time.time()
            self.jump_pressed = True
            return True
        return False
        
    def jump_release(self):
        """Handle jump button release"""
        self.jump_pressed = False
    
    def update(self, delta_time):
        """Update jump state and return the current y position"""
        if not self.is_jumping:
            return self.base_y, 0.0, False
        
        # Calculate how far we are in the jump (0 to 1)
        elapsed = time.time() - self.jump_start_time
        progress = min(elapsed / self.jump_duration, 1.0)
        
        # If jump is complete
        if progress >= 1.0:
            self.is_jumping = False
            self.current_y = self.base_y
            self.jump_progress = 0.0
            return self.base_y, 0.0, False
        
        # Parabolic jump trajectory (smooth up and down)
        # y = 4h * t * (1-t) where t is normalized time (0 to 1)
        # This creates a parabola with peak at t=0.5
        height_factor = 4.0 * self.jump_height * progress * (1.0 - progress)
        self.current_y = self.base_y + height_factor
        self.jump_progress = progress
        
        return self.current_y, progress, True
    
    def get_vertical_position(self):
        """Return the current vertical position"""
        return self.current_y
    
    def is_currently_jumping(self):
        """Return whether the dinosaur is currently in a jump"""
        return self.is_jumping