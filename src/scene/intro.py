from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import math
import random

class IntroScene:
    def __init__(self):
        self.title = "T-Rex Runner"
        self.instructions = [
            "Press SPACE to start",
            "Press ESC to pause/resume",
            "Press D for day/night toggle"
        ]
        self.credits = "Created with OpenGL"
        self.high_score = 0
        self.animation_time = 0
        self.last_update_time = time.time()
        self.show_buttons = True
        self.button_animation_period = 0.5  # Blinking period in seconds
        
        # Animation variables
        self.clouds = [
            {'x': random.randint(0, 800), 'y': random.randint(300, 450), 'speed': random.uniform(0.5, 2.0), 'size': random.uniform(10, 25)}
            for _ in range(5)
        ]
        self.dino_jump_height = 0
        self.dino_jump_dir = 1
        self.stars = [(random.uniform(0, 800), random.uniform(300, 500)) for _ in range(50)]
        
        # Start button
        self.start_button = {
            'x': 350, 'y': 180,
            'width': 100, 'height': 40,
            'hover': False,
            'pulse': 0
        }
        
        # Game over buttons
        self.game_over_buttons = [
            {
                'x': 300, 'y': 180,
                'width': 200, 'height': 40,
                'hover': False,
                'text': "Play Again",
                'action': "restart"
            },
            {
                'x': 300, 'y': 130,
                'width': 200, 'height': 40,
                'hover': False,
                'text': "Main Menu",
                'action': "menu"
            }
        ]
        
    def update(self):
        """Update animation timers"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update button blink animation
        self.animation_time += delta_time
        if self.animation_time > self.button_animation_period:
            self.animation_time -= self.button_animation_period
            self.show_buttons = not self.show_buttons
        
        # Animate clouds
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed'] * delta_time * 20
            if cloud['x'] < -50:
                cloud['x'] = 850
                cloud['y'] = random.randint(300, 450)
                cloud['speed'] = random.uniform(0.5, 2.0)
                cloud['size'] = random.uniform(10, 25)
        
        # Animate dinosaur bounce
        self.dino_jump_height += 0.5 * self.dino_jump_dir
        if self.dino_jump_height > 8 or self.dino_jump_height < 0:
            self.dino_jump_dir *= -1
            
        # Animate start button pulsing
        self.start_button['pulse'] = (self.start_button['pulse'] + delta_time * 3) % (2 * math.pi)
            
    def set_high_score(self, score):
        """Update high score if the new score is higher"""
        if score > self.high_score:
            self.high_score = score
    
    def check_button_hover(self, x, y):
        """Check if mouse is hovering over any button"""
        # Convert GLUT coords to our coord system
        # GLUT Y is from top to bottom, our Y is from bottom to top
        y = 500 - y
        
        # Reset all hover states
        self.start_button['hover'] = False
        for button in self.game_over_buttons:
            button['hover'] = False
        
        # Check intro button
        btn = self.start_button
        if (x >= btn['x'] and x <= btn['x'] + btn['width'] and
            y >= btn['y'] and y <= btn['y'] + btn['height']):
            self.start_button['hover'] = True
            return "start"
        
        # Check game over buttons
        for button in self.game_over_buttons:
            if (x >= button['x'] and x <= button['x'] + button['width'] and
                y >= button['y'] and y <= button['y'] + button['height']):
                button['hover'] = True
                return button['action']
        
        return None
    
    def check_button_click(self, x, y):
        """Check if any button was clicked and return its action"""
        return self.check_button_hover(x, y)
        
    def draw(self, is_paused=False, current_score=0, is_day=True):
        """Draw the intro screen"""
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set background color - light blue for day, dark blue for night
        if is_day:
            glClearColor(0.529, 0.808, 0.922, 1.0)  # Light blue sky
        else:
            glClearColor(0.05, 0.05, 0.2, 1.0)  # Night sky
            
        # Force a clear with the new color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        # Draw stars at night
        if not is_day:
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(2.0)
            glBegin(GL_POINTS)
            for x, y in self.stars:
                # Add twinkling effect
                if random.random() > 0.97:
                    glVertex2f(x, y)
            glEnd()
            glPointSize(1.0)
        
        # Draw clouds
        glColor3f(1.0, 1.0, 1.0)
        for cloud in self.clouds:
            self._draw_cloud(cloud['x'], cloud['y'], cloud['size'])
        
        # Draw ground
        glColor3f(0.133, 0.545, 0.133)  # Green ground
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(800, 0)
        glVertex2f(800, 100)
        glVertex2f(0, 100)
        glEnd()
        
        # Draw title with shadow effect
        glColor3f(0.0, 0.0, 0.0)  # Black shadow
        self._draw_text(self.title, 403, 397, 30, center=True)
        glColor3f(0.0, 0.8, 0.0)  # Green color
        self._draw_text(self.title, 400, 400, 30, center=True)
        
        # Draw an animated dinosaur
        self._draw_dino_animated(400, 300 + self.dino_jump_height)
        
        # Draw scores
        glColor3f(1.0, 0.0, 0.0)  # Red color
        self._draw_text(f"High Score: {self.high_score}", 400, 250, 18, center=True)
        
        if is_paused:
            glColor3f(1.0, 0.5, 0.0)  # Orange color
            self._draw_text(f"Current Score: {current_score}", 400, 220, 18, center=True)
            
            # Draw pause menu
            self._draw_text("Game Paused", 400, 190, 20, center=True)
            
            # Draw buttons
            self._draw_button(350, 150, 100, 40, "Resume", self.start_button['hover'])
            self._draw_button(350, 100, 100, 40, "New Game", False)
        else:
            # Draw interactive start button with pulsing animation
            pulse_scale = 1.0 + 0.1 * math.sin(self.start_button['pulse'])
            btn_width = self.start_button['width'] * pulse_scale
            btn_height = self.start_button['height'] * pulse_scale
            btn_x = self.start_button['x'] - (btn_width - self.start_button['width'])/2
            btn_y = self.start_button['y'] - (btn_height - self.start_button['height'])/2
            
            self._draw_button(
                btn_x, btn_y, btn_width, btn_height, 
                "START GAME", 
                self.start_button['hover']
            )
            
            # Draw instructions
            if self.show_buttons:
                glColor3f(0.0, 0.0, 0.0)  # Black text
                for i, instruction in enumerate(self.instructions):
                    self._draw_text(instruction, 400, 120 - i * 25, 14, center=True)
        
        # Draw credits at the bottom
        glColor3f(0.0, 0.0, 0.0)  # Black text
        self._draw_text(self.credits, 400, 20, 12, center=True)
    
    def draw_game_over(self, final_score, high_score, is_day=True):
        """Draw the game over screen with animations"""
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set background color - light blue for day, dark blue for night
        if is_day:
            glClearColor(0.529, 0.808, 0.922, 1.0)  # Light blue sky
        else:
            glClearColor(0.05, 0.05, 0.2, 1.0)  # Night sky
            
        # Force a clear with the new color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        # Draw stars at night
        if not is_day:
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(2.0)
            glBegin(GL_POINTS)
            for x, y in self.stars:
                # Add twinkling effect
                if random.random() > 0.97:
                    glVertex2f(x, y)
            glEnd()
            glPointSize(1.0)
        
        # Draw clouds
        glColor3f(1.0, 1.0, 1.0)
        for cloud in self.clouds:
            self._draw_cloud(cloud['x'], cloud['y'], cloud['size'])
        
        # Draw ground
        glColor3f(0.133, 0.545, 0.133)  # Green ground
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(800, 0)
        glVertex2f(800, 100)
        glVertex2f(0, 100)
        glEnd()
        
        # Draw a fallen dinosaur
        self._draw_dino_fallen(400, 120)
        
        # Draw game over text with animation
        pulse_scale = 1.0 + 0.1 * math.sin(self.start_button['pulse'] * 2)
        glColor3f(1.0, 0.0, 0.0)  # Red color
        self._draw_text("GAME OVER", 400, 350, int(30 * pulse_scale), center=True)
        
        # Draw score information
        glColor3f(0.0, 0.0, 0.0)  # Black color
        self._draw_text(f"Your Score: {final_score}", 400, 300, 20, center=True)
        glColor3f(1.0, 0.7, 0.0)  # Gold color
        self._draw_text(f"High Score: {high_score}", 400, 270, 20, center=True)
        
        # Check if this was a new high score
        if final_score >= high_score and final_score > 0:
            glColor3f(1.0, 0.8, 0.0)  # Bright gold
            self._draw_text("NEW HIGH SCORE!", 400, 240, 22, center=True)
        
        # Draw action buttons with proper hover state
        self._draw_button(
            self.game_over_buttons[0]['x'], 
            self.game_over_buttons[0]['y'], 
            self.game_over_buttons[0]['width'], 
            self.game_over_buttons[0]['height'], 
            self.game_over_buttons[0]['text'], 
            self.game_over_buttons[0]['hover']
        )
        
        self._draw_button(
            self.game_over_buttons[1]['x'], 
            self.game_over_buttons[1]['y'], 
            self.game_over_buttons[1]['width'], 
            self.game_over_buttons[1]['height'], 
            self.game_over_buttons[1]['text'], 
            self.game_over_buttons[1]['hover']
        )
        
    def _draw_text(self, text, x, y, size=18, center=False):
        """Draw text at specified position"""
        if center:
            text_width = 0
            for c in text:
                if size <= 12:
                    text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_12, ord(c))
                elif size <= 16:
                    text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c))
                else:
                    text_width += glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
            x = x - text_width // 2
        
        glRasterPos2f(x, y)
        
        for c in text:
            if size <= 12:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
            elif size <= 16:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            else:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    
    def _draw_button(self, x, y, width, height, text, hover=False):
        """Draw an interactive button"""
        # Button background
        if hover:
            glColor3f(0.0, 0.7, 0.0)  # Bright green when hovered
        else:
            glColor3f(0.0, 0.5, 0.0)  # Dark green normally
            
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        
        # Button border
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glLineWidth(1.0)
        
        # Button text
        glColor3f(1.0, 1.0, 1.0)  # White text
        text_size = 16
        text_width = 0
        for c in text:
            text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        text_x = x + (width - text_width) // 2
        text_y = y + (height - text_size) // 2 + 5
        
        glRasterPos2f(text_x, text_y)
        for c in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    def _draw_cloud(self, x, y, size):
        """Draw a simple cloud"""
        # Cloud made of overlapping circles
        for i in range(3):
            for r in range(int(size)):
                rx = x + i * size
                ry = y
                # Draw circle using points
                glBegin(GL_POLYGON)
                for angle in range(0, 360, 10):
                    rad = math.radians(angle)
                    glVertex2f(rx + r * math.cos(rad), ry + r * math.sin(rad))
                glEnd()
    
    def _draw_dino_animated(self, x, y):
        """Draw an animated dinosaur for the intro screen"""
        # Get a bobbing animation based on animation time
        bounce = 5 * math.sin(self.animation_time * 6)
        
        glColor3f(0.0, 0.6, 0.0)  # Green color
        
        # Draw dino body as a polygon
        glBegin(GL_POLYGON)
        glVertex2f(x - 40, y + 20)  # Head top
        glVertex2f(x - 50, y)       # Back
        glVertex2f(x - 30, y - 20)  # Tail
        glVertex2f(x + 20, y - 20)  # Bottom
        glVertex2f(x + 30, y)       # Front
        glVertex2f(x + 10, y + 10)  # Head front
        glEnd()
        
        # Draw legs with animation
        glLineWidth(3.0)
        glBegin(GL_LINES)
        # Front leg
        leg_angle_front = 15 * math.sin(self.animation_time * 6)
        fx1 = x + 15
        fy1 = y - 20
        fx2 = fx1 + 15 * math.sin(math.radians(leg_angle_front))
        fy2 = fy1 - 20 * math.cos(math.radians(leg_angle_front))
        glVertex2f(fx1, fy1)
        glVertex2f(fx2, fy2)
        
        # Back leg
        leg_angle_back = -leg_angle_front
        bx1 = x - 25
        by1 = y - 20
        bx2 = bx1 + 15 * math.sin(math.radians(leg_angle_back))
        by2 = by1 - 20 * math.cos(math.radians(leg_angle_back))
        glVertex2f(bx1, by1)
        glVertex2f(bx2, by2)
        glEnd()
        glLineWidth(1.0)
        
        # Draw eye
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)  # White eye
        glVertex2f(x + 15, y + 5)
        glEnd()
        
        # Draw blinking effect
        if random.random() > 0.95:
            glLineWidth(2.0)
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINES)
            glVertex2f(x + 10, y + 5)
            glVertex2f(x + 20, y + 5)
            glEnd()
            glLineWidth(1.0)
        else:
            glPointSize(3.0)
            glBegin(GL_POINTS)
            glColor3f(0.0, 0.0, 0.0)  # Black pupil
            glVertex2f(x + 17, y + 5)
            glEnd()
        glPointSize(1.0)
            
    # Update the _draw_dino_fallen method

    def _draw_dino_fallen(self, x, y):
        """Draw a fallen dinosaur for the game over screen"""
        try:
            glColor3f(0.0, 0.6, 0.0)  # Green color
            
            # Draw rotated dino body
            glPushMatrix()
            glTranslatef(x, y, 0)
            glRotatef(-90, 0, 0, 1)  # Rotate 90 degrees
            
            # Body
            glBegin(GL_POLYGON)
            glVertex2f(-20, 40)  # Head top
            glVertex2f(0, 50)    # Back
            glVertex2f(20, 30)   # Tail
            glVertex2f(20, -20)  # Bottom
            glVertex2f(0, -30)   # Front
            glVertex2f(-10, -10) # Head front
            glEnd()
            
            # Legs sticking up
            glLineWidth(3.0)
            glBegin(GL_LINES)
            # Front leg
            glVertex2f(-15, -20)
            glVertex2f(-15, -40)
            # Back leg
            glVertex2f(15, -10)
            glVertex2f(15, -30)
            glEnd()
            glLineWidth(1.0)
            
            # X eyes for dead dino
            glLineWidth(2.0)
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_LINES)
            glVertex2f(-15, -5)
            glVertex2f(-5, 5)
            glVertex2f(-15, 5)
            glVertex2f(-5, -5)
            glEnd()
            
            glPopMatrix()  # Balance the push matrix
        except Exception as e:
            print(f"Error drawing fallen dino: {e}")
    
    def draw_high_scores(self, score_history, x=600, y=400):
        """Draw the high score history table"""
        if not score_history:
            return
            
        # Draw table title
        glColor3f(0.8, 0.8, 0.0)  # Gold color
        self._draw_text("High Scores", x, y, 18, center=True)
        
        # Draw horizontal line
        glColor3f(0.7, 0.7, 0.7)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(x - 100, y - 10)
        glVertex2f(x + 100, y - 10)
        glEnd()
        glLineWidth(1.0)
        
        # Draw table headers
        glColor3f(0.0, 0.0, 0.0)  # Black for headers
        self._draw_text("Rank", x - 80, y - 30, 14)
        self._draw_text("Score", x, y - 30, 14, center=True)
        self._draw_text("Date", x + 80, y - 30, 14, center=True)
        
        # Draw scores, limited to top 5 for space
        display_count = min(5, len(score_history))
        for i in range(display_count):
            entry = score_history[i]
            
            y_pos = y - 60 - (i * 25)
            
            # Draw rank with color based on position
            if i == 0:
                glColor3f(1.0, 0.8, 0.0)  # Gold for #1
            elif i == 1:
                glColor3f(0.8, 0.8, 0.8)  # Silver for #2
            elif i == 2:
                glColor3f(0.8, 0.5, 0.2)  # Bronze for #3
            else:
                glColor3f(0.0, 0.0, 0.0)  # Black for others
                
            self._draw_text(f"#{i+1}", x - 80, y_pos, 14)
            
            # Draw score
            self._draw_text(str(entry['score']), x, y_pos, 14, center=True)
            
            # Draw date (shortened for space)
            date_str = entry['date'].split()[0] if 'date' in entry else ""
            self._draw_text(date_str, x + 80, y_pos, 12, center=True)